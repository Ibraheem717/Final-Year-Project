 <script lang="ts">
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'

export default defineComponent( {
    created() {
        this.get_owner_id()
        this.get_auction_items()
    },
    data() {
        return {
            all_items : [],
            user_id : 0,
        }
        
    },
    methods : {
        async get_auction_items() {
            let response = await fetch("http://localhost:8000/my-all-items", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.all_items = data.items
            console.log(this.all_items);
            
        },
        async get_owner_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id
        },
       async store_item (item: string) {
            localStorage.setItem('item', item)
       },
       async edit_item (ID : number, Title : string, Description : String, starting_price : number, current_price : number, auction_finish : Date) {
        let response = await fetch("http://localhost:8000/my-all-items", {method: "PUT", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" ,
            body:JSON.stringify({
                ID : ID, Title : Title, Description : Description, starting_price : starting_price, current_price : current_price, auction_finish : auction_finish, owner : this.user_id
            })
        })
            let data = await response.json()
            this.all_items = data
            console.log(this.all_items);
       },
    },
} )

</script>

<template>

    <div class="p-5 text-left bg-light" style="height:100%">
        <div class="text-left bg-light">
            <div class="jumbotron">
                <h1 class="display-4">My Items</h1>
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
                <th class="align-middle">Auction End Date</th>
            </tr>
            <tr v-for="items in all_items">

                <td>  <router-link @click="store_item(items['ID'])" class="nav-link" :to="{path: '/item'}"> {{items['Title']}} </router-link> </td>

                <td class="w-25"> 
                    <img :src="'http://localhost:8000' + items['Item Picture']" alt="" class="img-fluid "> 
                </td>

                <td class="align-middle"> {{ items ['Description'] }} </td>

                <td class="align-middle"> £{{ items ['Starting Price'] }} </td>

                <td class="align-middle"> £{{ items ['Current Price'] }} </td>

                <td class="align-middle"> {{ items ['Auction End'] }} </td>

            </tr>
        </table>
    </div>

</template>


