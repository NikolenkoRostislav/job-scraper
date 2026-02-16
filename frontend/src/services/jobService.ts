import qs from 'qs';

import api from './api.ts'
import type { JobBase, JobDetailed, JobFilters } from '@/types/job'
import type { SkillBase } from '@/types/skill'
import { JobOrder } from '@/types/enums'


export default class JobService {
    static async getJobByID(id: string): Promise<JobDetailed> {
        const res = await api.get(`/jobs/${id}`)
        return res.data
    }

    static async getJobs(
        page: number = 1,
        pageSize: number = 20,
        orderBy: JobOrder = JobOrder.UpdateTime,
        filters?: JobFilters
    ): Promise<{ jobs: JobBase[]; size: number }> {
        const res = await api.get('/jobs', {
            params: {
                page,
                page_size: pageSize,
                order_by: orderBy,
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

    static async getJobCount(): Promise<number> {
        const res = await api.get('/jobs/job-count')
        return res.data
    }

    static async getJobSkills(jobId: string): Promise<SkillBase[]> {
        const res = await api.get(`/jobs/${jobId}/skills`)
        return res.data
    }

    static async saveFilters(filters: JobFilters): Promise<JobFilters> {
        const res = await api.post('/jobs/save-filters', filters)
        return res.data
    }
}
