<script lang="ts" setup>
    import { ref, watch } from 'vue'

    import { JobOrder, SeniorityLevel } from '@/types/enums'
    import UserService from '@/services/userService'
    import JobService from '@/services/jobService'
    import useAuthStore from '@/stores/auth'
    import type { JobFilters } from '@/types/job'


    const authStore = useAuthStore()

    const emit = defineEmits<{
        (e: 'search', filters: JobFilters, order: JobOrder): void
    }>()

    const filters = ref<JobFilters>({
        seniority: [],
        skills: [],
        country: null,
        company: null,
        with_home_office_only: false,
    })

    const skillsInput = ref('')

    watch(skillsInput, (val) => {
        filters.value.skills = val
        .split(',')
        .map((s) => s.trim())
        .filter((s) => s)
    })

    const selectedOrder = ref<JobOrder>(JobOrder.UpdateTime)

    const jobOrders = Object.values(JobOrder)
    const seniorityLevels = Object.values(SeniorityLevel)

    function emitSearch() {
        emit('search', filters.value, selectedOrder.value)
    }

    const saveFilters = async () => {
        await JobService.saveFilters(filters.value)
    }

    const loadSavedFilters = async () => {
        let savedFilters: JobFilters | null = null

        if (authStore.loggedIn) {
            savedFilters = await UserService.getSavedFilters()
        }

        if (savedFilters) {
            filters.value = savedFilters
            skillsInput.value = savedFilters.skills.join(', ')
        }

        emitSearch()
    }

    watch(
        () => authStore.ready,
        (ready) => {
            if (ready) {
                loadSavedFilters()
            }
        },
        { immediate: true }
    )
</script>


<template>
    <div>
        <h3>Filters</h3>

        <div>
            <label v-for="level in seniorityLevels" :key="level">
                <input type="checkbox" :value="level" v-model="filters.seniority" />
                {{ level }}
            </label>
        </div>

        <div>
            <input
                type="text"
                placeholder="Skills (comma-separated)"
                v-model="skillsInput"
            />
        </div>

        <div>
            <input type="text" placeholder="Country" v-model="filters.country" />
        </div>

        <div>
            <input type="text" placeholder="Company" v-model="filters.company" />
        </div>

        <div>
            <label>
                <input type="checkbox" v-model="filters.with_home_office_only" />
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
        <button @click="emitSearch">Search All</button>
    </div>
</template>


<style scoped>
</style>
