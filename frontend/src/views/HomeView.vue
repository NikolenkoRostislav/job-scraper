<script lang="ts" setup>
    import { ref } from 'vue';

    import FilterPanel from '@/components/FilterPanel.vue';
    import JobService from '@/services/jobService';
    import FavoritedJobService from '@/services/favoriteJobService';
    import useAuthStore from '@/stores/auth';
    import useFiltersStore from '@/stores/filters';
    import JobListing from '@/components/JobListing.vue';
    import { JobOrder } from '@/types/enums';
    import type { JobListResponse, JobFilters } from '@/types/job';


    const filtersStore = useFiltersStore();
    const authStore = useAuthStore();
    const canLoadMore = ref(true);

    const jobOrder = ref<JobOrder>(JobOrder.UpdateTime);

    const pageSize = 20;
    const maxJobs = pageSize * 5;
    const page = ref(0);
    const jobs = ref<JobListResponse>({ jobs: [], size: 0 });

    const onClick = async () => {
        canLoadMore.value = true;
        page.value = page.value + 1;
        const newJobs = await JobService.getJobs(page.value, pageSize, jobOrder.value, filtersStore.filters);
        jobs.value.jobs.push(...newJobs.jobs);
        jobs.value.size += newJobs.size;

        if (jobs.value.jobs.length > maxJobs) {
            const overflow = jobs.value.jobs.length - maxJobs;
            jobs.value.jobs.splice(0, overflow);
            jobs.value.size -= overflow;
        }

        if (newJobs.size < pageSize) {
            canLoadMore.value = false;
        }
    }
    
    const search = (newFilters: JobFilters, newOrder: JobOrder) => {
        filtersStore.setFilters(newFilters);
        jobOrder.value = newOrder;
        page.value = 0;
        jobs.value = { jobs: [], size: 0 };
        onClick();
    }

    const loadFavoriteJobs = async () => {
        canLoadMore.value = false;
        if (!authStore.loggedIn) return;
        
        const favoriteJobs = await FavoritedJobService.getFavoritedJobs(filtersStore.filters);
        jobs.value = favoriteJobs;
    }
</script>


<template>
    <div class="home-page">
        <div class="page-header">
            <p class="page-eyebrow">Listings</p>
            <h1>Home</h1>
        </div>

        <div class="page-body">
            <div class="main-content">

                <aside class="sidebar">
                    <FilterPanel @search="search" />
                </aside>

                <section class="jobs-section">

                    <div class="jobs-header">
                        <div class="jobs-meta">
                            <h2 class="section-label">Job Listings</h2>
                            <span v-if="jobs.size > 0" class="total-badge">
                                {{ jobs.size.toLocaleString() }} jobs
                            </span>
                        </div>
                        <button
                            class="btn-favorites"
                            @click="loadFavoriteJobs"
                            :disabled="!authStore.loggedIn"
                        >
                            <span class="star-icon">★</span>
                            Favorites
                        </button>
                    </div>

                    <ul v-if="jobs.jobs.length" class="job-list">
                        <JobListing v-for="item in jobs.jobs" :key="item.id" :job="item" />
                    </ul>

                    <p v-else class="empty-state">
                        Use the filters to search for jobs.
                    </p>

                    <button class="btn-load-more" @click="onClick" v-if="canLoadMore && jobs.jobs.length">
                        Load More
                    </button>

                </section>
            </div>
        </div>
    </div>
</template>

<style scoped>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .home-page {
        width: 80%;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .page-header {
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

    .page-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.04);
    }

    .page-header::after {
        content: '';
        position: absolute;
        bottom: -20px; left: 30%;
        width: 320px; height: 120px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.025);
    }

    .page-eyebrow {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--color-accent);
        margin-bottom: var(--space-sm);
        position: relative;
        z-index: 1;
    }

    .page-header h1 {
        font-family: var(--font-display);
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--color-surface);
        line-height: 1.2;
        position: relative;
        z-index: 1;
    }

    .page-body {
        background: var(--color-surface);
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 40px 48px 48px;
        box-shadow: var(--shadow-card);
    }

    .main-content {
        display: flex;
        gap: var(--space-3xl);
        align-items: flex-start;
    }

    .sidebar {
        width: 220px;
        flex-shrink: 0;
    }

    .jobs-section {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: var(--space-lg);
        min-width: 0;
    }

    .jobs-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: var(--space-md);
    }

    .jobs-meta {
        display: flex;
        align-items: center;
        gap: var(--space-md);
    }

    .section-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
    }

    .total-badge {
        font-size: 0.78rem;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: var(--radius-pill);
        background: #eef2f8;
        color: var(--color-primary);
        border: 1px solid var(--color-border);
    }

    .btn-favorites {
        display: inline-flex;
        align-items: center;
        gap: var(--space-sm);
        font-family: var(--font-body);
        font-size: 0.85rem;
        font-weight: 500;
        padding: 8px 18px;
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-primary);
        background: transparent;
        color: var(--color-primary);
        cursor: pointer;
        letter-spacing: 0.03em;
        transition:
            background var(--transition-base),
            color var(--transition-base),
            transform var(--transition-fast),
            box-shadow var(--transition-base);
    }

    .btn-favorites:hover:not(:disabled) {
        background: var(--color-primary);
        color: var(--color-surface);
        box-shadow: var(--shadow-btn);
        transform: translateY(-1px);
    }

    .btn-favorites:active:not(:disabled) {
        transform: translateY(0);
        box-shadow: none;
    }

    .btn-favorites:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .btn-favorites .star-icon {
        font-size: 0.95rem;
        transition: transform var(--transition-base);
    }

    .btn-favorites:hover .star-icon {
        transform: scale(1.2) rotate(-10deg);
    }

    .job-list {
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .empty-state {
        text-align: center;
        padding: 60px 0;
        font-size: 0.95rem;
        color: var(--color-text-muted);
        font-weight: 300;
        letter-spacing: 0.04em;
    }

    .btn-load-more {
        align-self: center;
        font-family: var(--font-body);
        font-size: 0.85rem;
        font-weight: 500;
        padding: 10px 28px;
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-primary);
        background: transparent;
        color: var(--color-primary);
        cursor: pointer;
        letter-spacing: 0.03em;
        transition:
            background var(--transition-base),
            color var(--transition-base),
            transform var(--transition-fast),
            box-shadow var(--transition-base);
        margin-top: var(--space-sm);
    }

    .btn-load-more:hover {
        background: var(--color-primary);
        color: var(--color-surface);
        box-shadow: var(--shadow-btn);
        transform: translateY(-1px);
    }

    .btn-load-more:active {
        transform: translateY(0);
        box-shadow: none;
    }
</style>