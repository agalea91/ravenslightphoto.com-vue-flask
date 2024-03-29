import Vue from 'vue'
import Router from 'vue-router'
import VueHead from 'vue-head'
import VueAnalytics from 'vue-analytics'

import Home from './views/Home.vue'
import Collections from './views/Collections.vue'
import About from './views/About.vue'
import CookiesPolicy from './views/CookiesPolicy.vue'
import PhotoblogPost from './views/PhotoblogPost.vue'
import Error404 from './views/Error404.vue'

Vue.use(VueHead)
Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/collections',
      name: 'collections',
      component: Collections
    },
    {
      path: '/collection/:tag',
      name: 'collection',
      component: Home
    },
    {
      path: '/album/:year/:month/:post_name',
      name: 'post',
      component: PhotoblogPost
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/cookies-policy',
      name: 'cookies-policy',
      component: CookiesPolicy
    },
    {
      path: '/404',
      name: 'error-404',
      component: Error404
    },
    {
      path: '*',
      componen: Error404
    }
  ],
  mode: 'history'
})

Vue.use(VueAnalytics, {
  id: process.env.VUE_APP_GA_UNIVERSAL_ANALYTICS_ID,
  router
})

export default router
