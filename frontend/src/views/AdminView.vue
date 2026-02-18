<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    import useAuthStore from '@/stores/auth';

    
    const authStore = useAuthStore();
</script>


<template>
    <div class="about-page">
        <div class="page-header">
            <p class="page-eyebrow">Dashboard</p>
            <h1>Admin</h1>
        </div>
        <template v-if="authStore.user?.is_admin">
            <div class="page-body">
                <p class="body-text">Welcome to the admin dashboard! Here you can view analytics and perform administrative tasks.</p>
            </div>
        </template>
        <template v-else>
            <div class="page-body">
                <p class="body-text">Nice try<span v-if="authStore.user">{{`, ${authStore.user.username}` }}</span>! You don't have admin privileges.</p>
            </div>
        </template>
    </div>
</template>


<style scoped>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .about-page {
        width: 80%;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .page-header {
        background: linear-gradient(
            135deg,
            var(--color-primary) 0%,
            var(--color-primary-mid) 60%,
            var(--color-primary-deep) 100%
        );
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        padding: 40px 48px 36px;
        position: relative;
        overflow: hidden;
    }

    .page-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.04);
    }

    .page-header::after {
        content: '';
        position: absolute;
        bottom: -20px; left: 30%;
        width: 320px; height: 120px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.025);
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

    .page-header h1 {
        font-family: var(--font-display);
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--color-surface);
        line-height: 1.2;
        position: relative;
        z-index: 1;
    }

    .page-body {
        background: var(--color-surface);
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 40px 48px 48px;
        box-shadow: var(--shadow-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-3xl);
    }

    .section-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
        margin-bottom: var(--space-lg);
    }

    .subsection-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
        margin-bottom: var(--space-md);
    }

    .body-text {
        font-size: 0.95rem;
        line-height: 1.75;
        color: var(--color-text-body);
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, var(--color-border-subtle) 0%, transparent 100%);
        border: none;
    }

    .divider-inner {
        height: 1px;
        background: var(--color-border-subtle);
        border: none;
        margin: var(--space-xl) 0;
    }

    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-lg);
    }

    .stat-block {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
        padding: 18px 24px;
        background: var(--color-surface-subtle);
        border-radius: var(--radius-md);
        border-left: 3px solid var(--color-primary);
        transition: box-shadow var(--transition-base), transform var(--transition-base);
    }

    .stat-block:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }
</style>