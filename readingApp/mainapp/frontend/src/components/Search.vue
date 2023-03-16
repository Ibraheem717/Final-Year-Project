<script>
import { defineComponent } from 'vue'

export default defineComponent( {
    created() {
        this.get_owner_id()
        this.get_auction_items()
    },
    props: [
        'hostname' ,
    ],
    props: [
        'hostname' ,
    ],
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
            let response = await fetch(this.hostname + "Search", {method: "GET" })
            let data = await response.json()
            let tempArr = []
            for (let i = 0; i < data['file'].length; i++)
                tempArr.push(JSON.parse(data['file'][i])) 
            this.total_items = tempArr
            console.log(this.total_items);          
        },
        async get_owner_id() {
            let response = await fetch(this.hostname+"ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id
        },
       async store_item (item) {
            localStorage.setItem('item', item)
       },
       async Search(request) {
        let response = await fetch((this.hostname+"SearchGeneral/" + request), {method: "GET" })
        let data = await response.json()
        let tempArr = []
        for (let i = 0; i < data['file'].length; i++)
            tempArr.push(JSON.parse(data['file'][i])) 
        this.total_items = tempArr
        console.log(this.total_items);      
       },
       async bruh(request) {
        let response = await fetch((this.hostname+"test"), {method: "GET" })
       },
    },
} )

</script>

<template>

    <div class="p-5 text-left bg-light" style="height:100%">

        <div class="text-left bg-light">

            <div class="jumbotron">

                <h1 class="display-4">Listings</h1>

                <div class="row">

                    <form class="col-sm-3 row" @submit.prevent="Search(search)">

                        <div class="col-sm-9"><input class="form-control" type="text" v-model="search" placeholder="Search" ></div>

                        <button class="btn btn-primary col-sm-2">Enter</button>

                    </form>

                    <button class="btn btn-danger col-sm-1" @click="get_auction_items" >Reset</button>

                </div>

                <hr class="my-4">

            </div>

        </div>

        <table class="table table-hover mx-3">

            <div class="d-flex justify-content-center"><button class="btn btn-secondary" @click="get_auction_items">Refresh</button></div>
            
            <hr class="">
            
            <div class="row d-flex justify-content-around">
                
                <tr class="col-md-5 mt-2 row border border-dark " v-for="items in total_items">
                    
                    <tr class="row ">
        
                        <th class="align-middle col-sm-2 px-4">Book Name</th>
                        <th class="align-middle col-sm-2 px-4">Book Image</th>
                        <th class="align-middle col-sm-1 px-4">Authors</th>
                        <th class="align-middle col-sm-4 px-4 text-center">Catagories</th>
                        <th class="align-middle col-sm-1 px-4">Pages</th>
                        <th class="align-middle col-sm-2 px-4">Publish Information</th>
                        
                    </tr>
                   
                    <!-- Title -->
                    <td class="col-sm-2 p-4"><router-link @click="store_item(items['isbn'])" class="nav-link p-0" :to="{path: '/Book'}"> {{items['title']}} </router-link>  </td>
                    
                    <!-- Image -->
                    <td class="col-sm-2 p-4"> 
                        <img :src="items['img']" class="img-fluid p-0">
                    </td>
                    
                    <!-- Author -->
                    <td class="align-middle col-sm-1 p-4" > 
                        <div v-if="items ['author']" class="p-0">
                                {{ items['author'] }}
                        </div>
                        <div class="p-0" v-else>
                            No Known Authors
                        </div>
                    </td>
                    
                    <!-- Genre -->
                    <td class="align-middle col-sm-4 p-4 text-center">
                        <div v-if="items['genre']" class="p-0 " style="word-wrap: break-word;">
                            {{items['genre']}}
                        </div>
                        <div class="p-0" v-else> Book has not be catagorised </div>
                    </td>
                    
                    <!-- Pages -->
                    <td class="align-middle col-sm-1 p-4">
                        <div v-if="items['pages']" class="p-0">
                            <div  class="p-0">
                                {{  items['pages'] }} Pages
                            </div>
                        </div>
                        <div class="p-0" v-else> No page count </div>
                    </td>
                    
                    <!-- Rating -->
                    <td class="align-middle col-sm-2 p-4">
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
                        
                        <!-- Review -->
                        <div v-if="items['reviews']" class="p-0">
                            <div  class="p-0">
                                Number of Reviews : {{  items['reviews'] }}
                            </div>
                        </div>
                        <div class="p-0" v-else> No Known Publish Data </div>

                    </td> 
    
                </tr>
                

            </div>
            

        </table>

    </div>


</template>


