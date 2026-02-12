import api from '@/services/api.ts';


export async function getJobByID(id: string) {
    const res = (await api.get(`/jobs/${id}`));
    return res.data;
}