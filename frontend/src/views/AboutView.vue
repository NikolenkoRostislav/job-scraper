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
    const skillListSize = 16;
    const totalJobs = ref(0);
    const topSkills = ref<SkillListResponse>({ skills: [], size: 0 });

    onMounted(async () => {
        totalJobs.value = await JobService.getJobCount();
        topSkills.value = await SkillService.getTopSkills(skillListSize);
    })
</script>


<template>
    <h1>About</h1>

    <section>
        <h2>Description</h2>
        <p>
            IT-JobScraper helps you find the best IT jobs available online quickly and easily. 
        </p>
    </section>

    <section>
        <h2>Stats</h2>
        <h3>Total Jobs on Website:</h3>
        <p>{{ totalJobs }}</p>
        
        <h3>Top {{ skillListSize }} Most Looked-for Skills</h3>
        <ul>
            <li v-for="item in topSkills.skills" :key="item.skill.id" class="skill-item">
                <b>{{ item.skill.name }}</b>:
                {{ item.job_count }} jobs
                <span class="frequency">({{ (item.frequency * 100).toFixed(2) }}% of all jobs)</span>
            </li>
        </ul>
    </section>

    <section>
        <h2>Sources</h2>
        <p>We scrape jobs from the following sources:</p>
        <ul>
            <li v-for="source in sources" :key="source.name"><a :href="source.url">{{ source.name }}</a></li>
        </ul>
    </section>
</template>


<style scoped>
    .skill-item .frequency {
        opacity: 0;
        transition: opacity 0.2s;
        margin-left: 4px;
    }

    .skill-item:hover .frequency {
        opacity: 1;
    }
</style>
