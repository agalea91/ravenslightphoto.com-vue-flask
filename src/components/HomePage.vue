<template>

  <div id="app">
    <div v-if="tag">
      <h1>{{tag.replace('-', ' ')}}</h1>
      <div id="h1-lower" class="header-homepage-link">Raven's Light | A Photo Journal</div>
    </div>
    <div v-else>
      <h1>Raven's Light</h1>
      <div id="h1-lower" class="header-homepage-link">A Photo Journal</div>
    </div>
    <div class="headline-below-h1" v-show="isHome">
      <p class="headline-main-text">
        In Native American legends, Raven is said to have brought light to the world.
        <br>
        <br>
        This gallery is a brief look into that world, through the lens of my camera.
        <br>
        <br>
        - Alex
      </p>
    </div>
    <div></div>
    <SearchBox/>
    <ul>
      <li v-for="post in posts" :key="post.url_path">
        <div class="post-summary">
          <router-link
            :to="{ name: 'post', params: {
              year: post.year,
              month: post.month,
              post_name: post.post_name
            }}"
          >
            <div class="post-title">{{ post.title }}</div>
          </router-link>
          <div class="post-desc">
            {{ post.photo.desc }} | <i>{{ post.photo.date_taken }}</i> | <i>{{ post.photo.location }}</i>
          </div>
          <router-link
            :to="{ name: 'post', params: {
              year: post.year,
              month: post.month,
              post_name: post.post_name
            }}"
          >
            <img
              :src="post.cover_image"
              alt="Cover image"
              class="post-cover-image"
            >
          </router-link>
        </div>
      </li>
    </ul>
    <div class="pagination-nav" v-if="info.has_pagination">
      <router-link
        v-if="info.next_page_number"
        :to="{
          name:  isHome ? 'home': 'collection',
          params: isHome ? {} : { tag: info.tag },
          query: { page: info.next_page_number }
        }"
        style="padding-left: 25px;"
      >
        Page {{ info.next_page_number }} →
      </router-link>
      <br>
      <router-link
        v-if="info.prev_page_number"
        :to="{
          name:  isHome ? 'home': 'collection',
          params: isHome ? {} : { tag: info.tag },
          query: { page: info.prev_page_number }
        }"
        style="padding-right: 25px;"
      >
        ← Page {{ info.prev_page_number }}
      </router-link>
    </div>
    <div id="buyme-coffee">
      <a href="https://www.buymeacoffee.com/alexgalea"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=alexgalea&button_colour=000000&font_colour=ffffff&font_family=Cookie&outline_colour=ffffff&coffee_colour=FFDD00"></a>
    </div>
  </div>
</template>

<script>
import SearchBox from '@/components/SearchBox.vue'
export default {
  name: 'HomePage',
  props: {
    posts: Array,
    info: Object,
    isHome: Boolean,
    tag: String
  },
  components: {
    SearchBox
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.headline-main-text {
  // font-family: 'Playfair Display', serif;
  font-family: 'Nothing You Could Do', cursive;
  padding-bottom: 25px;
  font-size: 1.2rem;
  display: inline-block;
  width: 400px;
  max-width: 90%;
  height: 50px;
}
.post-title {
  font-family: 'Playfair Display', serif;
  margin: 40px 0 0;
  text-align: left;
  padding-left: 10px;
  font-weight: bold;
  font-size: 1.7rem;
}
.post-desc {
  // font-family: 'Playfair Display', serif;
  margin: 10px 0 0;
  text-align: left;
  padding-left: 10px;
  font-weight:normal;
  font-size: 1rem;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  // display: inline-block;
  margin: 30px;
}

.post-summary {
  width: 1000px;
  max-width: 100%;
  margin-left:auto;
  margin-right:auto;
  line-height: 100%;
}
.post-cover-image {
  max-width: 100%;
  margin: 10px;
}
.headline-below-h1 {
  display: inline-block;
  padding: 20px;
  width: 280px;
  max-width: 90%;
}
.pagination-nav {
  padding: 20px 0 40px 0;
  font-family: 'Playfair Display', serif;
  line-height: 40px;
  font-size: 1.5rem;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #545454;
    }
  }
}
</style>
