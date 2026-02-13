<script lang="ts" setup>
    import { ref } from "vue";

    import api from '@/services/api'
    import AuthService from '@/services/authService';

    const token = ref()
    const username = ref()
    const password = ref()
    const error = ref()

    async function login(username: string, password: string) {
        try {
            token.value = await AuthService.login(username, password)
            error.value = ""
        }
        catch (err) {
            error.value = err
        }
    }

    const user = ref()
    async function testLogin() {
        try {
            user.value = (await api.get("/user/me")).data
            error.value = ""
        }
        catch (err) {
            error.value = err
        }
    }
</script>

<template>
    <h1>Login</h1>
    <input v-model="username" placeholder="Username" />
    <input type="password" v-model="password" placeholder="Password" />
    <button @click='login(username, password)' v-if="username && password">Login button</button>
    <p v-if="error">{{ error }}</p>
    <p v-if="token">You are logged in!</p>
    <button @click='testLogin'>Try get user info button</button>
    <p>{{ user }}</p>
</template>

<style scoped>
</style>
