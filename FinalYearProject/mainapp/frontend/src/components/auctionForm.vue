<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent( {
    created() {
        this.get_owner_id()
    },
    data() {
        return {
            title : "",
            description : "",
            starting_price : 0,
            current_price : "",
            item_picture : "",
            auction_finish : "",
            item_owner : ""
        }
        
    },
    methods : {
        async get_owner_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.item_owner = data.user_id
        },
    }
} )

</script>

<template>
    <div class="p-5 text-left bg-light" style="height:100%">
        <div class="text-left bg-light">
            <div class="jumbotron">
                <h1 class="display-4">Add an Item</h1>
                <hr class="my-4">
            </div>
        </div>

        <div class="row">
            <div class="col"></div>
            <div class="col">
                <form :action="'http://localhost:8000/submit-item/' + item_owner" method="POST" enctype="multipart/form-data">

                    <label>Title: </label>
                    <input class="form-control" type="text" name="title">

                    <label>Description: </label>
                    <input class="form-control" type="text" name="description">

                    <label>Starting: </label>
                    <input class="form-control" type="number" name="starting_price">

                    <label>Auction Finish: </label>
                    <input class="form-control" type="datetime-local" name="auction_finish"><br>

                    <div class="mb-3">
                        <input class="form-control " type="file" name = "my_image">
                    </div>
                    <button class="btn btn-primary">Submit</button>
                </form>
            </div>
            <div class="col">
            </div>
        </div>
    </div>

 

</template>


