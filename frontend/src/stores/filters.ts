import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { JobFilters} from "@/types/job"
import UserService from '@/services/userService'


const useFiltersStore = defineStore('job', () => {
    const filters = ref<JobFilters>({
        seniority: [],
        skills: [],
        country: null,
        company: null,
        with_home_office_only: false,
    })

    const setFilters = (value: JobFilters) => {
        filters.value = value
    }

    const resetFilters = () => {
        filters.value = {   
            seniority: [],
            skills: [],
            country: null,
            company: null,
            with_home_office_only: false,
        }
    }

    const loadSavedFilters = async () => {
        let savedFilters: JobFilters | null = null

        try {
            savedFilters = await UserService.getSavedFilters()
        }
        catch (error) { }
        
        if (savedFilters) {
            setFilters(savedFilters)
        }
    }

    return { filters, setFilters, loadSavedFilters, resetFilters }
})

export default useFiltersStore
