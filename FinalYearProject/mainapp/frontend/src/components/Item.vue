<script lang="ts">
import { objectToString } from '@vue/shared'
import { json } from 'stream/consumers'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent( {
    created() {
        this.get_owner_id()
        this.get_item()
        this.get_auction_item()
        this.get_current_user()
    },
    data() {
        return {
            item : "",
            item_owner :  0,

            questions : [{question_id: 0, question_text: "", answer: "", user_id: "", answered: false, item_id: 0}],
            temp : {},
            item_data : {
                'Title' : "",
                'Item Picture' : "",
                'Description' : "",
                'Starting Price' : "",
                'Current Price' : "",
                'Auction End': "",
                'Owner' : ""
            },

            answer: this.answer,
            question: this.question,
            answered: this.answered,
            pending_question: "",
            current_user_id: "",
            bidded : true,
            new_bid : 0
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
        async get_auction_item() {
            let response = await fetch(("http://localhost:8000/get-item/" + this.item) , {
                method: "GET", 
                credentials: "include", 
                mode: "cors", 
                referrerPolicy: "no-referrer", 
            })
            let retrieved_data = await response.json()
            console.log(retrieved_data);
            this.item_data = retrieved_data.return_item
            
        },

        async bid(bid:number, item_id : number) {
        let data = await fetch("http://localhost:8000/bid", {
                method: 'PUT', credentials: "include", mode: "cors", referrerPolicy: "no-referrer",
                body: JSON.stringify({
                    item_owner : this.item_owner,
                    ID : item_id,
                    new_bid : bid,
                })
            })
            let response = await data.json()
            this.bidded = response.success
            console.log(this.bidded)
            if (this.bidded != true)
                alert("Invalid Bid")
            else 
                this.get_auction_item()
       }, 

        async fetch_question() {
            let response = await fetch(("http://localhost:8000/get-questions/" + this.item) , {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            })
            let data = await response.json()
            this.questions = data.questions
        },
        async ask_question() {
            let response = await fetch("http://localhost:8000/questions", {
                method: 'POST',
                body: JSON.stringify({
                    question: this.pending_question,
                    item_id: this.item,
                    user_id: this.item_owner,
                })
            })
            this.fetch_question()
        },
        async answer_question(question_id: Number, answer: String, answered: Boolean) {
            let response = await fetch("http://localhost:8000/questions", {
                method: 'PUT',
                body: JSON.stringify({
                    'question_id': question_id,
                    'user_id': this.item_owner,
                    'answer': answer,
                    'answered': answered,
                    'current_user_id': this.current_user_id,
                }) 
            })
            let data = await response.json()
            this.question = data.question
            this.fetch_question()
        },
        async get_current_user() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.current_user_id = data.user_id
            this.fetch_question()
        },
    },
} )

</script>

<template>
    <div class="p-5 text-left bg-light" style="height:100%">
        <div class="text-left bg-light">
            <div class="jumbotron">
                <h1 class="display-4">{{item_data['Title']}}</h1>
                <hr class="my-4">
                <p class="lead"> Description: {{item_data ['Description'] }} </p>
            </div>
        </div>
        <div class="row ">
                <div class="col "><img :src="'http://localhost:8000' + item_data['Item Picture']" alt="http://localhost:8000/mainapp/media/defaultIcon.jpg" class="img-fluid"> </div>
                <div class="col-8">
                    <table class="table">
                        <tr>
                            <th>Starting Price:</th>
                            <th>Current Bid:</th>
                            <th></th>
                            <th>Auction End:</th>
                        </tr>
                        <tr>
                            <td>£{{ item_data ['Starting Price'] }}</td>
                            <td>£{{ item_data ['Current Price'] }}</td>
                            <td>
                                <form @submit.prevent="bid(new_bid, parseInt(item))">
                                    <div class="row justify-content-between g-3">

                                        <div class="col-auto">
                                            <input type="number" name="bid" v-model="new_bid" class="form-control">
                                        </div>
                                        <div class="col-auto">
                                            <button class="btn btn-primary">Raise</button>
                                        </div>
                                    </div>
                                </form>
                            </td>
                            <td>{{ item_data ['Auction End'] }}</td>
                        </tr>  
                    </table>
                </div>
            </div>


    <form @submit.prevent="ask_question">
        <p>Question: </p>
        <input class="form-control" type="text" v-model="pending_question">
        <button>Ask</button>
    </form>


    <div v-for="item_question in questions" :key="item_question.question_id">
        <p>Question: {{ item_question.question_text }}</p>
        <div v-if="item_question.answered == true">
            <p>Answer: {{ item_question.answer }}</p>
        </div>
        <div v-else>
            <div v-if="item_question.user_id == current_user_id">
                <form @submit.prevent="answer_question(item_question.question_id, item_question.answer, item_question.answered)">
                    <p>Answer: </p>
                    <input class="form-control" type="text" v-model="item_question.answer">
                    <button>Answer</button>
                </form>
            </div>
            <div v-else>
                <p>{{ current_user_id }}</p>
            </div>
        </div>
    </div>

    </div>

</template>


