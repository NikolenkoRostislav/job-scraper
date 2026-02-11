<script lang="ts" setup>
    import { ref, watch, computed } from 'vue';

    import api from '@/services/api.ts';

    
    const props = defineProps({id: String})
    
    const job = ref<any>(null);
    const loading = ref(true);
    const error = ref("");

    const job_loaded = computed(() => {
        return job.value !== null
    })

    async function loadJob() {
        try {
            const res = (await api.get(`/jobs/${props.id}`));
            job.value = res.data;
            error.value = ""
        } catch (err) {
            error.value = `Failed to load job with id ${props.id}`;
        } finally {
            loading.value = false;
        }
    }

    watch(
        () => props.id, () => {
            loading.value = true;
            loadJob();
        },
        { immediate: true }
    );
</script>

<template>
    <h1>Job {{ id }}</h1>
    <p v-if="loading">Loading jobs...</p>
    <p v-else-if="error">{{ error }}</p>
    <div v-else-if="job_loaded">
        <p>{{ job?.title }}</p>
    </div>
</template>

<style scoped>
</style>
