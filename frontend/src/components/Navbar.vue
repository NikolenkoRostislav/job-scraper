<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    import isLoggedIn from '@/utils/loginChecker';
    import AuthService from '@/services/authService';

    const loggedIn = ref(false);

    const logout = async () => {
        if (await isLoggedIn()){
            await AuthService.logout();
            loggedIn.value = false;
        }
    }

    onMounted(async () => {
        loggedIn.value = await isLoggedIn();
    });
</script>


<template>
    <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <router-link to="/register">Register</router-link> |
        <router-link to="/login">Login</router-link> 
        <button @click="logout" :disabled="!loggedIn">Logout</button>
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
