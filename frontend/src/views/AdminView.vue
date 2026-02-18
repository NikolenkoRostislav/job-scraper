<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    import useAuthStore from '@/stores/auth';
    import AdminService from '@/services/adminService';
    import type { WebsiteStats, ScrapeReport, LogEntry, DateRange } from '@/types/admin';
    import { SourceWebsite, LogLevel } from '@/types/enums';

    const authStore = useAuthStore();

    const jobCount = ref<number | null>(null);
    const jobCountDateRange = ref<DateRange>({});

    const outdatedCutoff = ref<string>('');
    const outdatedCount = ref<number | null>(null);

    const selectedStatsSource = ref<SourceWebsite>(SourceWebsite.DICE);
    const statsDateRange = ref<DateRange>({});
    const websiteStats = ref<WebsiteStats | null>(null);
    const statsLoading = ref(false);

    const selectedReportSource = ref<SourceWebsite>(SourceWebsite.DICE);
    const reportDateRange = ref<DateRange>({});
    const failedOnly = ref(false);
    const scrapeReports = ref<ScrapeReport[]>([]);
    const reportsLoading = ref(false);

    const logName = ref<string>('');
    const selectedLogLevel = ref<LogLevel>(LogLevel.WARNING);
    const logDateRange = ref<DateRange>({});
    const logs = ref<LogEntry[]>([]);
    const logsLoading = ref(false);

    const sourceWebsiteOptions = Object.entries(SourceWebsite) as [string, SourceWebsite][];
    const logLevelOptions = Object.values(LogLevel);

    onMounted(async () => {
        jobCount.value = await AdminService.getJobCount();
    });

    const fetchJobCount = async () => {
        jobCount.value = await AdminService.getJobCount(jobCountDateRange.value);
    }

    const fetchWebsiteStats = async () => {
        statsLoading.value = true;
        try {
            websiteStats.value = await AdminService.getWebsiteStats(selectedStatsSource.value, statsDateRange.value);
        } finally {
            statsLoading.value = false;
        }
    }

    const fetchOutdatedJobs = async () => {
        if (!outdatedCutoff.value) return;
        const count = await AdminService.getOutdatedJobs(new Date(outdatedCutoff.value));
        outdatedCount.value = count.size;
    }

    const fetchScrapeReports = async () => {
        reportsLoading.value = true;
        try {
            scrapeReports.value = await AdminService.getScrapeReports(
                selectedReportSource.value,
                failedOnly.value,
                reportDateRange.value
            );
        } finally {
            reportsLoading.value = false;
        }
    }

    const fetchLogs = async () => {
        if (!logName.value.trim()) return;
        logsLoading.value = true;
        try {
            logs.value = await AdminService.getLogs(logName.value, selectedLogLevel.value, logDateRange.value);
        } finally {
            logsLoading.value = false;
        }
    }

    const formatDate = (dt: string | null | undefined): string => {
        if (!dt) return '—';
        return new Date(dt).toLocaleString();
    }

    const logLevelClass = (level: string): string => {
        return `log-level--${level.toLowerCase()}`;
    }
</script>


<template>
    <div class="admin-page">
        <div class="page-header">
            <p class="page-eyebrow">Dashboard</p>
            <h1>Admin</h1>
        </div>

        <template v-if="authStore.user?.is_admin">
            <div class="page-body">
                <section class="card">
                    <h2 class="section-label">Overview</h2>
                    <div class="overview-row">
                        <div v-if="jobCount !== null" class="stat-block">
                            <span class="stat-label">Total Jobs Listed</span>
                            <span class="stat-value">{{ jobCount.toLocaleString() }}</span>
                        </div>
                        <div class="filter-row">
                            <div class="field">
                                <label class="field-label">From</label>
                                <input class="input" type="datetime-local" v-model="jobCountDateRange.start_time" />
                            </div>
                            <div class="field">
                                <label class="field-label">To</label>
                                <input class="input" type="datetime-local" v-model="jobCountDateRange.end_time" />
                            </div>
                            <button class="btn" @click="fetchJobCount">Fetch</button>
                        </div>
                    </div>
                </section>

                <hr class="divider" />

                <section class="card">
                    <h2 class="section-label">Outdated Jobs</h2>
                    <div class="filter-row">
                        <div class="field">
                            <label class="field-label">Cutoff Time</label>
                            <input class="input" type="datetime-local" v-model="outdatedCutoff" />
                        </div>
                        <button class="btn" @click="fetchOutdatedJobs" :disabled="!outdatedCutoff">Check</button>
                    </div>
                    <div v-if="outdatedCount !== null" class="stat-grid mt-md">
                        <div class="stat-block">
                            <span class="stat-label">Jobs Not Seen Since Cutoff</span>
                            <span class="stat-value">{{ outdatedCount.toLocaleString() }}</span>
                        </div>
                    </div>
                </section>

                <hr class="divider" />

                <section class="card">
                    <h2 class="section-label">Website Stats</h2>
                    <div class="filter-row">
                        <div class="field">
                            <label class="field-label">Source</label>
                            <select class="input" v-model="selectedStatsSource">
                                <option v-for="[key, val] in sourceWebsiteOptions" :key="val" :value="val">
                                    {{ key.replace(/_/g, ' ') }}
                                </option>
                            </select>
                        </div>
                        <div class="field">
                            <label class="field-label">From</label>
                            <input class="input" type="datetime-local" v-model="statsDateRange.start_time" />
                        </div>
                        <div class="field">
                            <label class="field-label">To</label>
                            <input class="input" type="datetime-local" v-model="statsDateRange.end_time" />
                        </div>
                        <button class="btn" @click="fetchWebsiteStats" :disabled="statsLoading">
                            {{ statsLoading ? 'Loading…' : 'Fetch' }}
                        </button>
                    </div>
                    <div v-if="websiteStats" class="stat-grid mt-md">
                        <div class="stat-block">
                            <span class="stat-label">Jobs</span>
                            <span class="stat-value">{{ websiteStats.job_count.toLocaleString() }}</span>
                        </div>
                        <div class="stat-block">
                            <span class="stat-label">Scrapes</span>
                            <span class="stat-value">{{ websiteStats.scrape_count.toLocaleString() }}</span>
                        </div>
                        <div class="stat-block stat-block--danger">
                            <span class="stat-label">Failed Scrapes</span>
                            <span class="stat-value">{{ websiteStats.failed_scrape_count.toLocaleString() }}</span>
                        </div>
                    </div>
                </section>

                <hr class="divider" />

                <section class="card">
                    <h2 class="section-label">Scrape Reports</h2>
                    <div class="filter-row">
                        <div class="field">
                            <label class="field-label">Source</label>
                            <select class="input" v-model="selectedReportSource">
                                <option v-for="[key, val] in sourceWebsiteOptions" :key="val" :value="val">
                                    {{ key.replace(/_/g, ' ') }}
                                </option>
                            </select>
                        </div>
                        <div class="field">
                            <label class="field-label">From</label>
                            <input class="input" type="datetime-local" v-model="reportDateRange.start_time" />
                        </div>
                        <div class="field">
                            <label class="field-label">To</label>
                            <input class="input" type="datetime-local" v-model="reportDateRange.end_time" />
                        </div>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="failedOnly" />
                            Failed only
                        </label>
                        <button class="btn" @click="fetchScrapeReports" :disabled="reportsLoading">
                            {{ reportsLoading ? 'Loading…' : 'Fetch' }}
                        </button>
                    </div>
                    <div v-if="scrapeReports.length" class="table-wrap mt-md">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Started</th>
                                    <th>Finished</th>
                                    <th>Jobs</th>
                                    <th>Warnings</th>
                                    <th>Errors</th>
                                    <th>End Reason</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="report in scrapeReports" :key="report.id"
                                    :class="{ 'row--danger': report.errors_count > 0 }">
                                    <td class="mono">{{ report.id }}</td>
                                    <td>{{ formatDate(report.scrape_started_at) }}</td>
                                    <td>{{ formatDate(report.scrape_finished_at) }}</td>
                                    <td>{{ report.total_jobs_scraped }}</td>
                                    <td :class="{ 'cell--warn': report.warnings_count > 0 }">{{ report.warnings_count }}</td>
                                    <td :class="{ 'cell--danger': report.errors_count > 0 }">{{ report.errors_count }}</td>
                                    <td class="mono">{{ report.end_reason ?? '—' }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <p v-else-if="!reportsLoading" class="empty-state">No reports to display. Apply filters and fetch.</p>
                </section>

                <hr class="divider" />

                <section class="card">
                    <h2 class="section-label">Log Viewer</h2>
                    <div class="filter-row">
                        <div class="field">
                            <label class="field-label">Log Name</label>
                            <input class="input" type="text" v-model="logName" placeholder="e.g. api.log" />
                        </div>
                        <div class="field">
                            <label class="field-label">Min Level</label>
                            <select class="input" v-model="selectedLogLevel">
                                <option v-for="level in logLevelOptions" :key="level" :value="level">{{ level }}</option>
                            </select>
                        </div>
                        <div class="field">
                            <label class="field-label">From</label>
                            <input class="input" type="datetime-local" v-model="logDateRange.start_time" />
                        </div>
                        <div class="field">
                            <label class="field-label">To</label>
                            <input class="input" type="datetime-local" v-model="logDateRange.end_time" />
                        </div>
                        <button class="btn" @click="fetchLogs" :disabled="logsLoading || !logName.trim()">
                            {{ logsLoading ? 'Loading…' : 'Fetch' }}
                        </button>
                    </div>
                    <div v-if="logs.length" class="log-list mt-md">
                        <div v-for="(entry, i) in logs" :key="i" class="log-entry">
                            <span class="log-timestamp">{{ formatDate(entry.timestamp) }}</span>
                            <span class="log-level" :class="logLevelClass(entry.level)">{{ entry.level }}</span>
                            <span class="log-source mono">{{ entry.source }}</span>
                            <span class="log-message">{{ entry.message }}</span>
                        </div>
                    </div>
                    <p v-else-if="!logsLoading" class="empty-state">No logs to display. Enter a log name and fetch.</p>
                </section>

            </div>
        </template>

        <template v-else>
            <div class="page-body">
                <p class="body-text">
                    Nice try<span v-if="authStore.user">{{ `, ${authStore.user.username}` }}</span>! You don't have admin privileges.
                </p>
            </div>
        </template>
    </div>
</template>


<style scoped>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .admin-page {
        width: 80%;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .page-header {
        background: linear-gradient(
            135deg,
            var(--color-primary) 0%,
            var(--color-primary-mid) 60%,
            var(--color-primary-deep) 100%
        );
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        padding: 40px 48px 36px;
        position: relative;
        overflow: hidden;
    }

    .page-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.04);
    }

    .page-header::after {
        content: '';
        position: absolute;
        bottom: -20px; left: 30%;
        width: 320px; height: 120px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.025);
    }

    .page-eyebrow {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--color-accent);
        margin-bottom: var(--space-sm);
        position: relative;
        z-index: 1;
    }

    .page-header h1 {
        font-family: var(--font-display);
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--color-surface);
        line-height: 1.2;
        position: relative;
        z-index: 1;
    }

    .page-body {
        background: var(--color-surface);
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 40px 48px 48px;
        box-shadow: var(--shadow-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-3xl);
    }

    .section-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
        margin-bottom: var(--space-lg);
    }

    .body-text {
        font-size: 0.95rem;
        line-height: 1.75;
        color: var(--color-text-body);
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, var(--color-border-subtle) 0%, transparent 100%);
        border: none;
    }

    /* ── Stats ── */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-lg);
    }

    .stat-block {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
        padding: 18px 24px;
        background: var(--color-surface-subtle);
        border-radius: var(--radius-md);
        border-left: 3px solid var(--color-primary);
        transition: box-shadow var(--transition-base), transform var(--transition-base);
    }

    .stat-block:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }

    .stat-block--danger {
        border-left-color: var(--color-danger, #e05);
    }

    .stat-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
    }

    .stat-value {
        font-family: var(--font-display);
        font-size: 2rem;
        font-weight: 700;
        color: var(--color-primary);
        line-height: 1;
    }

    /* ── Filters ── */
    .filter-row {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        gap: var(--space-md);
    }

    .field {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .field-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--color-text-muted);
    }

    .input {
        font-size: 0.88rem;
        padding: 8px 12px;
        border-radius: var(--radius-sm);
        border: 1px solid var(--color-border);
        background: var(--color-surface-subtle);
        color: var(--color-text);
        outline: none;
        transition: border-color var(--transition-fast);
    }

    .input:focus {
        border-color: var(--color-primary);
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        font-size: 0.88rem;
        color: var(--color-text-body);
        padding-bottom: 8px;
        cursor: pointer;
    }

    .btn {
        padding: 8px 20px;
        font-size: 0.88rem;
        font-weight: 500;
        border-radius: var(--radius-sm);
        border: none;
        background: var(--color-primary);
        color: var(--color-surface);
        cursor: pointer;
        transition: opacity var(--transition-fast), transform var(--transition-fast);
    }

    .btn:hover:not(:disabled) {
        opacity: 0.88;
        transform: translateY(-1px);
    }

    .btn:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    /* ── Table ── */
    .table-wrap {
        overflow-x: auto;
        border-radius: var(--radius-md);
        border: 1px solid var(--color-border-subtle);
    }

    .table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }

    .table th {
        text-align: left;
        padding: 10px 14px;
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--color-text-muted);
        background: var(--color-surface-subtle);
        border-bottom: 1px solid var(--color-border-subtle);
    }

    .table td {
        padding: 10px 14px;
        color: var(--color-text-body);
        border-bottom: 1px solid var(--color-border-subtle);
    }

    .table tbody tr:last-child td {
        border-bottom: none;
    }

    .table tbody tr:hover {
        background: var(--color-surface-subtle);
    }

    .row--danger {
        background: color-mix(in srgb, var(--color-danger, #e05) 6%, transparent);
    }

    .cell--warn { color: var(--color-warning, #f90); font-weight: 600; }
    .cell--danger { color: var(--color-danger, #e05); font-weight: 600; }

    /* ── Logs ── */
    .log-list {
        display: flex;
        flex-direction: column;
        gap: 2px;
        font-size: 0.83rem;
        border-radius: var(--radius-md);
        border: 1px solid var(--color-border-subtle);
        overflow: hidden;
    }

    .log-entry {
        display: grid;
        grid-template-columns: 170px 72px 160px 1fr;
        align-items: baseline;
        gap: var(--space-md);
        padding: 8px 14px;
        transition: background var(--transition-fast);
    }

    .log-entry:nth-child(even) {
        background: var(--color-surface-subtle);
    }

    .log-entry:hover {
        background: color-mix(in srgb, var(--color-primary) 6%, transparent);
    }

    .log-timestamp {
        color: var(--color-text-muted);
        font-variant-numeric: tabular-nums;
    }

    .log-level {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 2px 6px;
        border-radius: var(--radius-pill);
        text-align: center;
    }

    .log-level--debug   { background: color-mix(in srgb, var(--color-text-muted) 15%, transparent); color: var(--color-text-muted); }
    .log-level--info    { background: color-mix(in srgb, #3b82f6 15%, transparent); color: #3b82f6; }
    .log-level--warning { background: color-mix(in srgb, var(--color-warning, #f90) 18%, transparent); color: var(--color-warning, #f90); }
    .log-level--error   { background: color-mix(in srgb, var(--color-danger, #e05) 15%, transparent); color: var(--color-danger, #e05); }
    .log-level--critical{ background: var(--color-danger, #e05); color: #fff; }

    .log-source {
        color: var(--color-text-muted);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .log-message {
        color: var(--color-text-body);
        white-space: pre-wrap;
        word-break: break-word;
    }

    /* ── Misc ── */
    .mono { font-family: var(--font-mono, monospace); }
    .mt-md { margin-top: var(--space-md); }

    .empty-state {
        font-size: 0.88rem;
        color: var(--color-text-muted);
        padding: var(--space-lg) 0;
        text-align: center;
    }

    .overview-row {
        display: flex;
        align-items: center;
        gap: var(--space-xl);
    }

    .overview-row .stat-block {
        flex-shrink: 0;
        min-width: 180px;
    }

    .overview-row .filter-row {
        flex: 1;
    }
</style>