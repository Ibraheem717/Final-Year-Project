<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent( {
    created() {
        this.get_item()
        this.get_owner_id()
        this.get_auction_item()
        this.fetch_Messages()
    },
    data() {
        return {
            item : "",
            item_owner :  0,
            ItemIndex : 0,

            rating : 0,
            review : "",

            all_messages : [],
            msg: "",
            LastUser : 0,
        }
    },   
    methods : {
        async get_owner_id() {
            let response = await fetch(("http://localhost:8000/ses-user"), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.item_owner = data.user_id
        },
        get_item() {
            let get_item = localStorage.getItem('item')
            if (get_item)
                this.item = get_item
            
        },
        async store_item (item) {
            localStorage.setItem('author', item)
        },
        async get_auction_item() {
            let response = await fetch(("http://localhost:8000/Search/" + this.item) , {
                method: "GET",  
            })
            let retrieved_data = await response.json()
            console.log(retrieved_data);
            this.item = JSON.parse(retrieved_data['Book'])
            this.ItemIndex = Object.keys(this.item['author'])[0]
            console.log(this.item);
            console.log("I dnt wnna go restaurant : " + this.item);
            this.fetch_Messages()
        },
        async fetch_Messages() {
            let data = await fetch(("http://localhost:8000/GetMessage/Book/" + this.item['isbn'][this.ItemIndex] ) , {
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
                console.log(LU);
                console.log(this.all_messages[i]['UserID']);
                if (LU == this.all_messages[i]['UserID']) {
                    console.log('hellp');
                    this.all_messages[i]['UserID'] = -1
                }
                    
                else
                LU = this.all_messages[i]['UserID']
            }
            console.log("Time to go : " );
            console.log(this.all_messages);
             
            
        },
        async post_review() {
            
            let genres = null
            if (this.item['genre'][this.ItemIndex])
                genres = this.item['genre'][this.ItemIndex]
            console.log("bruh: " + genres);
            let data = await fetch(("http://localhost:8000/postReview"), {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                body: JSON.stringify({
                    UserID: this.item_owner,
                    BookID : this.item ['isbn'][this.ItemIndex],
                    BookName :this.item['title'][this.ItemIndex],
                    Genres : genres,
                    Ratings : this.rating,
                    Review : this.review
                })
            })
            let response = await data.json()
            console.log(response);
            if (response.View.length > 0)
                alert("Review Posted")
            else
                alert("Already Reviewed")
        },
        async post_message() {
            if (this.msg!="") 
            {
                let data = await fetch(("http://localhost:8000/postMessage/Book"), {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                body: JSON.stringify({
                    BookID: this.item['isbn'][this.ItemIndex],
                    msg: this.msg,
                    BookName: this.item['title'][this.ItemIndex]
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
                <h1 class="display-4">{{item['title'][ItemIndex]}}</h1>
                <hr class="my-4">
                <p class="lead"> Description: {{item['desc'][ItemIndex] }} </p>
            </div>
        </div>


           


        <div class="row">

            <div class="col-1"> <a :href="item['link'][ItemIndex]"> <img :src="item['img'][ItemIndex]" class="img-fluid"> </a></div>

            <form class="col-md-3" @submit.prevent="post_review">
                
                    
                    <div class="form-group col"> <textarea class="form-control" rows="5" v-model="review" placeholder="Review Here"></textarea>  </div>

                    <div class="form-group row m-1">

                        <select class="form-control col m-1" v-model="rating">
                            <option >1</option>
                            <option >2</option>
                            <option >3</option>
                            <option >4</option>
                            <option >5</option>
                        </select>
                        
                        <button class="btn btn-primary col m-1" >Post</button>

                    </div>

                    
                   
                
            </form>
        </div>

        <hr>

        <div>
            <h3>Authors</h3>
            <div class="p-1" v-for="auth in item['author']">
                <router-link @click="store_item(auth)" class="nav-link" :to="{path: '/Author'}"> <h6> {{ auth }}  </h6></router-link>  
            </div>
        </div>

        <hr>


        <div>
            <h3>Chat</h3>
            <div>
                
                <table class="table m-3">

                    <tr v-for="messages in all_messages">


                        <th v-if="messages['UserID'] != -1" class="row">
                            {{ messages["UserID"] }}
                        </th>

                        <th class="row" style="font-weight: normal;"> {{ messages["Message"] }} </th>


                        
                        <!-- <div v-else class="d-flex justify-content-end">

                            <th v-if="messages['UserID'] != -1" class="row">
                                {{ messages["UserID"] }}
                            </th>
    
                            <th class="row" style="font-weight: normal;">{{ messages["Message"] }}</th>

                        </div> -->

                    </tr>

                </table>
            </div>
            <div>
                <form class="row" @submit.prevent="post_message">

                    <div class="col-md-11"><input class="form-control" type="text" v-model="msg"></div>
                    
                    <button class="col-md-1 btn btn-primary">Post</button>

                </form>
            </div>
        </div> 

    </div>

</template>


