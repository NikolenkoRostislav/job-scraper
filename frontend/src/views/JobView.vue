<script lang="ts" setup>
    import { ref, watchEffect, computed } from 'vue';
    import { useRoute } from 'vue-router'

    import { getJobByID } from '@/services/jobService';
    import { getParam } from '@/utils/paramHelpers';

    const route = useRoute()
    
    const job = ref<any>(null);
    const loading = ref(true);
    const error = ref("");
    
    const job_loaded = computed(() => {
        return job.value !== null
    })

    async function loadJob() {
        try {
            job.value = await getJobByID(getParam(route.params.id))
            error.value = ""
        } catch (err) {
            error.value = `Failed to load job with id ${route.params.id}`;
        } finally {
            loading.value = false;
        }
    }

    watchEffect(
        async () => {
            loading.value = true;
            await loadJob();
        }
    );
</script>

<template>
    <h1>Job {{ route.params.id }}</h1>
    <p v-if="loading">Loading jobs...</p>
    <p v-else-if="error">{{ error }}</p>
    <div v-else-if="job_loaded">
        <p>{{ job?.title }}</p>
    </div>
</template>

<style scoped>
</style>
