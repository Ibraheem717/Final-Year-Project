<script>
import { defineComponent } from 'vue'
import {CSRFToken} from './Cookie.js'

export default defineComponent( {
    created() {
        this.get_username()
        this.fetch_profile()
    },
    props: [
        'hostname' ,
    ],
    data() {
        return {
            user : {},
            user_id: "",
            username: "",
            password: "",
            old_password : "",
            email: "",
            date_of_birth: "",
            included: false,
            recommendation: true,
            private : "",


            friends: [],

            KaggleBooks : [],
            BookStats : [],
        }
        
    },
    methods : {
        async get_username() {
            let response = await fetch(this.hostname+"ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id

            this.fetch_userbooks()
            this.GetFriend()
        },
        store_book (item) {
            localStorage.setItem('item', item)
        },
        store_user (item) {
            localStorage.setItem('user', item)
        },
        async fetch_userbooks() {
            let data = await fetch( (this.hostname+"SearchUser/" + this.user_id))
            let response = await data.json()
            
            this.KaggleBooks = response['KaggleBooks']
            this.BookStats = response['UserBooks']

            
            for (let i=0; this.KaggleBooks.length; i++) {
                console.log(this.KaggleBooks[i]);
                this.KaggleBooks[i] = JSON.parse(this.KaggleBooks[i])
                for (let key in this.KaggleBooks[i]) {
                    this.KaggleBooks[i][key] = this.KaggleBooks[i][key][Object.keys(this.KaggleBooks[i][key])[0]]
                }
            }
            console.log(this.KaggleBooks);
            
        },
        async fetch_filter_userbooks(filter) {
            let data = await fetch( (this.hostname+"SearchUser/" + this.user_id + "/" + filter))
            let response = await data.json()
            
            this.KaggleBooks = response['KaggleBooks']
            this.BookStats = response['UserBooks']

            
            for (let i=0; this.KaggleBooks.length; i++) {
                console.log(this.KaggleBooks[i]);
                this.KaggleBooks[i] = JSON.parse(this.KaggleBooks[i])
                for (let key in this.KaggleBooks[i]) {
                    this.KaggleBooks[i][key] = this.KaggleBooks[i][key][Object.keys(this.KaggleBooks[i][key])[0]]
                }
            }
            console.log(this.KaggleBooks);
            
        },
        async fetch_profile() {
            
            let response = await fetch(this.hostname+"user-profile", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer"  })
            let data = await response.json()
            this.user = data.myUser[0]
            this.recommendation = this.user['recommend']
            this.private = this.user['private']
            // this.pic = data.profile_image
            // console.log(this.pic);
            
        },
        async GetFriend() {
            console.log("called");
            let response = await fetch((this.hostname+"GetFriends/" + this.user_id), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer"  })
            let data = await response.json()
            this.friends = data['friend']

            console.log("wtf");
            console.log(this.friends);
            
        },
        async edit_profile(user_id, data_change, data_field) {
            let delet = false
            if (data_field == "recommended") {
                if (data_change == false){
                    let delet = confirm("Doing so will delete all data")
                }
            }
            if (delet == false){
                let response = await fetch(this.hostname+"user-profile", {
                    method: 'PUT',
                    headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRFToken
                    },
                    body: JSON.stringify({
                        user_id: user_id,
                        old_pass : this.old_password,
                        change : data_change,
                        field : data_field,
                    })
                })
                this.old_password = ""
                let data = await response.json()
                this.included = data.included
                if (this.included == false){
                    alert("Invalid data inputted : " + data['msg'])
                } else {
                    this.user = data.myUser
                    this.fetch_profile()
                }
            }
        },
    }
} )

</script>
<template>
    <div class="p-5 text-left bg-light" style="height:100%">
        <div class="text-left bg-light">
            <div class="jumbotron">
                <h1 class="display-4">Your Profile</h1>
                <hr class="my-4">
            </div>
        </div>

        <div class="row">

            <div class="col-md-10">

                <div class="row ">
                    <div class="col-md-4" >
                        <p class="display-6"> Username: {{ user['username'] }} </p>
                    </div>
                    <div class="col-md-8 d-flex justify-content-end" style="margin-top: 1rem;">
                        <form class="row" style="margin-right: 3rem;" @submit.prevent="edit_profile(user_id, username, 'username')" >
                            <div class="col-md-11">
                                <input class="form-control" type="text" v-model="username" placeholder="New username">
                            </div>
                            <div class="col-md-1">
                                <button class="btn btn-secondary">Edit</button>
                            </div>
                        </form>
                    </div>                
                </div>
    
                <div class="row ">
                    <div class="col-md-4" >
                        <p class="display-6">Password: *****</p>
                    </div>
                    <div class="col-md-8 d-flex justify-content-end" style="margin-top: 1rem; margin-right: 0; padding-right: 0;">
                        <form class="row" style="margin-right: 0; padding-right: 0;" @submit.prevent="edit_profile(user_id, password, 'password')" >                        
                            <div class="col-md-5">
                                <input class="form-control" type="password" v-model="old_password" placeholder="Old Password">
                            </div>
                            <div class="col-md-5">
                                <input class="form-control" type="password" v-model="password" placeholder="New Password">
                            </div>
                            <div class="col-md-1" style="padding-right: 0;">
                                <button class="btn btn-secondary">Edit</button>
                            </div>
                        </form>
                    </div>                
                </div>
    
                <div class="row ">
                    <div class="col-md-4" >
                        <p class="display-6">E-Mail: {{ user['email'] }}</p>
                    </div>
                    <div class="col-md-8 d-flex justify-content-end" style="margin-top: 1rem;">
                        <form class="row" style="margin-right: 3rem;" @submit.prevent="edit_profile(user_id, email, 'email')" >
                            <div class="col-md-11">
                                <input class="form-control" type="email" v-model="email">
                            </div>
                            <div class="col-md-1">
                                <button class="btn btn-secondary">Edit</button>
                            </div>
                        </form>
                    </div>                
                </div>
    
                <div class="row ">
                    <div class="col-md-4" >
                        <p class="display-6">Recommendation: </p>
                    </div>
                    <div class="col-md-8 d-flex justify-content-end" style="margin-top: 1rem;">
    
                        <form class="row"  @submit.prevent="edit_profile(user_id, recommendation, 'recommended')" >
                            <div class="form-check form-switch col-md-3" style="margin-right: 1rem;">
                            <input class="form-check-input" style="width: 3rem; height: 2rem;" v-model="recommendation" type="checkbox">
                                </div>
                            <div class="col-md-1">
                                <button class="btn btn-secondary">Edit</button>
                            </div>
                        </form>
                    </div>                
                </div>
    
                <div class="row ">
                    <div class="col-md-4" >
                        <p class="display-6">Private: </p>
                    </div>
                    <div class="col-md-8 d-flex justify-content-end">
                        <form class="row"  @submit.prevent="edit_profile(user_id, private, 'private')" >
                            <div class="form-check form-switch col-md-3" style="margin-right: 1rem;">
                            <input class="form-check-input" style="width: 3rem; height: 2rem;" v-model="private" type="checkbox">
                                </div>
                            <div class="col-md-1">
                                <button class="btn btn-secondary">Edit</button>
                            </div>
                        </form>
                    </div>                
                </div>
    
                <div class="row ">
                    <div class="col-md-4" >
                        <p class="display-6">Date Of Birth: {{ user['dateOfBirth'] }}</p>   
                    </div>
                    <div class="col-md-8 d-flex justify-content-end" style="margin-top: 1rem;">
                        <form class="row" style="margin-right: 1.8rem" @submit.prevent="edit_profile(user_id, date_of_birth, 'date_of_birth')" >
                            <div class="col-md-10">
                                <input class="form-control" type="date" v-model="date_of_birth">
                            </div>
                            <div class="col-md-1">
                                <button class="btn btn-secondary">Edit</button>
                            </div>
                        </form>
                    </div>                
                </div>

            </div>

            <div class="col-md-2 ">
                
                <h4 class="text-center"> <u> Friends </u> </h4>

                <div v-for="friend in friends" class="row p-2">
                    
                    <router-link @click="store_user(friend['friend']['id'])" class="nav-link text-center" :to="{path: '/OtherUser'}"> <b>{{ friend['friend']['username'] }}</b> </router-link>  
                </div>

            </div>


        </div>
        
        <hr>

        <div>

            <div class="row">

                <button class="col-md-1 m-3 btn btn-primary" @click="fetch_userbooks()">All</button>
                <button class="col-md-1 m-3 btn btn-success" @click="fetch_filter_userbooks(0)">Completed Books</button>
                <button class="col-md-1 m-3 btn btn-danger" @click="fetch_filter_userbooks(1)">Currently Reading Books</button>

            </div>


            <table class="table table-hover">

                <tr class="row mt-1">

                    <th class="align-middle col-sm-2 p-2">Book Name</th>
                    <th class="align-middle col-sm-2 p-2">Book Image</th>
                    <th class="align-middle col-sm-2 p-2">Authors</th>
                    <th class="align-middle col-sm-2 p-2">Catagories</th>
                    <th class="align-middle col-sm-2 p-2">Pages</th>
                    <th class="align-middle col-sm-2 p-2">Publish Information</th>
                    
                </tr>
                

                <tr class="mt-2 row" v-for="items in KaggleBooks" v-if="KaggleBooks">

                    <!-- {{ items }} -->

                    <td class="col-sm-2 p-2">
                        <router-link @click="store_book(items['isbn'])" class="nav-link p-0" :to="{path: '/Book'}">
                                {{items['title']}} 
                        </router-link> 
                        </td>

                    <td class="col-sm-2 p-2"> 
                        <img :src="items['img']" class="img-fluid p-0">
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
                                {{ BookStats[items['isbn']]['read'] }} / {{  items['pages'] }} Pages
                                <caption v-if="BookStats[items['isbn']]['completed']">Completed</caption>
                                <caption v-else>In Progress</caption>
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


