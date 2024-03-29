# -*- coding: utf-8 -*-

import re
import json
import glob
import os
import sys
import shutil
import pathlib

import traceback

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

PROC_PATH = pathlib.Path("processed")
POST_PATH = pathlib.Path("posts")
PUB_PATH = pathlib.Path("public")
IGNORE_POSTS_STARTSWITH = "_"
WATERMARK_FONT_SIZE = 25
MAX_PX_SIZE = 1280
WATERMARK_DOMAIN = "ravenslightphoto.com"

def main(post_slug):
    """ Process images in "posts" - shrink, watermark, etc.

    Default is to process all posts unless post_slug argument is given.

    post_slug : str
        Only process this post.
    """
    if post_slug:
        print(f"Copying single post: {post_slug}")
        print("Desination folder is not cleaned prior to processing.")
    else:
        print("Refreshing all posts")
        delete_folder(PUB_PATH / "img")


    post_cat_img_fp = POST_PATH / "img" / "categories"
    pub_cat_img_fp = PUB_PATH / "img" / "categories"
    pub_cat_img_fp.mkdir(exist_ok=True, parents=True)
    print("Copying posts/img/categories/photo.json")
    src = post_cat_img_fp / "photo.json"
    dest = pub_cat_img_fp / "photo.json"
    shutil.copyfile(src, dest)
    print("Copying posts/img/categories/quote.json")
    src = post_cat_img_fp / "quote.json"
    dest = pub_cat_img_fp / "quote.json"
    shutil.copyfile(src, dest)

    post_fps = read_posts()
    for fp in post_fps:
        if fp.parts[-1].startswith(IGNORE_POSTS_STARTSWITH):
            print(f"Ignoring {fp}")
            continue
        elif post_slug and not str(fp).endswith(post_slug):
            print(f"Ignoring {fp}")
            continue
        else:
            print(f"Processing {fp}")
        try:
            image_files = read_post_images(fp)
        except:
            print(f"Failed to read images in post: {fp}")
            print(traceback.print_exc())
            image_files = []

        pub_fp = PUB_PATH / (pathlib.Path(*fp.parts[1:]))
        proc_fp = PROC_PATH / (pathlib.Path(*fp.parts[1:]))
        if post_slug:
            delete_folder(pub_fp)
            delete_folder(proc_fp)

        post_fp = (fp / "post.json")
        pub_post_fp = (pub_fp / "post.json")
        print(f"{str(post_fp)} -> {str(pub_post_fp)}")
        pathlib.Path(*pub_post_fp.parts[:-1]).mkdir(exist_ok=True, parents=True)
        shutil.copyfile(post_fp, pub_post_fp)

        for image in image_files:
            image_fp = (fp / image["file"])
            proc_image_fp = dict(
                small=(proc_fp / f"sm_{image['file']}"),
                small_watermark=(proc_fp / f"sm_wk_{image['file']}"),
            )
            pub_image_fp = (pub_fp / image["file"])
            print(image_fp)

            image_obj = load_image(image_fp)
            image_obj_small = resize_pixels(image_obj, MAX_PX_SIZE)
            image_obj_small_watermark = add_watermark(image_obj_small, date=image["date"], photographer=image["photographer"])

            # Write to "processed" folder
            print(f"{str(image_fp)} -> {str(proc_image_fp['small'])}")
            write_image(image_obj_small, proc_image_fp['small'])
            print(f"{str(image_fp)} -> {str(proc_image_fp['small_watermark'])}")
            write_image(image_obj_small_watermark, proc_image_fp['small_watermark'])

            # Write to "public" folder
            print(f"{str(image_fp)} -> {str(pub_image_fp)}")
            write_image(image_obj_small_watermark, pub_image_fp)


def delete_folder(folder):
    ans = input(f"WARNING: about to delete {str(folder)} folder. Press enter to proceed.")
    if ans.strip() == "":
        try:
            shutil.rmtree(folder)
        except FileNotFoundError:
           pass
    else:
        sys.exit("User exit")




def load_image(image_fp):
    image = Image.open(image_fp).convert("RGBA")
    return image
    


def add_watermark(image_obj, date, photographer):
    photo_date = re.findall("\d{4}", date)[0]
    upper_right_text = f"© {photographer} {photo_date}"
    bottom_left_text = f"{WATERMARK_DOMAIN}"
    
    txt_obj = Image.new("RGBA", image_obj.size, (255,255,255,0))
    font = ImageFont.truetype("./fonts/PlayfairDisplay-Black.ttf", WATERMARK_FONT_SIZE)
    draw = ImageDraw.Draw(txt_obj)
    w, h = image_obj.size
    draw.text((w-400, 50), upper_right_text, (255,255,255, 70), font=font)
    draw.text((50, h-100), bottom_left_text, (255,255,255, 70), font=font)
    image_obj = Image.alpha_composite(image_obj, txt_obj)
        
#     from matplotlib.pyplot import imshow
#     import numpy as np        
#     image_obj.convert('RGB').save('./dev/watermark.jpg')
#     imshow(np.asarray(image_obj), aspect='auto')
#     raise
    
    return image_obj


    

def resize_pixels(image_obj, max_px_size):
    width_0, height_0 = image_obj.size

    if max((width_0, height_0)) <= max_px_size:
        # The image is smaller than the crop size, do nothing
        return image_obj

    if width_0 > height_0:
        wpercent = max_px_size / float(width_0)
        hsize = int(float(height_0) * float(wpercent))
        img = image_obj.resize((max_px_size, hsize), Image.ANTIALIAS)
        return img
    else:
        hpercent = max_px_size / float(height_0)
        wsize = int(float(width_0) * float(hpercent))
        img = image_obj.resize((wsize, max_px_size), Image.ANTIALIAS)
        return img

def read_posts():
    post_folders = glob.glob(str(POST_PATH / "img" / "*" / "*" / "*"), recursive=True)
    post_folders = [pathlib.Path(folder) for folder in post_folders]
    return post_folders


def read_post_images(post_fp):
    images = []
    with open((post_fp / "post.json"), "rb") as f:
        post = json.load(f)
        for block in post["body"]["divs"]:
            if block["type"] == "photo":
                photo = block["file"]
                if not photo:
                    continue
                images.append({})
                images[-1]["file"] = photo
                images[-1]["date"] = post["photo"]["date_taken"]
                images[-1]["photographer"] = post["photo"]["photographer"]
    return images


def write_image(image_obj, pub_image_fp):
    pub_image_fp.parent.mkdir(exist_ok=True, parents=True)
    image_obj.convert("RGB").save(pub_image_fp, optimize=True, quality=95)
    print(f"{ pathlib.Path(pub_image_fp).stat().st_size / 1e3 } kb")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert images in posts to public images for website")
    parser.add_argument(
        "--post-slug",
        default="",
        help=(
            "Update a single post (skip the rest). "
            "Example slug: 4-lakota-dream-of-what-was-to-be"
        )
    )
    args = parser.parse_args()
    post_slug = args.post_slug
    main(post_slug)

