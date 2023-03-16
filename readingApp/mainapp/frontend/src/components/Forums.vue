 <script>
import { defineComponent } from 'vue'
import {CSRFToken} from './Cookie.js'

export default defineComponent( {
    created() {
        this.get_owner_id()
        this.GetForums()
    },
    props: [
        'hostname' ,
    ],
    data() {
        return {
            all_items : [],
            user_id : 0,

            Name : '',
            AllForums : []
        }
        
    },
    methods : {
        async get_owner_id() {
            let response = await fetch(this.hostname+"ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id
        },
       async GetForums ( ) {
        let data = await fetch(this.hostname+"GetForums", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
        let response = await data.json()
        this.AllForums = response['Forums']
       },
       async CreateForum() {
        let data = await fetch(this.hostname+"CreateForum", 
        {   method: 'POST',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({
                user : this.user_id,
                Name : this.Name
            })
        })
        let reponse = await data.json()
        this.GetForums()
       },
        store_item (item) {
            localStorage.setItem('forum', item)
       },
    },
} )

</script>

<template>


    <form class="row p-5" @submit.prevent="CreateForum">

        <div class="col-md-2"><input class="form-control" type="text" v-model="Name" placeholder="Create new forum"></div>
        
        <button class="col-md-1 btn btn-primary">Add new forum</button>

    </form>
    
    <hr style="padding-bottom: 0.5rem; padding-top: 1rem;">

    <div class="row">

        <div class="col-md-4 p-5" v-for="forum in AllForums">
                
            <router-link @click="store_item(forum['id'])" class="nav-link" :to="{path: '/ForumPage'}"> 

                <div class="row p-5 border border-primary">

                    <div class=" col-3 font-weight-bold" style="font-weight: bolder;">
                        {{ forum['Name'] }}
                    </div>  

                    <div class="col-5">
                        Number Of Messages : {{ forum['NumberOfMessages'] }}
                    </div>

                    <div class="col-4">
                        Number Of Users : {{ forum['NumberOfUsers'] }}
                    </div>

                </div>

            </router-link>  

        </div>

    </div>

</template>


