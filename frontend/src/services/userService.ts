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
}
