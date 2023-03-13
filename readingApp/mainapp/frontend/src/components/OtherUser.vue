<script>
import { defineComponent } from 'vue'
import { CSRFToken } from './Cookie.js'

export default defineComponent( {
    created() {
        this.get_item()
        this.GetMyUser()
        this.fetch_foreign_user()
        this.CheckFriends()
        this.GetFriend()
    },
    data() {
        return {
            my_user_id : 0,
            user : {},
            user_id: "",
            username: "",
            password: "",
            old_password : "",
            email: "",
            date_of_birth: "",

            friends : [],

            included: false,
            recommendation: true,
            private : "",

            KaggleBooks : [],
            BookStats : [],
        }
        
    },
    methods : {
        async GetMyUser() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.my_user_id = data.user_id
            
        },
        async GetFriend() {
            console.log("called");
            let response = await fetch(("http://localhost:8000/GetFriends/" + this.user_id), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer"  })
            let data = await response.json()
            this.friends = data['friend']

            // this.pic = data.profile_image
            // console.log(this.pic);
            
        },
        async CheckFriends() {
            let data = await fetch(("http://localhost:8000/CheckFriends/" + this.my_user_id +"/"+ this.user_id), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer"  ,
            })
            let response = await data.json()

            this.included = response['followed']

            // this.pic = data.profile_image
            // console.log(this.pic);
            
        },
        async AddFriend() {
            let response = await fetch(("http://localhost:8000/AddFriends"), {method: "POST", credentials: "include", mode: "cors", referrerPolicy: "no-referrer"  ,
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({
                user : this.my_user_id,
                friend : this.user_id
                })
            })
            let data = await response.json()
            this.CheckFriends()
            // this.pic = data.profile_image
            // console.log(this.pic);
            
        },
        get_item() {
            let get_user = localStorage.getItem('user')
            if (get_user)
                this.user_id = get_user
            
        },
        async fetch_userbooks() {
            let data = await fetch( ("http://localhost:8000/SearchUser/" + this.user_id))
            let response = await data.json()
            
            this.KaggleBooks = response['KaggleBooks']
            this.BookStats = response['UserBooks']

            for (let i=0; this.KaggleBooks.length; i++) {
                this.KaggleBooks[i] = JSON.parse(this.KaggleBooks[i])
                for (let key in this.KaggleBooks[i]) [
                    this.KaggleBooks[i][key] = this.KaggleBooks[i][key][Object.keys(this.KaggleBooks[i][key])[0]]
                ]
            }
            console.log("this is kaggle");
            console.log(this.BookStats);
        },
        async fetch_foreign_user() {            
            let data = await fetch(("http://localhost:8000/GetForeignUser/" + this.user_id), {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer"  })
            let response = await data.json()
            console.log(response);
            this.private = response['private']
            if (response['private'] == false) {
                this.user = response['user']
                if (response['recommend']) {
                    this.fetch_userbooks()
                }
            }
        },

    }
} )

</script>
<template>
    <div class="p-5 bg-light" style="height:100%">


        <div class="bg-light d-flex">

            <div class="p-2">
                <h1 class="display-4">Profile</h1>
                
            </div>

            <div class="ms-auto p-2 d-flex align-content-center flex-wrap" v-if="!included">
                <button @click="AddFriend" class="btn btn-primary">Add Friend</button>
            </div>

            <div v-else>
                Already Following
            </div>


        </div>

        <hr class="my-4">

        <div v-if="private == false">

            <div class="row">

                <div class="col-md-10">

                    <div class="row ">
                        <div class="col-md-4" >
                            <p class="display-6"> Username: {{ user['name'] }} </p>
                        </div>             
                    </div>
            
                    <div class="row ">
                        <div class="col-md-4" >
                            <p class="display-6">E-Mail: {{ user['email'] }}</p>
                        </div>          
                    </div>
            
                    <div class="row ">
                        <div class="col-md-4" >
                            <p class="display-6">Date Of Birth: {{ user['dateofbirth'] }}</p>
                        </div>    
                    </div>

                </div>

                <div class="col-md-2 ">
                
                    <h4 class="text-center"> <u> Friends </u> </h4>

                    <div v-for="friend in friends" class="row p-2">
                        
                        <router-link @click="store_item(friend['friend']['username'])" class="nav-link text-center" :to="{path: '/OtherUser'}"> <b>{{ friend['friend']['username'] }}</b> </router-link> 

                    </div>

                </div>

            </div>
    
    
    
            <div v-if="BookStats.length">
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
                            <router-link @click="store_item(items['isbn'])" class="nav-link p-0" :to="{path: '/Book'}">
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


            
        
            <div v-else>

                <hr>
                <h1> No books Recorded </h1>

            </div>


        </div>

        <div v-else>

            <h1> This account is private </h1>

        </div>
        
            

    </div>           

</template>


