<script lang="ts">
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent( {
    created() {
        this.get_username()
        this.fetch_profile()
    },
    data() {
        return {
            user_id: "",
            user: [{username: "", email: "", date_of_birth: "", city: "", image: ""}],
            username: "",
            email: "",
            date_of_birth: "",
            city: "",
            edits: [{username: "", email: "", date_of_birth: "", city:""}],
            included: false,
            pic: "",
        }
        
    },
    methods : {
        async get_username() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },
        async fetch_profile() {
            let response = await fetch("http://localhost:8000/user-profile", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer"  })
            let data = await response.json()
            this.user = data.myUser
            console.log(this.user[0].image);
            
            // this.pic = data.profile_image
            // console.log(this.pic);
            
        },
        async edit_profile(user_id: any, username: any, email: any, city:any , date_of_birth: any) {
            let response = await fetch("http://localhost:8000/user-profile", {
                method: 'PUT',
                body: JSON.stringify({
                    user_id: user_id,
                    username: username,
                    email: email,
                    city: city,
                    date_of_birth: date_of_birth,
                })
            })
            let data = await response.json()
            this.included = data.included
            console.log(this.included)
            if (this.included == true){
                alert("Username already exists")
            } else {
                this.user = data.myUser
                this.fetch_profile()
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
        <div class="row justify-content-between g-3">
            <div class="col-auto">
                <img :src="'http://localhost:8000' + user[0].image" class="img-thumbnail w-25 ">
            </div>
            <div class="col-auto">
                <form :action="'http://localhost:8000/submit-user-image/' + user_id" method="POST" enctype="multipart/form-data">
                    <label for="formFile">Update Profile Picture</label>
                    <div class="mb-3">
                        <input class="form-control " type="file" id="formFile">
                    </div>
                <input type="submit" class="btn btn-secondary" value="Update Picture">
            </form>
            </div>
        </div>
        <div v-for="info in user">
            <div v-for="edit in edits">
                <form @submit.prevent="edit_profile(user_id, edit.username, info.email, info.city, info.date_of_birth)">
                    <div class="row justify-content-between g-3">
                        <div class="col-auto">
                            <p>Username: {{ info.username }}</p>
                        </div>
                        <div class="col-auto">
                            <div class="row align-items-center g-3">
                                <div class="col-auto">
                                    <input class="form-control" type="text" v-model="edit.username">
                                </div>
                                <div class="col-auto">
                                    <button class="btn btn-secondary">Edit</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                
                <form @submit.prevent="edit_profile(user_id, info.username, edit.email, info.city, info.date_of_birth)">
                    <div class="row justify-content-between g-3">
                        <div class="col-auto">
                            <p>Email: {{ info.email }}</p>
                        </div>
                        <div class="col-auto">
                            <div class="row align-items-center g-3">
                                <div class="col-auto">
                                    <input class="form-control" type="email" v-model="edit.email">
                                </div>
                                <div class="col-auto">
                                    <button class="btn btn-secondary">Edit</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <form @submit.prevent="edit_profile(user_id, info.username, info.email, edit.city, info.date_of_birth)">
                    <div class="row justify-content-between g-3">
                        <div class="col-auto">
                            <p>City: {{ info.city }}</p>
                        </div>
                        <div class="col-auto">
                            <div class="row align-items-center g-3">
                                <div class="col-auto">
                                    <input class="form-control" type="text" v-model="edit.city">
                                </div>
                                <div class="col-auto">
                                    <button class="btn btn-secondary">Edit</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <form @submit.prevent="edit_profile(user_id, info.username, info.email, info.city, edit.date_of_birth)">
                    <div class="row justify-content-between g-3">
                        <div class="col-auto">
                            <p>Date of birth: {{ info.date_of_birth }}</p>
                        </div>
                        <div class="col-auto">
                            <div class="row align-items-center g-3">
                                <div class="col-auto">
                                    <input class="form-control" type="date" v-model="edit.date_of_birth">
                                </div>
                                <div class="col-auto">
                                    <button class="btn btn-secondary">Edit</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>  
            </div>           
        </div>
    </div>
</template>


