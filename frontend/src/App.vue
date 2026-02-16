<script lang="ts" setup>
  import { onMounted } from 'vue';
  import Navbar from "./components/Navbar.vue";
  import useAuthStore from '@/stores/auth';

  const authStore = useAuthStore()

  onMounted(() => {
    authStore.checkAuth()
  })
</script>


<template>
  <div>
    <Navbar />
    <router-view />
  </div>
</template>


<style scoped>
</style>
