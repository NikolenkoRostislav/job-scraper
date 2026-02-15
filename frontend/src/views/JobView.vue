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
    <h1>Job {{ route.params.id }}</h1>

    <p v-if="loading">Loading job...</p>
    <p v-else-if="error">{{ error }}</p>

    <div v-else-if="job_loaded">
        <h2>{{ job?.title }}</h2>
        <p v-if="job?.company"><strong>Company:</strong> {{ job.company }}</p>
        <p v-if="job?.location"><strong>Location:</strong> {{ job.location }}</p>
        <p v-if="job?.home_office"><strong>Remote:</strong> Yes</p>
        <p v-if="job?.description"><strong>Description:</strong> {{ job.description }}</p>

        <div v-if="job?.skills && job.skills.length">
        <strong>Skills:</strong>
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
