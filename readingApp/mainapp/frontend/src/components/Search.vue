<script>
import { defineComponent } from 'vue'

export default defineComponent( {
    created() {
        this.get_owner_id()
        this.get_auction_items()
    },
    data() {
        return {
            user_id : 0,
            data : "",
            bidded : true,
            new_bid : 0,
            search : "",
            total_items : [],
        }
        
    },
    methods : {
        async get_auction_items() {
            let response = await fetch("http://localhost:8000/Search", {method: "GET" })
            let data = await response.json()
            let tempArr = []
            for (let i = 0; i < data['file'].length; i++)
                tempArr.push(JSON.parse(data['file'][i])) 
            this.total_items = tempArr
            console.log(this.total_items);          
        },
        async get_owner_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id
        },
       async store_item (item) {
            localStorage.setItem('item', item)
       },
       async Search(request) {
        let response = await fetch(("http://localhost:8000/SearchGeneral/" + request), {method: "GET" })
        let data = await response.json()
        let tempArr = []
        for (let i = 0; i < data['file'].length; i++)
            tempArr.push(JSON.parse(data['file'][i])) 
        this.total_items = tempArr
        console.log(this.total_items);      
       },
       async bruh(request) {
        let response = await fetch(("http://localhost:8000/add"), {method: "GET" })
       },
    },
} )

</script>

<template>

    <button @click="bruh">okosdkfosdjfsd</button>

    <div class="p-5 text-left bg-light" style="height:100%">

        <div class="text-left bg-light">

            <div class="jumbotron">

                <h1 class="display-4">Listings</h1>

                <div class="row">

                    <form class="col-sm-4 row" @submit.prevent="Search(search)">

                        <div class="col-sm-9"><input class="form-control" type="text" v-model="search" placeholder="Search" ></div>

                        <button class="btn btn-primary col-sm-2">Enter</button>

                    </form>

                    <button class="btn btn-danger col-sm-1" @click="get_auction_items" >Reset</button>

                </div>

                <hr class="my-4">

            </div>

        </div>

        <table class="table table-hover">

            <tr class="row mt-1">

                <th class="align-middle col-sm-2 p-2">Book Name</th>
                <th class="align-middle col-sm-2 p-2">Book Image</th>
                <th class="align-middle col-sm-2 p-2">Authors</th>
                <th class="align-middle col-sm-2 p-2">Catagories</th>
                <th class="align-middle col-sm-2 p-2">Pages</th>
                <th class="align-middle col-sm-2 p-2">Publish Information</th>
                
            </tr>
            
            <tr class="mt-2 row" v-for="items in total_items">

                <!-- {{ items }} -->

                <td class="col-sm-2 p-2"><router-link @click="store_item(items['isbn'])" class="nav-link p-0" :to="{path: '/Book'}"> {{items['title']}} </router-link>  </td>

                <td class="col-sm-2 p-2"> 
                    <img :src="items['img']" class="img-fluid p-0">
                </td>

                <td class="align-middle col-sm-2 p-2" > 
                    <div v-if="items ['author']" class="p-0">
                            {{ items['author'] }}
                    </div>
                    <div class="p-0" v-else>
                        No Known Authors
                    </div>
                </td>

                <td class="align-middle col-sm-2 p-2">
                    <div v-if="items['genre']" class="p-0 " style="word-wrap: break-word;">
                        {{items['genre']}}
                    </div>
                    <div class="p-0" v-else> Book has not be catagorised </div>
                </td>

                <td class="align-middle col-sm-2 p-2">
                    <div v-if="items['pages']" class="p-0">
                        <div  class="p-0">
                            {{  items['pages'] }} Pages
                        </div>
                    </div>
                    <div class="p-0" v-else> No page count </div>
                </td>

                <td class="align-middle col-sm-2 p-2">
                    <div v-if="items['rating']" class="p-0">
                        <div  class="p-0">
                            Rating : {{  items['rating'] }}
                        </div>
                    </div>
                    <div class="p-0" v-else> No Known Publisher </div>

                    <div v-if="items['totalratings']" class="p-0">
                        <div  class="p-0">
                            Number of Rating : {{  items['totalratings'] }}
                        </div>
                    </div>

                    <div v-if="items['reviews']" class="p-0">
                        <div  class="p-0">
                            Number of Reviews : {{  items['reviews'] }}
                        </div>
                    </div>
                    <div class="p-0" v-else> No Known Publish Data </div>
                </td> 
            </tr>

        </table>

    </div>


</template>


