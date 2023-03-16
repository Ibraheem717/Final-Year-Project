import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import App from './App.vue'
import Profile from './components/Profile.vue'
import OtherUser from './components/OtherUser.vue'
import Recommendation from './components/Recommendation.vue'
import Search from './components/Search.vue'
import Book from './components/Book.vue'
import Forums from './components/Forums.vue'
import ForumPage from './components/ForumPage.vue'
import Author from './components/Author.vue'


let hostname = "./"

const csrfToken = getCookie('CSRF-TOKEN');

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/Profile', name: 'Profile', component: Profile},
        {path: '/OtherUser', name: 'User Page', component: OtherUser},
        {path: '/Recommendation', name: 'Recommendation', component: Recommendation, props: {cookie:csrfToken}},
        {path: '/Book', alias:'', name: 'Item', component: Book},
        {path: '/Search', name: 'Search', component: Search},
        {path: '/Forums', name: 'Forums', component: Forums},
        {path: '/ForumPage', name: 'Forum Page', component: ForumPage},
        {path: '/Author', name: 'Author Page', component: Author},
        
    ]
})


createApp(App).use(router).mount('#app')
