import qs from 'qs';

import api from './api.ts'
import type { UserBase, UserCreate } from '@/types/user'
import type { JobFilters } from '@/types/job'


export default class UserService {
    static async register(user: UserCreate, emailCode: number): Promise<UserBase> {
        const res = await api.post('/user/register', user, {
            params: { email_code: emailCode }
        })
        return res.data
    }

    static async getMe(): Promise<UserBase> {
        const res = await api.get('/user/me')
        return res.data
    }

    static async getSavedFilters(): Promise<JobFilters> {
        const res = await api.get('/user/saved-filters')
        return res.data
    }
    
    static async saveFilters(filters: JobFilters): Promise<JobFilters> {
        const query = qs.stringify({
            country: filters.country || undefined,
            company: filters.company || undefined,
            seniority: filters.seniority.length ? filters.seniority : undefined,
            skills: filters.skills.length ? filters.skills : undefined,
            ...(filters.with_home_office_only ? { home_office: true } : {}),
        }, { arrayFormat: 'repeat'});

    const res = await api.post(`/user/save-filters?${query}`);
        return res.data
    }
}
