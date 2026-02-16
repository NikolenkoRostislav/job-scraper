<template>
    <div class="not-found-page">
        <div class="not-found-card">

            <div class="card-header">
                <p class="page-eyebrow">Error</p>
                <h1>404</h1>
            </div>

            <div class="card-body">
                <p class="not-found-message">Not Found</p>
                <p class="not-found-sub">The page you're looking for doesn't exist or has been moved.</p>
                <router-link to="/" class="btn-home">
                    ← Back to Home
                </router-link>
            </div>

        </div>
    </div>
</template>

<script lang="ts" setup></script>

<style scoped>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .not-found-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--space-3xl) var(--space-xl);
    }

    .not-found-card {
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
        font-size: 4rem;
        font-weight: 700;
        color: var(--color-surface);
        line-height: 1;
        position: relative;
        z-index: 1;
        opacity: 0.9;
    }

    .card-body {
        background: var(--color-surface);
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 36px 40px 40px;
        box-shadow: var(--shadow-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .not-found-message {
        font-family: var(--font-display);
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--color-text);
    }

    .not-found-sub {
        font-size: 0.92rem;
        line-height: 1.7;
        color: var(--color-text-muted);
        max-width: 52ch;
    }

    .btn-home {
        align-self: flex-start;
        margin-top: var(--space-sm);
        font-family: var(--font-body);
        font-size: 0.9rem;
        font-weight: 500;
        padding: 10px 22px;
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-primary);
        background: transparent;
        color: var(--color-primary);
        text-decoration: none;
        letter-spacing: 0.03em;
        transition:
            background var(--transition-base),
            color var(--transition-base),
            transform var(--transition-fast),
            box-shadow var(--transition-base);
    }

    .btn-home:hover {
        background: var(--color-primary);
        color: var(--color-surface);
        box-shadow: var(--shadow-btn);
        transform: translateY(-1px);
    }

    .btn-home:active {
        transform: translateY(0);
        box-shadow: none;
    }
</style>