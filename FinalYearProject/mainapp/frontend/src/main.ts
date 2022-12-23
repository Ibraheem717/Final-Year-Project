import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import App from './App.vue'
import Profile from './components/Profile.vue'
import auctionForm from './components/auctionForm.vue'
import view_items from './components/view_items.vue'
import Item from './components/Item.vue'
import my_items from './components/my_items.vue'

function getCookie(name : any) {
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
        {path: '/auctionForm', name: 'Auction Form', component: auctionForm, props: {csrfToken}},
        {path: '/item', name: 'Item', component: Item},
        {path: '/view_items', name: 'All Items', component: view_items},
        {path: '/my_items', name: 'My Items', component: my_items},
    ]
})


createApp(App).use(router).mount('#app')
