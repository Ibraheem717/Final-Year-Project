import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import App from './App.vue'
import Profile from './components/Profile.vue'
import Recommendation from './components/Recommendation.vue'
import Search from './components/Search.vue'
import Book from './components/Book.vue'
import Forums from './components/Forums.vue'
import ForumPage from './components/ForumPage.vue'
import Author from './components/Author.vue'

let hostname = "http://localhost:8000/"

function getCookie(name) {
    if (!document.cookie) {
      return null;
    }
  
    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));
  
    if (xsrfCookies.length === 0) {
      return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
  }

const csrfToken = getCookie('CSRF-TOKEN');

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/Profile', name: 'Profile', component: Profile},
        {path: '/Recommendation', name: 'Recommendation', component: Recommendation, props: {cookie:csrfToken}},
        {path: '/Book', name: 'Item', component: Book},
        {path: '/Search', name: 'Search', component: Search},
        {path: '/Forums', name: 'Forums', component: Forums},
        {path: '/ForumPage', name: 'Forum Page', component: ForumPage},
        {path: '/Author', name: 'Author Page', component: Author},
    ]
})


createApp(App).use(router).mount('#app')
