<script lang="ts" setup>
import { ref } from "vue";
import AuthService from "@/services/authService";
import UserService from "@/services/userService";

const email = ref("");
const username = ref("");
const password = ref("");
const code = ref<number | null>(null);
const codeSent = ref(false);
const error = ref("");
const success = ref("");

async function sendCode() {
    if (!email.value || !username.value || !password.value) {
        error.value = "Please fill in all fields";
        return;
    }

    try {
        await AuthService.sendEmailCode(email.value);
        codeSent.value = true;
        error.value = "";
    } catch (err: any) {
        error.value = err.message || "Failed to send code";
    }
}

async function register() {
    try {
        if (!code.value) {
            error.value = "Enter the code first!";
            return;
        }

        await UserService.register(
            { email: email.value, username: username.value, password: password.value },
            code.value
        );
        success.value = "Registered successfully!";
        error.value = "";

        email.value = "";
        username.value = "";
        password.value = "";
        code.value = null;
        codeSent.value = false;

        window.location.href = "/login";
    } catch (err: any) {
        error.value = err.message || "Registration failed";
    }
}
</script>


<template>
    <h1>Register</h1>

    <div v-if="!codeSent">
        <input v-model="email" placeholder="Email" />
        <input v-model="username" placeholder="Username" />
        <input type="password" v-model="password" placeholder="Password" />
        <button @click="sendCode" :disabled="!email || !username || !password">Register</button>
    </div>

    <div v-else>
        <input type="number" v-model.number="code" placeholder="Enter code" />
        <button @click="register" :disabled="!code">Confirm Code</button>
    </div>

    <p v-if="error" style="color: red;">{{ error }}</p>
    <p v-if="success" style="color: green;">{{ success }}</p>
</template>


<style scoped>
</style>
