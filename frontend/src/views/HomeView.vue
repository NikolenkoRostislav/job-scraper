<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    import JobService from '@/services/jobService';
    import type { JobListResponse } from '@/types/job';


    const pageSize = 20;
    const totalJobs = ref(0);
    const page = ref(0);
    const jobs = ref<JobListResponse>({ jobs: [], size: 0 });

    const onClick = async () => {
        page.value = page.value + 1;
        const newJobs = await JobService.getJobs(page.value, pageSize);
        jobs.value.jobs.push(...newJobs.jobs);
        totalJobs.value += newJobs.size;
        jobs.value.size += newJobs.size;
    }

    onMounted(async () => {
        onClick();
    })
</script>


<template>
    <h1>Home</h1>
    <div>Pretend we have a filters menu here</div>
    <h2>Job Listings</h2>
    <p>Total Jobs: {{ totalJobs }}</p>
    <ul>
        <li v-for="item in jobs.jobs" :key="item.id">
            <router-link :to="`/job/${item.id}`">
            {{ item.title }}
            </router-link>
        </li>
    </ul>
    <button @click="onClick">Load More</button>
</template>


<style scoped>
</style>
