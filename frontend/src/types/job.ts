import type { SkillBase } from "./skill"
import type { SeniorityLevel } from "./enums"

export type JobFilters = {
    seniority: SeniorityLevel[]
    skills: string[]
    country?: string | null
    company?: string | null
    with_home_office_only: boolean
}

export type JobBase = {
    id: number
    url: string
    title: string
    location?: string | null
    country?: string | null
    company?: string | null
    seniority_levels?: SeniorityLevel[] | null
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

export type JobListResponse = {
  jobs: JobBase[]
  size: number
}