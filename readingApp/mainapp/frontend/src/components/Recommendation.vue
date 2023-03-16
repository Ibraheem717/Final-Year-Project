<script>
import { defineComponent } from 'vue'

export default defineComponent( {
    props: [
        'cookies'
    ],
    created() {
        this.get_owner_id()
        this.GetRecomended()
    },
    props: [
        'hostname' ,
    ],
    data() {
        return {
            item_owner : "",
            recomended : [],
            RecomendedStart : 0,
            RecomendedOptions : [0,1,2,3,4,5],
            End : false,
        }
        
    },
    methods : {
        async get_owner_id() {
            let response = await fetch(this.hostname+"ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.item_owner = data.user_id
        },
        async store_item (item) {
            localStorage.setItem('item', item)
       },
        async GetRecomended() {
            this.recomended = []
            this.End = false
            let data = await fetch((this.hostname+"GetRecommendation/" + this.RecomendedStart*10), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let response = await data.json()
            response = response['Found']
            if (response) {
            for (let i of response) {
                this.recomended.push(await this.GetBook(i))
            }}
            else
                this.End = true
            console.log(this.recomended.length);
            console.log(this.RecomendedStart);
        },
        async GetBook(isbn) {
            let response = await fetch((this.hostname+"Search/" + isbn) , {
                method: "GET",  
            })
            let retrieved_data = await response.json()
            let item = JSON.parse(retrieved_data['Book'])
            let index = Object.keys(item['author'])[0]
            for (let key in item){
                item[key] = item[key][index]}
            return item
        },
    }
} )

</script>

<template>

    <div class="p-5 text-left bg-light" style="height:100%">
        <div class="text-left bg-light">
            <div class="jumbotron">
                <h1 class="display-4">Recommendation</h1>
                <hr class="my-4">
            </div>
        </div>

        <div v-if="recomended.length==0">

            <h1>No books rereviewed</h1>

        </div>

        <div v-else>

            <table class="table table-hover">
    
                <tr class="row mt-1">
    
                    <th class="align-middle col-sm-2 p-2">Book Name</th>
                    <th class="align-middle col-sm-2 p-2">Book Image</th>
                    <th class="align-middle col-sm-2 p-2">Authors</th>
                    <th class="align-middle col-sm-2 p-2">Catagories</th>
                    <th class="align-middle col-sm-2 p-2">Pages</th>
                    <th class="align-middle col-sm-2 p-2">Publish Information</th>
                    
                </tr>
                
                <tr class="mt-2 row" v-for="items in recomended">
    
                    <!-- {{ items }} -->
    
                    <td class="col-sm-2 p-2"><router-link @click="store_item(items['isbn'])" class="nav-link p-0" :to="{path: '/Book'}"> {{items['title']}} </router-link>  </td>
    
                    <td class="col-sm-2 p-2"> 
                        <img :src="items['img']" class="img-fluid p-0" width="300" height="400" alt="No Image">
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

        </div>
        

</template>