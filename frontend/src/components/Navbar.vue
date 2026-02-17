<script lang="ts" setup>
    import useAuthStore from '@/stores/auth';
    import AuthService from '@/services/authService';
import { a } from 'vue-router/dist/index-Cu9B0wDz.mjs';


    const authStore = useAuthStore();

    const logout = async () => {
        if (authStore.loggedIn) {
            await AuthService.logout();
            authStore.setLoggedIn(false);   
            authStore.user = null;
        }
    }
</script>


<template>
    <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <router-link to="/register">Register</router-link> |
        <router-link to="/login">Login</router-link> <div v-if="authStore.user?.is_admin">|</div>
        <router-link to="/admin" v-if="authStore.user?.is_admin"> Admin</router-link>
        <div class="user-actions">
            <span v-if="authStore.loggedIn && authStore.user" class="username">
                {{ authStore.user.username }}
            </span>
            <button @click="logout" :disabled="!authStore.loggedIn">Logout</button>
        </div>
    </nav>
</template>


<style scoped>
    nav {
        display: flex;
        align-items: center;
        gap: var(--space-md);
        padding: var(--space-sm) var(--space-lg);
        background: var(--color-surface);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-card);
        font-family: var(--font-body);
        font-size: 0.9rem;
    }

    a {
        text-decoration: none;
        color: var(--color-primary);
        font-weight: 500;
        transition: color var(--transition-base);
    }

    a:hover {
        color: var(--color-accent);
    }

    button {
        margin-left: 0;
        font-family: var(--font-body);
        font-size: 0.85rem;
        font-weight: 500;
        padding: 6px 12px;
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-danger);
        background: var(--color-surface);
        color: var(--color-danger);
        cursor: pointer;
        margin-left: auto;
        transition: background var(--transition-base), color var(--transition-base), transform var(--transition-fast), box-shadow var(--transition-base);
    }

    button:hover:not(:disabled) {
        background: var(--color-danger);
        color: var(--color-surface);
        box-shadow: var(--shadow-btn);
        transform: translateY(-1px);
    }

    button:active:not(:disabled) {
        transform: translateY(0);
        box-shadow: none;
    }

    button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .user-actions {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        margin-left: auto;
    }

    .username {
        font-weight: 600;
        color: var(--color-text);
    }
</style>

