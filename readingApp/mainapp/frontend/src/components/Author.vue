<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'
import {CSRFToken} from './Cookie.js'

export default defineComponent( {
    created() {
        this.get_item()
        this.get_owner_id()
        this.fetch_author()
        this.fetch_books()
    },
    data() {
        return {
            item : "",
            item_owner :  0,

            author_id : -1,
            author_books : [],

            rating : 0,
            review : "",

            all_messages : [],
            msg: "",

            side : true,

            tab_users : [],

            all_tabs: [],
            new_tab: "",
            tab_id: 0,
            tab : "main",
        }
    },   
    methods : {
        async get_owner_id() {
            let response = await fetch(("./ses-user"), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.item_owner = data.user_id
            
            this.fetch_author()
        },
        get_item() {
            let get_item = localStorage.getItem('author')
            if (get_item)
                this.item = get_item
        },
        async store_user (item) {
            localStorage.setItem('user', item)
        },
        async fetch_author() {
            console.log("hello");
            let data = await fetch(("./CheckAuthor/" +this.item ) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let response = await data.json()
            this.author_id =  response['Author']
            if (this.author_id)  {
                this.fetch_tabs()

            }
            
        },
        async fetch_books() {
            console.log("hello");
            let data = await fetch(("./AuthorBooks/" +this.item ) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let response = await data.json()
            this.author_books = JSON.parse(response['Books'])

            if (this.author_books) {
                let len = Object.keys(this.author_books[Object.keys(this.author_books)[0]])
    
                let books = []
                let temp;
    
                for (const i of len) {
                    temp = {}
                    
                    for (let key in this.author_books) {
                        temp[key] = this.author_books[key][i]
                    }
                    books.push(temp)
                }
                this.author_books = books
            }

        },
        async fetch_Messages() {
            let data = await fetch(("./GetMessage/Author/" + this.item + "/" + this.tab ) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            this.all_messages = []
            let response = await data.json()
            if (response['Existing'] == true) {
                this.all_messages = response['Values']
            }             
            let LU = -1
            for (let i =0 ; i < this.all_messages.length; i++) {
                if (LU == this.all_messages[i]['UserID']['id']) {
                    this.all_messages[i]['UserID']['id'] = -1
                }                    
                else
                    LU = this.all_messages[i]['UserID']['id']
            }
            this.fetch_tabs()
        },
        async fetch_tabs() {
            let data = await fetch(("./GetAllTabs/Author/" + this.author_id['id']) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let response = await data.json()
            response = response['Author']
            this.all_tabs = []
            if (Object.keys(response).length != 0)
                this.tab = "main"
            for (let key in response) {
                this.all_tabs.push(response[key]['name'])
                if (response[key]['name'] == this.tab)
                    this.tab_id = response[key]['id']
            }
            this.fetch_user()
        },
        async fetch_user() {
            let data = await fetch(("./GetTabUsers/author/" + this.tab_id) , {
                method: 'GET',
            })
            let response = await data.json()
            console.log(response);
            response = response['tab']
            console.log(response);
            this.tab_users = []
            this.tab_users = response
        },
        async create_tab() {
            if (this.tab!="") 
            {
                let data = await fetch(("./CreateTab"), {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
                },
                body: JSON.stringify({
                    medium : 'author',
                    author: this.author_id['id'],
                    name: this.new_tab,
                })
            })
            let response = await data.json()
            this.fetch_tabs()
            }
        },
        async post_message() {
            if (this.msg!="") 
            {
                let data = await fetch(("./postMessage/Author"), {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
                },
                body: JSON.stringify({
                    AuthorID: this.item,
                    msg: this.msg,
                    tab : this.tab,
                })
            })
            let response = await data.json()
            if (response.Passed)
                this.fetch_Messages()
            }
            if (response.Passed) {
                this.fetch_Messages()
            }
            this.msg = ""
        },
        change_tab(NewTab) {
            this.tab = NewTab
            this.fetch_Messages()
        }
    },
} )

</script>

<template>

    <div class="d-flex justify-content-center">
        <button class="p-2 m-3 btn btn-secondary" @click="side=true">Other Works</button>
        <button class="p-2 m-3 btn btn-primary" @click="side=false">Forums</button>
    </div>

    <hr>

    <div class="" v-if="side">

        <table class="table table-hover mx-3">

            
            
            <div class="row d-flex justify-content-around">
                
                <tr class="col-md-4 mt-2 row border border-dark p-4 " v-for="items in author_books">
                    
                    <tr class="row ">
        
                        <th class="align-middle col-sm-2 ">Book Name</th>
                        <th class="align-middle col-sm-2 ">Book Image</th>
                        <th class="align-middle col-sm-1 ">Authors</th>
                        <th class="align-middle col-sm-4 ">Catagories</th>
                        <th class="align-middle col-sm-1 ">Pages</th>
                        <th class="align-middle col-sm-2 ">Publish Information</th>
                        
                    </tr>
                   
                    <!-- Title -->
                    <td class="col-sm-2 p-2"><router-link @click="store_item(items['isbn'])" class="nav-link p-0" :to="{path: '/Book'}"> {{items['title']}} </router-link>  </td>
                    
                    <!-- Image -->
                    <td class="col-sm-2 p-2"> 
                        <img :src="items['img']" class="img-fluid p-0">
                    </td>
                    
                    <!-- Author -->
                    <td class="align-middle col-sm-1 p-2" > 
                        <div v-if="items ['author']" class="p-0">
                                {{ items['author'] }}
                        </div>
                        <div class="p-0" v-else>
                            No Known Authors
                        </div>
                    </td>
                    
                    <!-- Genre -->
                    <td class="align-middle col-sm-4 p-2">
                        <div v-if="items['genre']" class="p-0 " style="word-wrap: break-word;">
                            {{items['genre']}}
                        </div>
                        <div class="p-0" v-else> Book has not be catagorised </div>
                    </td>
                    
                    <!-- Pages -->
                    <td class="align-middle col-sm-1 p-2">
                        <div v-if="items['pages']" class="p-0">
                            <div  class="p-0">
                                {{  items['pages'] }} Pages
                            </div>
                        </div>
                        <div class="p-0" v-else> No page count </div>
                    </td>
                    
                    <!-- Rating -->
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

    <div class="mt-3" style="height: 100rem;" v-else>

        <div class="row h-100">

            <div class="col-md-2">

                <form class="row m-1 mt-3" @submit.prevent="create_tab">

                    <div class="col-sm-9"><input class="form-control" type="text" v-model="new_tab" placeholder="Create Tab" ></div>

                    <button class="btn btn-primary col-md-3">Create</button>

                </form>

                <hr>
                
                <section style="overflow: auto; overflow-x: hidden ; ">
                    <div v-for="tab in all_tabs" class="text-center p-2 m-2 border border-dark" style="cursor: pointer;" >
                        <i v-if="tab == current_tab" class="text-secondary" >{{ tab }}</i>
                        <b v-else @click="change_tab(tab)" >{{ tab }}</b>
                    </div>
                </section>
                
            </div>
    

            <div class="col-md-8 h-90 ">   
                
                <div class="border border-dark rounded " style="height: 90%;">

                    <div class="p-4 row " style="overflow: auto; overflow-x: hidden ; width: 100%;" >
        
                        <div class="" v-for="messages in all_messages">
        
                            <div style="border-style: none; text-decoration: underline; font;" v-if="messages['UserID']['id'] != -1" class="row p-1">
                                <b>{{ messages["UserID"]['username'] }}</b> 
                            </div>
        
                            <div class="row p-0" style="font-weight: normal; margin-left: 0.1rem; margin-bottom: 0.1rem;"> 
                                <span class="border rounded m-0" style="width: auto;">{{ messages["Message"] }}</span>                                
                            </div>
        
                        </div>
                        
                    </div>

                </div>


                <div>
    
                    <form class="row m-1" @submit.prevent="post_message">
            
                        <div class="col-md-11"><input class="form-control" type="text" v-model="msg"></div>
                        
                        <button class="col-md-1 btn btn-success" style="height: 10%; background-color: green;">Post</button>
            
                    </form>
                </div>
                
            </div>

            <div class="col-md-2" style="overflow: auto; overflow-x: hidden ;">

                <section style="overflow: auto; overflow-x: hidden ; ">

                    <h3 class="text-center"> <u> Users </u> </h3>
    
                    <div class="text-center border border-dark m-2" v-for="user in tab_users">
                        <router-link @click="store_user(user['id'])" class="nav-link p-2" :to="{path: '/OtherUser'}"> <h6> {{ user['username'] }}  </h6></router-link>  
                    </div>
    
                </section>

            </div>
    




        </div>


    </div>

</template>


