 <script>
import { defineComponent } from 'vue'

export default defineComponent( {
    created() {
        this.get_owner_id()
        this.GetForums()
    },
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
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id
        },
       async GetForums ( ) {
        let data = await fetch("http://localhost:8000/GetForums", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
        let response = await data.json()
        this.AllForums = response['Forums']
        console.log(response);
       },
       async CreateForum() {
        let data = await fetch("http://localhost:8000/CreateForum", 
        {   method: 'POST',
            headers : {'Content-Type':'application/json'},
            body: JSON.stringify({
                Name : this.Name
            })
        })
        let reponse = await data.json()
       },
        store_item (item) {
            localStorage.setItem('forum', item)
       },
    },
} )

</script>

<template>

    <form @submit.prevent="GetForums"><button>Click me</button></form>

    <form @submit.prevent="CreateForum"><input type="text" v-model="Name"><button>Click This</button></form>

    <div v-for="forum in AllForums">

        <td class="row p-5"> 

            <router-link @click="store_item(forum['id'])" class="nav-link col-3 p-5 " :to="{path: '/ForumPage'}"> 

                <div class="row">
                    <div class=" col-4 font-weight-bold" style="size: 1000rem;">
                        {{ forum['Name'] }}
                    </div>  

                    <div class="col-4">
                        NumberOfMessages : {{ forum['NumberOfMessages'] }}
                    </div>

                    <div class="col-4">
                        NumberOfUsers : {{ forum['NumberOfUsers'] }}
                    </div>

                </div>



            </router-link>  

        </td>

    </div>

</template>


