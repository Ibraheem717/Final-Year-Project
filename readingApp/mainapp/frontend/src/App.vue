<template>
    <nav class="navbar navbar-expand-lg bg-dark">

      <a class="navbar-brand p-4" href="#"><h1 class="text-white">Reading App</h1></a>

      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse">

        <ul class="nav nav-pills p-3 ml-5 mr-5">

            <li class="nav-item">
              <router-link class="nav-link text-white" href="#" to="/Search">Books</router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link text-white" href="#" to="/Profile">Profile</router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link text-white" href="#" to="/Forums">Forums</router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link text-white" href="#" to="/Recommendation">Recommendation</router-link>
            </li>

            <li class="nav-item">
              <a class="nav-link text-white" href="http://localhost:8000/logout" >Logout</a>
            </li>
          </ul>

        </div>

      </nav>

    <router-view></router-view>
</template>


