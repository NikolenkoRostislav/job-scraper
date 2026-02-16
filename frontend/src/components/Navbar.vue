<script lang="ts" setup>
    import useAuthStore from '@/stores/auth';
    import AuthService from '@/services/authService';


    const authStore = useAuthStore();

    const logout = async () => {
        if (authStore.loggedIn) {
            await AuthService.logout();
            authStore.setLoggedIn(false);   
        }
    }
</script>


<template>
    <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <router-link to="/register">Register</router-link> |
        <router-link to="/login">Login</router-link> 
        <button @click="logout" :disabled="!authStore.loggedIn">Logout</button>
    </nav>
</template>


<style scoped>
    nav {
        margin-bottom: 1rem;
    }
    a {
        text-decoration: none;
    }
</style>
