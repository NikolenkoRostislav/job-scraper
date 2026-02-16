<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    import FilterPanel from '@/components/FilterPanel.vue';
    import JobService from '@/services/jobService';
    import { JobOrder } from '@/types/enums';
    import type { JobListResponse, JobFilters } from '@/types/job';

    
    const filters = ref<JobFilters>({
        seniority: [],
        skills: [],
        country: null,
        company: null,
        with_home_office_only: false,
    });
    const jobOrder = ref<JobOrder>(JobOrder.UpdateTime);


    const pageSize = 20;
    const totalJobs = ref(0);
    const page = ref(0);
    const jobs = ref<JobListResponse>({ jobs: [], size: 0 });

    const emitSearch = (newFilters: JobFilters, newOrder: JobOrder) => {
        filters.value = newFilters;
        jobOrder.value = newOrder;
        page.value = 0;
        jobs.value = { jobs: [], size: 0 };
        totalJobs.value = 0;
        onClick();
    }
    const onClick = async () => {
        page.value = page.value + 1;
        const newJobs = await JobService.getJobs(page.value, pageSize, jobOrder.value, filters.value);
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
    <FilterPanel @search="emitSearch"/>
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
