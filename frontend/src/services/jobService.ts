import api from './api.ts';
import type { JobDetailed } from '@/types/job';


export default class JobService {
    static async getJobByID(id: string): Promise<JobDetailed> {
        const res = (await api.get(`/jobs/${id}`));
        return res.data;
    }
}
