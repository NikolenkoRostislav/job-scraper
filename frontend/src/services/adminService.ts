import api from './api.ts'
import type { JobListResponse } from '@/types/job'
import type { DateRange, WebsiteStats, LogEntry, ScrapeReport } from '@/types/admin.ts'
import type { LogLevel, SourceWebsite } from '@/types/enums.ts'


export default class AdminService {
    static async deleteJob(jobId: number): Promise<void> {
        await api.delete(`/admin/jobs/${jobId}`)
    }

    static async getLogs(logName: string, logLevel: LogLevel, dateRange?: DateRange): Promise<LogEntry[]> {
        const res = await api.get('/admin/stats/logs', {
            params: {
                log_name: logName,
                log_level: logLevel,
                ...dateRange
            }
        })
        return res.data
    }

    static async getJobCount(dateRange?: DateRange): Promise<number> {
        const res = await api.get('/admin/stats/jobs-count', {
            params: { ...dateRange }
        })
        return res.data
    }

    static async getOutdatedJobs(cutoffTime: Date): Promise<JobListResponse> {
        const res = await api.get('/admin/stats/outdated-jobs', {
            params: { cutoff_time: cutoffTime.toISOString() }
        })
        return res.data
    }

    static async getWebsiteStats(sourceWebsite: SourceWebsite, dateRange?: DateRange): Promise<WebsiteStats> {
        const res = await api.get(`/admin/stats/${sourceWebsite}`, {
            params: { ...dateRange }
        })
        return res.data
    }

    static async getScrapeReports(sourceSpider: SourceWebsite, failedOnly: boolean = false, dateRange?: DateRange): Promise<ScrapeReport[]> {
        const res = await api.get('/admin/scrape-reports', {
            params: {
                source_spider: sourceSpider,
                failed_only: failedOnly,
                ...dateRange
            }
        })
        return res.data
    }

    static async getScrapeReport(reportId: number): Promise<ScrapeReport> {
        const res = await api.get(`/admin/scrape-reports/${reportId}`)
        return res.data
    }
}