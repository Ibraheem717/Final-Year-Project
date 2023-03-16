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


let hostname = "http://localhost:8000/"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/Profile', alias:'', name: 'Profile', component: Profile, props : {hostname: hostname}},
        {path: '/OtherUser', name: 'User Page', component: OtherUser, props : {hostname: hostname}},
        {path: '/Recommendation', name: 'Recommendation', component: Recommendation, props : {hostname: hostname}},
        {path: '/Book', name: 'Item', component: Book, props : {hostname: hostname}},
        {path: '/Search', name: 'Search', component: Search, props : {hostname: hostname}},
        {path: '/Forums', name: 'Forums', component: Forums, props : {hostname: hostname}},
        {path: '/ForumPage', name: 'Forum Page', component: ForumPage, props : {hostname: hostname}},
        {path: '/Author', name: 'Author Page', component: Author, props : {hostname: hostname}},
        
    ]
})


createApp(App).use(router).mount('#app')
