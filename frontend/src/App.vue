<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/register">Register</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/settings">Settings</router-link> |
      <router-link to="/skills">Skills</router-link> |
      <router-link to="/job/1">Job Example 1</router-link> |
      <router-link to="/job/888">Job Example 888</router-link> |
      <router-link to="/sources">Sources</router-link>
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
