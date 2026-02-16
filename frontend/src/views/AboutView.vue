<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    import JobService from '@/services/jobService';
    import SkillService from '@/services/skillService';
    import type { SkillListResponse } from '@/types/skill';

    const sources = [
        {"name": "Dice", "url": "https://www.dice.com/"},
        {"name": "Get in IT", "url": "https://www.get-in-it.de/"},
        {"name": "Relocate.me", "url": "https://www.relocate.me/"},
        {"name": "WeAreDevelopers", "url": "https://www.wearedevelopers.com/"},
        {"name": "SAP", "url": "https://jobs.sap.com/"},
        {"name": "Siemens", "url": "https://jobs.siemens.com/"},
        {"name": "Zalando", "url": "https://jobs.zalando.com/"}
    ];
    const skillListSize = 15;
    const totalJobs = ref(0);
    const skillCount = ref(0);
    const topSkills = ref<SkillListResponse>({ skills: [], size: 0 });

    onMounted(async () => {
        totalJobs.value = await JobService.getJobCount();
        skillCount.value = await SkillService.getSkillsCount();
        topSkills.value = await SkillService.getTopSkills(skillListSize);
    })
</script>


<template>
    <div class="about-page">

        <div class="page-header">
            <p class="page-eyebrow">Platform</p>
            <h1>About</h1>
        </div>

        <div class="page-body">

            <section class="card">
                <h2 class="section-label">Description</h2>
                <p class="body-text">
                    IT-JobScraper helps you find the best IT jobs available online quickly and easily.
                </p>
            </section>

            <hr class="divider" />

            <section class="card">
                <h2 class="section-label">Stats</h2>

                <div class="stat-grid">
                    <div class="stat-block">
                        <span class="stat-label">Total Jobs Listed</span>
                        <span class="stat-value">{{ totalJobs.toLocaleString() }}</span>
                    </div>
                    <div class="stat-block">
                        <span class="stat-label">Skills Tracked</span>
                        <span class="stat-value">{{ skillCount }}</span>
                    </div>
                    <div class="stat-block">
                        <span class="stat-label">Sites Scraped</span>
                        <span class="stat-value">{{ sources.length }}</span>
                    </div>
                </div>

                <hr class="divider-inner" />

                <h3 class="subsection-label">Top {{ skillListSize }} Most Looked-for Skills</h3>
                <ul class="skills-list">
                    <li
                        v-for="(item, index) in topSkills.skills"
                        :key="item.skill.id"
                        class="skill-item"
                    >
                        <span class="skill-rank">{{ String(index + 1).padStart(2, '0') }}</span>
                        <span class="skill-name">{{ item.skill.name }}</span>
                        <span class="skill-bar-wrap">
                            <span
                                class="skill-bar"
                                :style="{ width: `${(item.frequency * 100).toFixed(2)}%` }"
                            ></span>
                        </span>
                        <span class="skill-jobs">{{ item.job_count }} jobs</span>
                        <span class="skill-frequency">{{ (item.frequency * 100).toFixed(2) }}%</span>
                    </li>
                </ul>
            </section>

            <hr class="divider" />

            <section class="card">
                <h2 class="section-label">Sources</h2>
                <p class="body-text sources-intro">We scrape jobs from the following sources:</p>
                <ul class="sources-list">
                    <li v-for="source in sources" :key="source.name" class="source-item">
                        <a :href="source.url" target="_blank" rel="noopener" class="source-link">
                            <span class="source-name">{{ source.name }}</span>
                            <span class="source-arrow">↗</span>
                        </a>
                    </li>
                </ul>
            </section>

        </div>
    </div>
</template>


<style scoped>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .about-page {
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

    .subsection-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--color-text-muted);
        margin-bottom: var(--space-md);
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

    .divider-inner {
        height: 1px;
        background: var(--color-border-subtle);
        border: none;
        margin: var(--space-xl) 0;
    }

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

    .skills-list {
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .skill-item {
        display: grid;
        grid-template-columns: 28px 140px 1fr 72px 52px;
        align-items: center;
        gap: var(--space-md);
        padding: 10px 14px;
        border-radius: var(--radius-sm);
        transition: background var(--transition-fast);
    }

    .skill-item:hover {
        background: var(--color-surface-subtle);
    }

    .skill-rank {
        font-size: 11px;
        font-weight: 500;
        color: var(--color-text-muted);
        letter-spacing: 0.06em;
        font-variant-numeric: tabular-nums;
    }

    .skill-name {
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--color-text);
    }

    .skill-bar-wrap {
        height: 4px;
        background: var(--color-border-subtle);
        border-radius: var(--radius-pill);
        overflow: hidden;
    }

    .skill-bar {
        display: block;
        height: 100%;
        background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-accent) 100%);
        border-radius: var(--radius-pill);
        transition: width var(--transition-base);
    }

    .skill-jobs {
        font-size: 0.82rem;
        color: var(--color-text-muted);
        text-align: right;
        font-variant-numeric: tabular-nums;
    }

    .skill-frequency {
        font-size: 0.82rem;
        font-weight: 500;
        color: var(--color-primary);
        text-align: right;
        font-variant-numeric: tabular-nums;
        opacity: 0;
        transition: opacity var(--transition-base);
    }

    .skill-item:hover .skill-frequency {
        opacity: 1;
    }

    .sources-intro {
        margin-bottom: var(--space-lg);
    }

    .sources-list {
        list-style: none;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: var(--space-sm);
    }

    .source-link {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        border-radius: var(--radius-md);
        background: var(--color-surface-subtle);
        border: 1px solid var(--color-border);
        text-decoration: none;
        transition:
            background var(--transition-base),
            border-color var(--transition-base),
            box-shadow var(--transition-base),
            transform var(--transition-fast);
    }

    .source-link:hover {
        background: var(--color-primary);
        border-color: var(--color-primary);
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }

    .source-name {
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--color-text);
        transition: color var(--transition-base);
    }

    .source-link:hover .source-name {
        color: var(--color-surface);
    }

    .source-arrow {
        font-size: 0.85rem;
        color: var(--color-accent);
        opacity: 0;
        transform: translateY(3px);
        transition:
            opacity var(--transition-base),
            transform var(--transition-base);
    }

    .source-link:hover .source-arrow {
        opacity: 1;
        transform: translateY(0);
    }
</style>