import qs from 'qs'

import api from './api.ts'
import type { JobListResponse, JobDetailed, JobFilters } from '@/types/job'

export default class FavoritedJobService {
    static async getFavoritedJobs(filters?: JobFilters): Promise<JobListResponse> {
        const res = await api.get('/favorited-jobs/', {
            params: {
                country: filters?.country,
                company: filters?.company,
                seniority: filters?.seniority,
                skills: filters?.skills,
                ...(filters?.with_home_office_only && { home_office: true })
            },
            paramsSerializer: params => qs.stringify(params, { arrayFormat: 'repeat' })
        })
        return res.data
    }

    static async checkJobFavorited(jobId: string): Promise<boolean> {
        const res = await api.get(`/favorited-jobs/${jobId}/is-favorited`)
        return res.data
    }

    static async favoriteJob(jobId: string): Promise<JobDetailed> {
        const res = await api.post(`/favorited-jobs/${jobId}/favorite`)
        return res.data
    }

    static async unfavoriteJob(jobId: string): Promise<void> {
        await api.delete(`/favorited-jobs/${jobId}/unfavorite`)
    }
}
