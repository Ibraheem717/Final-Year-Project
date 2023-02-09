<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent( {
    created() {
        this.get_item()
        this.get_owner_id()
        this.fetch_Messages()
    },
    data() {
        return {
            item : "",
            item_owner :  0,

            rating : 0,
            review : "",

            all_messages : [],
            msg: "",
        }
    },   
    methods : {
        async get_owner_id() {
            let response = await fetch(("http://localhost:8000/ses-user"), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.item_owner = data.user_id
        },
        get_item() {
            let get_item = localStorage.getItem('author')
            if (get_item)
                this.item = get_item
            
        },
        async fetch_Messages() {
            let data = await fetch(("http://localhost:8000/GetMessage/Author/" + this.item ) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let response = await data.json()
            if (response['Existing'] == true) {
                this.all_messages = response['Values']
            }
            console.log("Time to go : " );
            console.log(this.all_messages);
             
            
        },
        async post_message() {
            if (this.msg!="") 
            {
                let data = await fetch(("http://localhost:8000/postMessage/Author"), {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                body: JSON.stringify({
                    AuthorID: this.item,
                    msg: this.msg,
                })
            })
            let response = await data.json()
            if (response.Passed)
                this.fetch_Messages()
            }
            this.msg = ""
        },
    },
} )

</script>

<template>
    <div class="p-5 text-left bg-light" style="height:100%">
        <div class="text-left bg-light">
            <div class="jumbotron">
                <h1 class="display-4">{{ item }}</h1>
                <hr class="my-4">
            </div>
        </div>

        <div>
            <p>Chat</p>
            <div>
                <table class="table">
                    <tr v-for="messages in all_messages">
                        <th>{{messages["UserID"]}}</th>
                        <th>{{ messages["Message"] }}</th>
                    </tr>
                </table>
            </div>
            <div>
                <form @submit.prevent="post_message">
                    <input class="form-control" type="text" v-model="msg">
                    <button>Post</button>
                </form>
            </div>
        </div> 

    </div>

</template>


