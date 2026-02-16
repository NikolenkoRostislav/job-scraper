import api from './api.ts'
import type { SkillDetailResponse, SkillListResponse } from '@/types/skill'


export default class SkillService {
    static async getSkillsCount(): Promise<number> {
        const res = await api.get('/skills/skill-count')
        return res.data
    }

    static async getTopSkills(limit: number = 10): Promise<SkillListResponse> {
        const res = await api.get(`/skills/ranking/${limit}`)
        return res.data
    }

    static async getSkillByName(skillName: string): Promise<SkillDetailResponse | null> {
        const res = await api.get(`/skills/${skillName}`)
        return res.data
    }
}
