<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent( {
    created() {
        this.get_item()
        this.get_owner_id()
        this.fetch_Messages()
        this.fetch_tabs()
    },
    data() {
        return {
            Forum : "",
            item_owner :  0,

            rating : 0,
            review : "",

            all_messages : [],
            msg: "",

            all_tabs : [],
            current_tab : "main",
            tab_id : 0,
            new_tab : "",
            tab_users : []
        }
    },   
    methods : {
        async get_owner_id() {
            let response = await fetch(("http://localhost:8000/ses-user"), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.item_owner = data.user_id
        },
        get_item() {
            let get_item = localStorage.getItem('forum')
            if (get_item)
                this.Forum = get_item
            
        },
        async store_item (item) {
            localStorage.setItem('user', item)
        },
        async fetch_tabs() {
            let data = await fetch(("http://localhost:8000/GetTabs/" + this.Forum) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let response = await data.json()
            response = response['Forums']
            this.all_tabs = []
            for (let key in response) {
                this.all_tabs.push(response[key]['name'])
                if (response[key]['name'] == this.current_tab)
                    this.tab_id = response[key]['id']
            }
            this.fetch_user()
        },
        async fetch_user() {
            let data = await fetch(("http://localhost:8000/GetTabUsers/" + this.tab_id) , {
                method: 'GET',
            })
            let response = await data.json()
            console.log(response);
            response = response['tab']
            console.log(response);
            this.tab_users = []
            this.tab_users = response
        },
        async fetch_Messages() {
            let data = await fetch(("http://localhost:8000/GetForumTab/" + this.Forum + "/" + this.current_tab) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let response = await data.json()
            response = response['Forums']
            this.all_messages = []
            for (let key in response) {
                this.all_messages.push(response[key]['message'])
            }
            let LU = -1
            for (let i =0 ; i < this.all_messages.length; i++) {
                if (LU == this.all_messages[i]['UserID']['id']) {
                    this.all_messages[i]['UserID']['id'] = -1
                }
                    
                else
                    LU = this.all_messages[i]['UserID']['id']
            }             
            
        },
        async post_message() {

            let data = await fetch(("http://localhost:8000/postMessage/Forum"), {
            method: 'POST',
            credentials: "include",
            mode: "cors",
            referrerPolicy: "no-referrer",
            body: JSON.stringify({
                ForumID: this.Forum,
                msg: this.msg,
                tab : this.current_tab,
                })
            })
            let response = await data.json()
            if (response.Passed)
                this.fetch_Messages()
            
            this.msg = ""
        },

        async create_tab() {
            if (this.current_tab!="") 
            {
                let data = await fetch(("http://localhost:8000/CreateForumTab"), {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                body: JSON.stringify({
                    forum: this.Forum,
                    name: this.new_tab,
                })
            })
            let response = await data.json()
            this.fetch_tabs()
            }
        },
        change_tab(NewTab) {
            this.current_tab = NewTab
            this.fetch_Messages()
        }
    },
} )

</script>

<template>
    <div class="p-5 text-left bg-light container" style="height: 100%;">

            <div class="collapse" id="navbarToggleExternalContent">
            <div class="bg-dark p-4">
                <h5 class="text-white h4">Collapsed content</h5>
                <span class="text-muted">Toggleable via the navbar brand.</span>
            </div>
            </div>
            <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggleExternalContent" 
                    aria-controls="navbarToggleExternalContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            </nav>

            <div class="row">

                <form class="col-sm-4 row" @submit.prevent="create_tab">

                    <div class="col-sm-9"><input class="form-control" type="text" v-model="new_tab" placeholder="Search" ></div>

                    <button class="btn btn-primary col-sm-2">Enter</button>

                </form>

            </div>

            <section>
                <div v-for="tab in all_tabs">
                    <b @click="change_tab(tab)">{{ tab }}</b>
                </div>
            </section>
                

            <div class="p-1 row border border-dark rounded" style="overflow: auto; overflow-x: hidden ; width: 100%;" >

                <div class="" v-for="messages in all_messages">

                    <div style="border-style: none; text-decoration: underline; font;" v-if="messages['UserID']['id'] != -1" class="row">
                        <b>{{ messages["UserID"]['username'] }}</b> 
                    </div>

                    <div class="row p-0" style="font-weight: normal; margin-left: 0.1rem; margin-bottom: 0.1rem;"> 
                        <span class="border rounded m-0" style="width: auto;">{{ messages["Message"] }}</span>                                
                    </div>

                </div>
                
            </div>
    

                <div>

                <form class="row m-1" @submit.prevent="post_message">
        
                    <div class="col-md-11"><input class="form-control" type="text" v-model="msg"></div>
                    
                    <button class="col-md-1 btn btn-success" style="height: 10%; background-color: green;">Post</button>
        
                </form>
            </div>

            <section>

                <div v-for="user in tab_users">
                    <router-link @click="store_item(user['id'])" class="nav-link" :to="{path: '/OtherUser'}"> <h6> {{ user['username'] }}  </h6></router-link>  
                </div>

            </section>

    </div>



</template>


