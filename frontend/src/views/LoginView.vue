<script lang="ts" setup>
    import { ref } from "vue";

    import AuthService from '@/services/authService';
    import useAuthStore from '@/stores/auth';


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
        }
        catch (err) {
            error.value = err
        }
    }

    async function googleLogin() {
        await AuthService.googleLogin()
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

                    <button class="btn-google" @click="googleLogin">
                        <svg class="google-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                        </svg>
                        Continue with Google
                    </button>
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

    .btn-google {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--space-sm);
        font-family: var(--font-body);
        font-size: 0.92rem;
        font-weight: 500;
        padding: 11px;
        border-radius: var(--radius-sm);
        border: 1px solid var(--color-border);
        background: var(--color-surface);
        color: var(--color-text);
        cursor: pointer;
        letter-spacing: 0.02em;
        transition:
            background var(--transition-base),
            border-color var(--transition-base),
            box-shadow var(--transition-base),
            transform var(--transition-fast);
    }

    .btn-google:hover {
        background: var(--color-surface-subtle);
        border-color: var(--color-border);
        box-shadow: var(--shadow-hover);
        transform: translateY(-1px);
    }

    .btn-google:active {
        transform: translateY(0);
        box-shadow: none;
    }

    .google-icon {
        width: 18px;
        height: 18px;
        flex-shrink: 0;
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