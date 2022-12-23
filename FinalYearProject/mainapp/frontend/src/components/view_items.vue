<script lang="ts">
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'


export default defineComponent( {
    created() {
        this.get_owner_id()
        this.get_auction_items()
    },
    data() {
        return {
            all_items : [],
            user_id : 0,
            data : "",
            bidded : true,
            new_bid : 0,
            search : ""
        }
        
    },
    methods : {
        async get_auction_items() {
            let response = await fetch("http://localhost:8000/all-items", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.all_items = data
            
            
        },
        async get_owner_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id
        },
       async store_item (item: string) {
            localStorage.setItem('item', item)
       },
       async bid(bid:number, item_id : number, date : Date) {
        let data = await fetch("http://localhost:8000/bid", {
                method: 'PUT', credentials: "include", mode: "cors", referrerPolicy: "no-referrer",
                body: JSON.stringify({
                    item_owner : this.user_id,
                    ID : item_id,
                    new_bid : bid,
                    end_date : date
                })
            })
            let response = await data.json()
            this.bidded = response.success
            console.log(this.bidded)
            if (this.bidded != true)
                alert("Invalid Bid")
            else 
                this.get_auction_items()
       },
       async Search(request:string) {
        let data = await fetch(("http://localhost:8000/search-items/" + request), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
        let response = await data.json()
        this.all_items = response.responses
        
       },
    },
} )

</script>

<template>

    <div class="p-5 text-left bg-light" style="height:100%">
        <div class="text-left bg-light">
            <div class="jumbotron">
                <h1 class="display-4">Listings</h1>
                <div>
                    <form @submit.prevent="Search(search)">
                        <input type="text" v-model="search" placeholder="Search" >
                        <button>Enter</button>
                    </form>
                    <button @click="get_auction_items" >Reset</button>
                </div>
                <hr class="my-4">
            </div>
        </div>



        <table class="table table-hover">
            <tr>
                <th class="align-middle">Item Name</th>
                <th class="align-middle">Item Image</th>
                <th class="align-middle">Description</th>
                <th class="align-middle">Starting Price</th>
                <th class="align-middle">Current Price</th>
                <th class="align-middle"></th>
                <th class="align-middle">Auction End Date</th>
            </tr>
            <tr v-for="items in all_items">

                <td><router-link @click="store_item(items['ID'])" class="nav-link" :to="{path: '/item'}"> {{items['Title']}} </router-link>  </td>

                <td class="w-25"> 
                    <img :src="'http://localhost:8000' + items['Item Picture']" alt="http://localhost:8000/mainapp/media/defaultIcon.jpg" class="img-fluid">
                </td>

                <td class="align-middle">{{ items ['Description'] }} </td>

                <td class="align-middle">£{{ items ['Starting Price'] }} </td>

                <td class="align-middle">
                    £{{ items ['Current Price'] }} 
                </td>

                <td class="align-middle">
                    <form @submit.prevent="bid(new_bid, items['ID'], items['Auction End'])">
                        <div class="row justify-content-between g-3">

                            <div class="col-auto">
                                <input type="number" name="bid" v-model="new_bid" class="form-control">
                            </div>
                            <div class="col-auto">
                                <button class="btn btn-primary">Raise</button>
                            </div>
                        </div>
                    </form>
                </td>
                <td class="align-middle">{{ items ['Auction End'] }}</td>

            </tr>
        </table>
    </div>


</template>


