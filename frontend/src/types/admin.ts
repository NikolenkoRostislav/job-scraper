import type { SourceWebsite } from './enums'


export interface DateRange {
    start_time?: string   // ISO 8601 datetime string
    end_time?: string
}

export interface ScrapeReport {
    id: number
    target_website: string
    scrape_started_at?: string
    scrape_finished_at?: string
    total_jobs_scraped: number
    warnings_count: number
    errors_count: number
    end_reason?: string
}

export interface WebsiteStats {
    job_count: number
    scrape_count: number
    failed_scrape_count: number
    date_range: DateRange
}

export interface LogEntry {
    timestamp: string
    level: string
    source: string
    message: string
}