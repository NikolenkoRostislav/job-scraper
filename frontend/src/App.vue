<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/register">Register</router-link> |
      <router-link to="/login">Login</router-link> 
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts" setup></script>

<style scoped>
nav {
  margin-bottom: 1rem;
}
a {
  text-decoration: none;
}
</style>
