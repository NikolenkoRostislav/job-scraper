import type { SkillBase } from "./skill"


export type JobBase = {
    id: number
    url: string
    title: string
    location?: string | null
    country?: string | null
    company?: string | null
    seniority_levels?: string[] | null
    home_office?: boolean | null
    created_at?: string | null
    last_updated_at?: string | null
    last_seen_at?: string | null
}

export type JobDetailed = JobBase & {
    description?: string | null
    source_website?: string | null
    skills?: SkillBase[] | null
}