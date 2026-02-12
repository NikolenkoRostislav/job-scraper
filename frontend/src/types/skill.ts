export type SkillBase = {
    id: number
    name: string
    category?: string | null
}

export type SkillDetailResponse = {
    skill: SkillBase
    job_count: number
    frequency: number
}

export type SkillListResponse = {
  skills: SkillDetailResponse[]
  size: number
}