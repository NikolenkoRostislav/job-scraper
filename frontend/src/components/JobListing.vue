<script lang="ts" setup>
    import type { JobBase } from '@/types/job'

    defineProps<{
        job: JobBase
    }>()
</script>

<template>
    <li class="job-item">
        <router-link :to="`/job/${job.id}`" class="job-link">
            <div class="job-main">
                <div class="job-top">
                    <span class="job-title">{{ job.title }}</span>
                    <span class="job-arrow">→</span>
                </div>
                <div class="job-meta">
                    <span v-if="job.company" class="badge badge-company">{{ job.company }}</span>
                    <span v-if="job.location" class="badge badge-location">📍 {{ job.location }}</span>
                    <span v-else-if="job.country" class="badge badge-location">📍 {{ job.country }}</span>
                    <span
                        v-for="level in job.seniority_levels"
                        :key="level"
                        class="badge badge-seniority"
                    >
                        {{ level }}
                    </span>
                </div>
            </div>
        </router-link>
    </li>
</template>

<style scoped>
    .job-item {
        border-radius: var(--radius-md);
        transition: background var(--transition-fast);
    }

    .job-item:hover {
        background: var(--color-surface-subtle);
    }

    .job-link {
        display: block;
        padding: 12px 14px;
        text-decoration: none;
        border-radius: var(--radius-md);
    }

    .job-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: var(--space-sm);
        margin-bottom: var(--space-xs);
    }

    .job-title {
        font-size: 0.92rem;
        font-weight: 500;
        color: var(--color-text);
        transition: color var(--transition-base);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .job-arrow {
        font-size: 0.9rem;
        color: var(--color-accent);
        flex-shrink: 0;
        opacity: 0;
        transform: translateX(-4px);
        transition: opacity var(--transition-base), transform var(--transition-base);
    }

    .job-item:hover .job-title { color: var(--color-primary); }
    .job-item:hover .job-arrow { opacity: 1; transform: translateX(0); }

    .job-meta {
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-xs);
    }

    .badge {
        font-size: 0.72rem;
        font-weight: 500;
        padding: 2px 8px;
        border-radius: var(--radius-pill);
        white-space: nowrap;
    }

    .badge-company  { background: #eef2f8; color: var(--color-primary); border: 1px solid var(--color-border); }
    .badge-location { background: #f0faf5; color: #2a7a55; border: 1px solid #b6e8d0; }
    .badge-seniority { background: #fdf6ee; color: #a05a10; border: 1px solid #f5ddb6; }
    .badge-skill    { background: var(--color-surface-subtle); color: var(--color-text-muted); border: 1px solid var(--color-border-subtle); }
</style>