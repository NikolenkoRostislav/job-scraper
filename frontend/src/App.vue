<script lang="ts" setup>
  import { onMounted } from 'vue';
  import Navbar from "./components/Navbar.vue";
  import useAuthStore from '@/stores/auth';
  import useFiltersStore from '@/stores/filters';


  const filtersStore = useFiltersStore()
  const authStore = useAuthStore()
        
  onMounted(async () => {
    await authStore.checkAuth()
    if (authStore.loggedIn) {
      await filtersStore.loadSavedFilters()
    }
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
