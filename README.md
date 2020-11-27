# Raven's Light Photo Journal

## Project at a glance

There are three main things going on here:
| Folder | Description |
| - | - |
| `src` | Vue web app. My photoblog frontend application.
| `app` |  Flask server. Backend server providing data to the web app.
| `posts` | Posts directory. Put new posts here and original size images.

## Docker quick start

There are two apps which should both be run on the development machine:

*Flask server*
```
docker-compose build server
docker-compose run --service-ports server
```

*Vue dev server*
```
docker-compose build client
docker-compose run --service-ports client
```

## Running for development without Docker

### Dependencies

- Yarn
- Vue Cli 3
- Python 3

### Vue
```
yarn install
yarn serve
```

### Flask
```
pip install -r requirements.txt
flask", "run", "--host", "0.0.0.0
```

## Posts

Refresh `public/img` with folders and resized, watermarked images from `posts` by running
```
python update_public_posts.py
```

Adjust global variables in `update_public_posts.py` to set image size and watermark details.

### Adding a blog post

TLDR: Add a new folder to `posts`, create a `post.json` and copy over images. Run `python update_public_postss.py` to copy changes to live dev site.

A blog post is a set of images and a `post.json` file. These are in the `posts` folder,

e.g.

```
posts
└── img
    └── 2020
        ├── 09
        │   └── 1-thunderbird
        │       ├── 20200911-IMG_7124.jpg
        │       ├── 20200911-IMG_7126.jpg
        │       ├── IMG_5959.jpg
        │       └── post.json
        └── 10
            ├── 1-joy-in-life
            │   ├── 1-20200415-IMG_5172-2.jpg
            │   ├── 2-20200415-IMG_5177.jpg
            │   ├── 3-20200415-IMG_5200.jpg
            │   ├── 4-20200415-IMG_5205.jpg
            │   └── post.json
            ├── 2-the-story-of-s7ayulh-thunder
            │   └── post.json
            ├── 3-earthquake-foot
            │   ├── 20201007-IMG_7440.jpg
            │   ├── 20201007-IMG_7508.jpg
            │   ├── post.json
            │   └── sources.txt
            └── 4-lakota-dream-of-what-was-to-be
                ├── 1-20201007-IMG_7494-2.jpg
                ├── 2-20201007-IMG_7443.jpg
                ├── 3-20201007-IMG_7503.jpg
                ├── 4-20201007-IMG_7455.jpg
                ├── IMG_6308.jpg
                └── post.json
```
