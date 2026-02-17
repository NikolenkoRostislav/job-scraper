<script lang="ts" setup>
    import { ref } from "vue";

    import AuthService from '@/services/authService';
    import useAuthStore from '@/stores/auth';
    import GoogleLogin from "@/components/GoogleLogin.vue";


    const authStore = useAuthStore();

    const token = ref()
    const username = ref()
    const password = ref()
    const error = ref()

    async function login(username: string, password: string) {
        try {
            token.value = await AuthService.login(username, password)
            error.value = ""
            authStore.setLoggedIn(true);
            authStore.checkAuth();
        }
        catch (err) {
            error.value = err
        }
    }
</script>

<template>
    <div class="login-page">
        <div class="login-card">

            <div class="card-header">
                <p class="page-eyebrow">Welcome back</p>
                <h1>Login</h1>
            </div>

            <div class="card-body">

                <div class="form-group">
                    <label for="username">Username</label>
                    <input id="username" v-model="username" placeholder="Enter your username" autocomplete="username" />
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input id="password" type="password" v-model="password" placeholder="Enter your password" autocomplete="current-password" />
                </div>

                <p v-if="error" class="error-message">{{ error }}</p>

                <div class="actions">
                    <button
                        class="btn-primary"
                        @click="login(username, password)"
                        :disabled="!(username && password)"
                    >
                        Login
                    </button>

                    <div class="divider-row">
                        <span class="divider-line"></span>
                        <span class="divider-label">or</span>
                        <span class="divider-line"></span>
                    </div>

                    <GoogleLogin />
                </div>

                <div v-if="token" class="success-message">
                    <span class="success-icon">✓</span>
                    You are logged in!
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .login-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--space-3xl) var(--space-xl);
    }

    .login-card {
        width: 100%;
        max-width: 440px;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .card-header {
        background: linear-gradient(
            135deg,
            var(--color-primary) 0%,
            var(--color-primary-mid) 60%,
            var(--color-primary-deep) 100%
        );
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        padding: 36px 40px 32px;
        position: relative;
        overflow: hidden;
    }

    .card-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 180px; height: 180px;
        border-radius: 50%;
        background: rgba(255,255,255,0.04);
    }

    .card-header::after {
        content: '';
        position: absolute;
        bottom: -20px; left: 20%;
        width: 260px; height: 100px;
        border-radius: 50%;
        background: rgba(255,255,255,0.025);
    }

    .page-eyebrow {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--color-accent);
        margin-bottom: var(--space-sm);
        position: relative;
        z-index: 1;
    }

    .card-header h1 {
        font-family: var(--font-display);
        font-size: 2rem;
        font-weight: 700;
        color: var(--color-surface);
        line-height: 1.2;
        position: relative;
        z-index: 1;
    }

    .card-body {
        background: var(--color-surface);
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 36px 40px 40px;
        box-shadow: var(--shadow-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-lg);
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .form-group label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
    }

    .form-group input {
        font-family: var(--font-body);
        font-size: 0.92rem;
        color: var(--color-text);
        background: var(--color-surface-subtle);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-sm);
        padding: 11px 14px;
        outline: none;
        transition: border-color var(--transition-base), box-shadow var(--transition-base);
    }

    .form-group input::placeholder {
        color: var(--color-text-muted);
        opacity: 0.7;
    }

    .form-group input:focus {
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(26, 42, 74, 0.08);
    }

    .actions {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .btn-primary {
        width: 100%;
        font-family: var(--font-body);
        font-size: 0.92rem;
        font-weight: 500;
        padding: 12px;
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-primary);
        background: var(--color-primary);
        color: var(--color-surface);
        cursor: pointer;
        letter-spacing: 0.03em;
        transition:
            background var(--transition-base),
            border-color var(--transition-base),
            transform var(--transition-fast),
            box-shadow var(--transition-base);
    }

    .btn-primary:hover:not(:disabled) {
        background: var(--color-primary-deep);
        border-color: var(--color-primary-deep);
        box-shadow: var(--shadow-btn);
        transform: translateY(-1px);
    }

    .btn-primary:active:not(:disabled) {
        transform: translateY(0);
        box-shadow: none;
    }

    .btn-primary:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .divider-row {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }

    .divider-line {
        flex: 1;
        height: 1px;
        background: var(--color-border-subtle);
    }

    .divider-label {
        font-size: 0.78rem;
        color: var(--color-text-muted);
        letter-spacing: 0.06em;
    }

    .success-message {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: 12px 16px;
        background: #f0faf5;
        border: 1px solid #b6e8d0;
        border-radius: var(--radius-sm);
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--color-success);
    }

    .success-icon {
        font-size: 1rem;
    }

    .error-message {
        font-size: 0.85rem;
        color: var(--color-danger);
        padding: 10px 14px;
        background: #fdf2f2;
        border: 1px solid #f5c6c6;
        border-radius: var(--radius-sm);
    }
</style>