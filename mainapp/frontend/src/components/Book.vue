<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'
import {CSRFToken} from './Cookie.js'

export default defineComponent( {
    created() {
        this.get_item()
        this.get_owner_id()
        this.GetBook()
        this.fetch_reviews()
        this.fetch_tabs()
    },
    props: [
        'hostname' ,
    ],
    data() {
        return {
            item : "",
            item_owner :  0,
            ItemIndex : 0,
            ItemISBN : 0,

            rating : 0,
            review : "",
            user_reviews: [],
            review_counter : 0,

            tracked : false,
            pages_read : 0,

            all_messages : [],
            msg: "",
            LastUser : 0,

            tab_users : [],

            all_tabs: [],
            new_tab: "",
            tab_id: 0,
            tab : "main",
        }
    },   
    methods : {
        async get_owner_id() {
            let response = await fetch((this.hostname+"ses-user"), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.item_owner = data['user_id']
            console.log(this.item_owner);
            this.check_tracker()
        },
        get_item() {
            let get_item = localStorage.getItem('item')
            if (get_item)
                this.ItemISBN = get_item
            
        },
        async store_item (item) {
            localStorage.setItem('author', item)
        },
        async GetBook() {
            let response = await fetch((this.hostname+"Search/" + this.ItemISBN) , {
                method: "GET",  
            })
            let retrieved_data = await response.json()
            this.item = JSON.parse(retrieved_data['Book'])
            this.ItemIndex = Object.keys(this.item['author'])[0]
            this.fetch_Messages()
        },
        async fetch_reviews() {
            let data = await fetch((this.hostname+"GetReview/" + this.ItemISBN ) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
            })
            let response = await data.json()
            this.user_reviews = response['Reviews']
        },
        async fetch_Messages() {
            let data = await fetch((this.hostname+"GetMessage/Book/" + this.ItemISBN + "/" + this.tab) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
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
            let data = await fetch((this.hostname+"GetAllTabs/Book/" + this.ItemISBN) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let response = await data.json()
            response = response['Book']
            this.all_tabs = []
            console.log("wats new scooby");
            console.log(response);
            for (let key in response) {
                this.all_tabs.push(response[key]['name'])
                console.log(response[key]['name'] + response[key]['id'] + this.tab);
                if (response[key]['name'] == this.tab)
                    this.tab_id = response[key]['id']
            }
            console.log(this.tab_id);
            this.fetch_user()
        },
        async fetch_user() {
            let data = await fetch((this.hostname+"GetTabUsers/book/" + this.tab_id) , {
                method: 'GET',
            })
            let response = await data.json()
            console.log(response);
            response = response['tab']
            console.log(response);
            this.tab_users = []
            this.tab_users = response
        },
        async fetch_tracker() {
            console.log("ello");
            console.log(this.item);
            let data  = await fetch(this.hostname+"AddToColection", {
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
                    isbn : this.ItemISBN,
                    name : this.item['title'][this.ItemIndex],
                    total_pages : this.item['pages'][this.ItemIndex],
                    user_id : this.item_owner,
                    completed : false,
                    read : 0
                })
            })
            let response = await data.json()
            
            console.log(response);
            this.tracked=response['Tracker']
        },
        async post_review() {
            
            let genres = null
            if (this.item['genre'][this.ItemIndex])
                genres = this.item['genre'][this.ItemIndex]
            console.log("bruh: " + genres);
            let data = await fetch((this.hostname+"postReview"), {
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
                    UserID: this.item_owner,
                    BookID : this.item ['isbn'][this.ItemIndex],
                    BookName :this.item['title'][this.ItemIndex],
                    total_pages : this.item['pages'][this.ItemIndex],
                    Genres : genres,
                    Ratings : this.rating,
                    Review : this.review
                })
            })
            let response = await data.json()
            console.log(response);
            if (response.View== "False")
                alert("Already Reviewed")
            else {
                
                alert("Review Posted")
                this.fetch_reviews()
            }
        },
        async post_message() {
            if (this.msg!="") 
            {
                let data = await fetch((this.hostname+"postMessage/Book"), {
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
                    BookID: this.item['isbn'][this.ItemIndex],
                    msg: this.msg,
                    total_pages : this.item['pages'][this.ItemIndex],
                    BookName: this.item['title'][this.ItemIndex],
                    tab : this.tab,  
                })
            })
            let response = await data.json()
            if (response.Passed)
                this.fetch_Messages()
            }
            this.msg = ""
        },
        async create_tab() {
            if (this.tab!="") 
            {
                let data = await fetch((this.hostname+"CreateTab"), {
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
                    medium : 'book',
                    book: this.ItemISBN,
                    name: this.new_tab,
                })
            })
            let response = await data.json()
            this.fetch_tabs()
            }
        },
        async check_tracker() {
            console.log(this.item_owner);
            let data  = await fetch( (this.hostname+"CheckCollection/" + this.item_owner + "/" + this.ItemISBN), {
                method: 'GET',
            } )
            let response = await data.json()  
            this.tracked = response['Tracker']     
            console.log(this.tracked);     
        },
        async update_tracker() {
            let data  = await fetch(this.hostname+"UpdateCollection", {
                method: 'PUT',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
                },
                body: JSON.stringify({
                    book_id : this.ItemISBN,
                    user_id : this.item_owner,
                    pages : this.pages_read,
                })
            })
            let response = await data.json()
            console.log(response);
            if (response['Updated'])
                this.check_tracker()
            else
                alert("Invalid Input")
        },
    },
} )

</script>

<template>
    <div class="p-5 text-left bg-light" style="height:100%" v-if="item">


        <div class="text-left bg-light">

            <div class="jumbotron row">

                <div class="col-md-9">

                    <h1 class="display-4">{{item['title'][ItemIndex]}}</h1>

                </div>  

                <div class="col-md-3">
                    
                    <form class="d-flex justify-content-center" style="margin-top: 2rem;" @submit.prevent="fetch_tracker" v-if="!tracked">

                        <button class="btn btn-primary p-3 text-uppercase font-weight-bold">Add To Collection</button>

                    </form>

                    <div v-else>
                        <p class="row" v-if="tracked['completed']"> Completed : Yes</p>
                        <p class="row" v-else> Completed : No</p>
                        <p class="row">
                            <p class="col-md-4" style="padding-left: 0; margin-top: 0.5rem;">Page Count : {{ tracked['read'] }} / {{ item['pages'][ItemIndex] }}</p>
                            

                            <form class="col-md-8 row" @submit.prevent="update_tracker">
                                <div class="col-md-4"><input v-model="pages_read" type="text" class="col-md-12 form-control"></div>
                                <button class="col-md-3 btn btn-secondary" style="height: 2.6rem;">Update</button>
                            </form>
                        </p>
                    </div>
                    

                </div>

                <hr class="my-4">
                <p class="lead"> Description: {{item['desc'][ItemIndex] }} </p>
            </div>
            

        </div>
           


        <div class="row">

            <div class="col-1 m-5 row"> <a :href="item['link'][ItemIndex]"> 
                <img :src="item['img'][ItemIndex]" class="img-fluid text-center" width="180" height="250"> 
            </a></div>

            <form class="col-md-3" style="margin: 2rem;" @submit.prevent="post_review">                
                    
                    <div class="form-group col"> <textarea class="form-control" rows="10" v-model="review" placeholder="Review Here"></textarea>  </div>

                    <div class="form-group row m-1">

                        <select class="form-control col m-1" v-model="rating">
                            <option>1</option>
                            <option>2</option>
                            <option>3</option>
                            <option>4</option>
                            <option>5</option>
                        </select>
                        
                        <button class="btn btn-primary col m-1" >Post</button>

                    </div>     
                
            </form>

            <div class="col-md-7" v-if="user_reviews">

                <div class="row" v-if="user_reviews.length">
    
                    <div class="col-md-1 d-flex justify-content-center" v-if="review_counter > 0"><button style="border: 0px; background: 000;" @click="review_counter--">
    
                        <img class="img-fluid" style="width: 1rem; -webkit-transform: scaleX(-1); transform: scaleX(-1); background: 000" src="../assets/Arrow.jpg">
    
                    </button></div>
    
                    <div class="col-md-1 d-flex justify-content-center" v-else><button style="border: 0px; background: 000;">
    
                        <img class="img-fluid" style="width: 1rem; -webkit-transform: scaleX(-1); transform: scaleX(-1); background: 000" src="../assets/Arrow.jpg">
    
                    </button></div>
    
    
                    <div class="col-md-8 " style="margin-left: 2rem;"> 
                        <h5 class="text-center"> {{ user_reviews[review_counter]['user']['username']  }} </h5>
                        <hr>
                        <p>{{ user_reviews[review_counter]['review'] }}</p> 
                    </div> 
    
    
                    <div class="col-md-1 d-flex justify-content-center" v-if="review_counter < user_reviews.length"><button style="border: 0px; background: 000;" @click="review_counter++">
    
                        <img class="img-fluid" style="width: 1rem; background: 000" src="../assets/Arrow.jpg">
    
                    </button></div>
    
                    <div class="col-md-1 d-flex justify-content-center" v-else><button style="border: 0px; background: 000;">
    
                        <img class="img-fluid" style="width: 1rem; background: 000;" src="../assets/Arrow.jpg">
    
                    </button></div>
                    
                </div>
                
                <div class="text-center row h-100" v-else>
                    <b class="align-self-center"> No Reviews </b> 
                </div>

            </div>

        </div>
        
        <hr>

        <div>
            <h3 style="text-decoration: underline;">Authors</h3>
            <div class="p-1" v-for="auth in item['author']">
                <router-link @click="store_item(auth)" class="nav-link" :to="{path: '/Author'}"> <h6> {{ auth }}  </h6></router-link>  
            </div>
        </div>

        <hr>


        
        <div class="mt-3" style="height: 100rem;">

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
        

                <div class="col-md-8 h-50 ">   
                    
                    <div class="border border-dark rounded" style="height: 100%;">

                        <div class="p-4 row" style="overflow: auto; overflow-x: hidden ; width: 100%;" >
            
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

    </div>

</template>


