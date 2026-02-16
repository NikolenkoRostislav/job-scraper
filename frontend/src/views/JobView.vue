<script lang="ts" setup>
    import { ref, watchEffect, computed } from 'vue';
    import { useRoute } from 'vue-router';

    import JobService from '@/services/jobService';
    import FavoritedJobService from '@/services/favoriteJobService';
    import useAuthStore from '@/stores/auth';
    import type { JobDetailed } from '@/types/job';


    const route = useRoute();
    const jobId = computed(() => route.params.id as string)

    const authStore = useAuthStore();

    const job = ref<JobDetailed | null>(null);
    const loading = ref(true);
    const error = ref("");
    const favoriteLoading = ref(false);
    const favorited = ref(false);

    const job_loaded = computed(() => job.value !== null);

    async function loadJob() {
        try {
            job.value = await JobService.getJobByID(jobId.value);
            error.value = "";

            if (authStore.loggedIn) {
                favorited.value = await FavoritedJobService.checkJobFavorited(jobId.value);
            } else {
                favorited.value = false; 
            }
        } catch (err: any) {
            error.value = `Failed to load job with id ${route.params.id}`;
            favorited.value = false;
        } finally {
            loading.value = false;
        }
    }

    async function toggleFavorite() {
        if (!job.value || favoriteLoading.value || !authStore.loggedIn) return; 

        favoriteLoading.value = true;

        try {
            const jobId = job.value.id.toString();
            if (favorited.value) {
                await FavoritedJobService.unfavoriteJob(jobId);
                favorited.value = false;
            } else {
                await FavoritedJobService.favoriteJob(jobId);
                favorited.value = true;
            }
        } catch (err: any) {
            console.error("Failed to toggle favorite", err);
            error.value = "Failed to toggle favorite";
        } finally {
            favoriteLoading.value = false;
        }
    }

    watchEffect(async () => {
        loading.value = true;
        await loadJob();
    });
</script>


<template>
    <p v-if="loading" class="status-message">Loading job...</p>
    <p v-else-if="error" class="status-message error">{{ error }}</p>

    <div v-else-if="job_loaded" class="job-page">

        <div class="job-header">
            <p class="job-eyebrow"><span v-for="(level, index) in job?.seniority_levels" :key="level">
                {{ level }}
                <span v-if="job?.seniority_levels &&(index < job.seniority_levels.length - 1)"> · </span>
            </span></p>
            <a :href="job?.url" class="job-title-link">
                <h1>{{ job?.title }}</h1>
            </a>
        </div>

        <div class="job-body">

            <div class="info-section">
                <div v-if="job?.company" class="info-item">
                    <h2>Company</h2>
                    <p>{{ job.company }}</p>
                </div>
                <div v-if="job?.location" class="info-item">
                    <h2>Location</h2>
                    <p>{{ job.location }}</p>
                </div>
                <div v-if="job?.home_office" class="info-item remote">
                    <h2>Remote</h2>
                    <p>✓ Yes</p>
                </div>
            </div>

            <hr v-if="job?.description" class="divider" />

            <div v-if="job?.description" class="description-section">
                <h2>Description</h2>
                <p>{{ job.description }}</p>
            </div>

            <hr v-if="job?.skills && job.skills.length" class="divider" />

            <div v-if="job?.skills && job.skills.length" class="skills-section">
                <h2>Skills</h2>
                <ul class="skills-list">
                    <li v-for="skill in job.skills" :key="skill.id">{{ skill.name }}</li>
                </ul>
            </div>

            <div class="actions">
                <button
                    class="btn-favorite"
                    :class="{ 'is-favorited': favorited }"
                    :disabled="favoriteLoading || !authStore.loggedIn"
                    @click="toggleFavorite"
                >
                    <span class="star-icon">★</span>
                    <span class="label">{{ favorited ? "Unfavorite" : "Favorite" }}</span>
                </button>
            </div>

        </div>
    </div>
</template>


<style scoped>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .job-page {
        width: 80%;
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .job-header {
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

    .job-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: rgba(255,255,255,0.04);
    }

    .job-header::after {
        content: '';
        position: absolute;
        bottom: -20px; left: 30%;
        width: 320px; height: 120px;
        border-radius: 50%;
        background: rgba(255,255,255,0.025);
    }

    .job-eyebrow {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--color-accent);
        margin-bottom: var(--space-sm);
        position: relative;
        z-index: 1;
    }

    .job-title-link {
        text-decoration: none;
        position: relative;
        z-index: 1;
        display: inline-block;
    }

    .job-title-link h1 {
        font-family: var(--font-display);
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--color-surface);
        line-height: 1.2;
        transition: color var(--transition-base);
    }

    .job-title-link:hover h1 {
        color: var(--color-accent);
    }

    .job-title-link::after {
        content: '↗';
        display: inline-block;
        font-family: var(--font-body);
        font-size: 1rem;
        color: var(--color-accent);
        margin-left: var(--space-sm);
        opacity: 0;
        transform: translateY(4px);
        transition: opacity var(--transition-base), transform var(--transition-base);
    }

    .job-title-link:hover::after {
        opacity: 1;
        transform: translateY(0);
    }

    .job-body {
        background: var(--color-surface);
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 40px 48px 48px;
        box-shadow: var(--shadow-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-3xl);
    }

    .info-section {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: var(--space-lg);
    }

    .info-item {
        padding: 18px 20px;
        background: var(--color-surface-subtle);
        border-radius: var(--radius-md);
        border-left: 3px solid var(--color-primary);
        transition: box-shadow var(--transition-base), transform var(--transition-base);
    }

    .info-item:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }

    .info-item h2 {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
        margin-bottom: var(--space-xs);
    }

    .info-item p {
        font-size: 0.95rem;
        font-weight: 400;
        color: var(--color-text);
        line-height: 1.4;
    }

    .info-item.remote p {
        color: var(--color-success);
        font-weight: 500;
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, var(--color-border-subtle) 0%, transparent 100%);
        border: none;
    }

    .description-section h2,
    .skills-section h2 {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
        margin-bottom: var(--space-sm);
    }

    .description-section p {
        font-size: 1rem;
        line-height: 1.8;
        color: var(--color-text-body);
        max-width: 72ch;
    }

    .skills-list {
        list-style: none;
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-xs);
    }

    .skills-list li {
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        padding: 6px 14px;
        border-radius: var(--radius-pill);
        background: #eef2f8;
        color: var(--color-primary);
        border: 1px solid var(--color-border);
        transition: background var(--transition-fast), color var(--transition-fast), border-color var(--transition-fast);
        cursor: default;
    }

    .skills-list li:hover {
        background: var(--color-primary);
        color: var(--color-surface);
        border-color: var(--color-primary);
    }

    .btn-favorite {
        display: inline-flex;
        align-items: center;
        gap: var(--space-sm);
        font-family: var(--font-body);
        font-size: 0.9rem;
        font-weight: 500;
        padding: 12px 28px;
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-primary);
        background: transparent;
        color: var(--color-primary);
        cursor: pointer;
        letter-spacing: 0.03em;
        transition: background var(--transition-base), color var(--transition-base), transform var(--transition-fast), box-shadow var(--transition-base);
    }

    .btn-favorite:hover:not(:disabled) {
        background: var(--color-primary);
        color: var(--color-surface);
        box-shadow: var(--shadow-btn);
        transform: translateY(-1px);
    }

    .btn-favorite:active:not(:disabled) {
        transform: translateY(0);
        box-shadow: none;
    }

    .btn-favorite.is-favorited {
        background: var(--color-primary);
        color: var(--color-surface);
    }

    .btn-favorite.is-favorited:hover:not(:disabled) {
        background: var(--color-danger);
        border-color: var(--color-danger);
    }

    .btn-favorite:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .btn-favorite .star-icon {
        font-size: 1rem;
        transition: transform var(--transition-base);
    }

    .btn-favorite:hover .star-icon {
        transform: scale(1.2) rotate(-10deg);
    }

    .status-message {
        text-align: center;
        padding: 80px 0;
        font-size: 1rem;
        color: var(--color-text-muted);
        font-weight: 300;
        letter-spacing: 0.04em;
    }
</style>