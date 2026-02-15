<script lang="ts" setup>
    import { ref, watchEffect, computed } from 'vue';
    import { useRoute } from 'vue-router';

    import JobService from '@/services/jobService';
    import FavoritedJobService from '@/services/favoriteJobService';
    import { getParam } from '@/utils/paramHelpers';
    import type { JobDetailed } from '@/types/job';
    import isLoggedIn from '@/utils/loginChecker';

    const route = useRoute();

    const job = ref<JobDetailed | null>(null);
    const loading = ref(true);
    const error = ref("");
    const favoriteLoading = ref(false);
    const favorited = ref(false);

    const job_loaded = computed(() => job.value !== null);

    async function loadJob() {
        try {
            const jobId = getParam(route.params.id);
            job.value = await JobService.getJobByID(jobId);
            error.value = "";

            if (isLoggedIn()) {
                favorited.value = await FavoritedJobService.checkJobFavorited(jobId);
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
        if (!job.value || favoriteLoading.value || !isLoggedIn()) return; 

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
    <p v-if="loading">Loading job...</p>
    <p v-else-if="error">{{ error }}</p>

    <div v-else-if="job_loaded">
        <h1>{{ job?.title }}</h1>

        <div v-if="job?.company">
            <h2>Company:</h2>
            <p>{{ job.company }}</p>
        </div>

        <div v-if="job?.location">
            <h2>Location:</h2>
            <p>{{ job.location }}</p>
        </div>

        <div v-if="job?.home_office">
            <h2>Remote:</h2>
            <p>Yes</p>
        </div>

        <div v-if="job?.description">
            <h2>Description:</h2>
            <p>{{ job.description }}</p>
        </div>

        <div v-if="job?.skills && job.skills.length">
            <h2>Skills:</h2>
            <ul>
                <li v-for="skill in job.skills" :key="skill.id">{{ skill.name }}</li>
            </ul>
        </div>

        <button @click="toggleFavorite" :disabled="favoriteLoading || !isLoggedIn()">
            {{ favorited ? "Unfavorite" : "Favorite" }}
        </button>
    </div>
</template>

<style scoped>
</style>
