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

    body {
        background: #f0f2f5;
        font-family: 'DM Sans', sans-serif;
        color: #1a2233;
        min-height: 100vh;
        display: flex;
        justify-content: center;
        padding: 48px 24px;
    }

    .job-page {
        width: 100%;
        max-width: 760px;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    /* ── Header Card ─────────────────────────────── */
    .job-header {
        background: linear-gradient(135deg, #1a2a4a 0%, #243554 60%, #1e3a5f 100%);
        border-radius: 16px 16px 0 0;
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
        color: #7eb8f7;
        margin-bottom: 14px;
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
        font-family: 'Playfair Display', serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
        transition: color 0.2s;
    }

    .job-title-link:hover h1 {
        color: #7eb8f7;
    }

    .job-title-link::after {
        content: '↗';
        display: inline-block;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        color: #7eb8f7;
        margin-left: 10px;
        opacity: 0;
        transform: translateY(4px);
        transition: opacity 0.2s, transform 0.2s;
    }

    .job-title-link:hover::after {
        opacity: 1;
        transform: translateY(0);
    }

    /* ── Body Card ───────────────────────────────── */
    .job-body {
        background: #ffffff;
        border-radius: 0 0 16px 16px;
        padding: 40px 48px 48px;
        box-shadow: 0 8px 40px rgba(26, 34, 51, 0.10);
        display: flex;
        flex-direction: column;
        gap: 32px;
    }

    /* ── Info Section ─────────────────────────────── */
    .info-section {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 20px;
    }

    .info-item {
        padding: 18px 20px;
        background: #f7f9fc;
        border-radius: 10px;
        border-left: 3px solid #1a2a4a;
        transition: box-shadow 0.2s, transform 0.2s;
    }

    .info-item:hover {
        box-shadow: 0 4px 16px rgba(26, 42, 74, 0.10);
        transform: translateY(-2px);
    }

    .info-item h2 {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #7b8fa6;
        margin-bottom: 6px;
    }

    .info-item p {
        font-size: 0.95rem;
        font-weight: 400;
        color: #1a2233;
        line-height: 1.4;
    }

    .info-item.remote p {
        color: #1a7a4a;
        font-weight: 500;
    }

    /* ── Divider ──────────────────────────────────── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, #e2e8f0 0%, transparent 100%);
        border: none;
    }

    /* ── Description ──────────────────────────────── */
    .description-section h2 {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #7b8fa6;
        margin-bottom: 14px;
    }

    .description-section p {
        font-size: 0.95rem;
        line-height: 1.75;
        color: #3a4a60;
    }

    /* ── Skills ───────────────────────────────────── */
    .skills-section h2 {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #7b8fa6;
        margin-bottom: 14px;
    }

    .skills-list {
        list-style: none;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .skills-list li {
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        padding: 6px 14px;
        border-radius: 20px;
        background: #eef2f8;
        color: #1a2a4a;
        border: 1px solid #d5deee;
        transition: background 0.15s, color 0.15s, border-color 0.15s;
        cursor: default;
    }

    .skills-list li:hover {
        background: #1a2a4a;
        color: #ffffff;
        border-color: #1a2a4a;
    }

    /* ── Favorite Button ─────────────────────────── */
    .actions {
        display: flex;
        justify-content: flex-end;
        padding-top: 8px;
    }

    .btn-favorite {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 12px 28px;
        border-radius: 8px;
        border: 2px solid #1a2a4a;
        background: transparent;
        color: #1a2a4a;
        cursor: pointer;
        letter-spacing: 0.03em;
        transition: background 0.2s, color 0.2s, transform 0.15s, box-shadow 0.2s;
    }

    .btn-favorite:hover:not(:disabled) {
        background: #1a2a4a;
        color: #ffffff;
        box-shadow: 0 4px 16px rgba(26, 42, 74, 0.25);
        transform: translateY(-1px);
    }

    .btn-favorite:active:not(:disabled) {
        transform: translateY(0);
        box-shadow: none;
    }

    .btn-favorite.is-favorited {
        background: #1a2a4a;
        color: #ffffff;
    }

    .btn-favorite.is-favorited:hover:not(:disabled) {
        background: #c0392b;
        border-color: #c0392b;
    }

    .btn-favorite:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .btn-favorite .star-icon {
        font-size: 1rem;
        transition: transform 0.2s;
    }

    .btn-favorite:hover .star-icon {
        transform: scale(1.2) rotate(-10deg);
    }

    /* ── Status messages ─────────────────────────── */
    .status-message {
        text-align: center;
        padding: 80px 0;
        font-size: 1rem;
        color: #7b8fa6;
        font-weight: 300;
        letter-spacing: 0.04em;
    }
</style>
