<script lang="ts" setup>
    import { ref, computed, onMounted } from 'vue'

    import { JobOrder, SeniorityLevel } from '@/types/enums'
    import JobService from '@/services/jobService'
    import useAuthStore from '@/stores/auth'
    import useFiltersStore from '@/stores/filters'
    import type { JobFilters } from '@/types/job'


    const authStore = useAuthStore()
    const filtersStore = useFiltersStore()

    const emit = defineEmits<{
        (e: 'search', filters: JobFilters, order: JobOrder): void
    }>()

    const skillsInput = computed({
        get: () => filtersStore.filters.skills.join(', '),
        set: (val: string) => {
            filtersStore.filters.skills = val
                .split(',')
                .map((s) => s.trim())
                .filter((s) => s)
        }
    })

    const selectedOrder = ref<JobOrder>(JobOrder.UpdateTime)

    const jobOrders = Object.values(JobOrder)
    const seniorityLevels = Object.values(SeniorityLevel)

    function emitSearch() {
        emit('search', filtersStore.filters, selectedOrder.value)
    }

    const saveFilters = async () => {
        await JobService.saveFilters(filtersStore.filters)
    }

    const loadSavedFilters = async () => {
        await filtersStore.loadSavedFilters()
        emitSearch()
    }

    const resetFilters = () => {
        filtersStore.resetFilters()
        emitSearch()
    }

    onMounted(() => {
        emitSearch()
    })
</script>


<template>
    <div>
        <h3>Filters</h3>

        <div>
            <label v-for="level in seniorityLevels" :key="level">
                <input type="checkbox" :value="level" v-model="filtersStore.filters.seniority" />
                {{ level }}
            </label>
        </div>

        <textarea                 
            placeholder="Skills (comma-separated)"
            v-model="skillsInput" 
        />


        <div>
            <input type="text" placeholder="Country" v-model="filtersStore.filters.country" />
        </div>

        <div>
            <input type="text" placeholder="Company" v-model="filtersStore.filters.company" />
        </div>

        <div>
            <label>
                <input type="checkbox" v-model="filtersStore.filters.with_home_office_only" />
                Home office only
            </label>
        </div>

        <div>
            <select v-model="selectedOrder">
                <option v-for="order in jobOrders" :key="order" :value="order">
                    {{ order }}
                </option>
            </select>
        </div>

        <button @click="saveFilters" :disabled="!authStore.loggedIn">Save Filters</button>
        <button @click="loadSavedFilters" :disabled="!authStore.loggedIn">Load Saved Filters</button>
        <button @click="resetFilters">Reset Filters</button>
        <button @click="emitSearch">Search</button>
    </div>
</template>


<style scoped>
    div {
        font-family: var(--font-body);
        color: var(--color-text-body);
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
        background: var(--color-surface);
        padding: var(--space-lg);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-card);
        max-width: 20vw;
        min-width: 180px;
        font-size: 0.85rem; 
    }

    h3 {
        font-family: var(--font-display);
        font-size: 1rem;
        font-weight: 700;
        color: var(--color-primary);
        margin-bottom: var(--space-sm);
    }

    label {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        font-weight: 500;
        color: var(--color-text-body);
        cursor: pointer;
    }

    input[type="text"] {
        font-family: var(--font-body);
        font-size: 0.85rem;
        padding: var(--space-xs) var(--space-sm);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-sm);
        outline: none;
        transition: border-color var(--transition-base), box-shadow var(--transition-base);
        width: 100%;
    }

    input[type="text"]:focus {
        border-color: var(--color-primary);
        box-shadow: var(--shadow-hover);
    }

    input[type="checkbox"] {
        accent-color: var(--color-primary);
        width: 14px;
        height: 14px;
    }

    select {
        font-family: var(--font-body);
        font-size: 0.85rem;
        padding: var(--space-xs) var(--space-sm);
        border-radius: var(--radius-sm);
        border: 1px solid var(--color-border-subtle);
        outline: none;
        transition: border-color var(--transition-base), box-shadow var(--transition-base);
        width: 100%;
    }

    select:focus {
        border-color: var(--color-primary);
        box-shadow: var(--shadow-hover);
    }

    button {
        font-family: var(--font-body);
        font-size: 0.85rem;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-primary);
        background: var(--color-surface);
        color: var(--color-primary);
        cursor: pointer;
        transition: background var(--transition-base), color var(--transition-base), transform var(--transition-fast), box-shadow var(--transition-base);
        margin-top: var(--space-sm);
        width: 100%;
    }

    button:hover:not(:disabled) {
        background: var(--color-primary);
        color: var(--color-surface);
        box-shadow: var(--shadow-btn);
        transform: translateY(-1px);
    }

    button:active:not(:disabled) {
        transform: translateY(0);
        box-shadow: none;
    }

    button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    div {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    textarea {
        font-family: var(--font-body);
        font-size: 0.85rem;
        padding: var(--space-xs) var(--space-sm);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-sm);
        outline: none;
        transition: border-color var(--transition-base), box-shadow var(--transition-base);
        width: 100%;
        resize: vertical; 
        min-height: 60px;
    }

    textarea:focus {
        border-color: var(--color-primary);
        box-shadow: var(--shadow-hover);
    }
</style>

