<template>
    <footer class="site-footer">
        <p class="footer-text">© {{ year }} IT-JobScraper. All rights reserved.</p>
    </footer>
</template>

<script lang="ts" setup>
    const year = new Date().getFullYear()
</script>

<style scoped>
    .site-footer {
        width: 80%;
        margin: var(--space-lg) auto 0;
        padding: var(--space-lg) 48px;
        border-top: 1px solid var(--color-border-subtle);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .footer-text {
        font-size: 0.78rem;
        color: var(--color-text-muted);
        letter-spacing: 0.04em;
    }
</style>