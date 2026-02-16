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
</style>

