from datetime import datetime, timezone

from scrapy import signals
from itemadapter import ItemAdapter

from core.database import SessionLocal
from shared.schemas import JobCreate
from shared.services import SkillService, JobService, ScrapeReportService
from shared.utils import parse_skill, parse_seniority_list, remove_extra_spaces, normalize_string


class JobscraperPipeline:
    def __init__(self):
        self.skill_cache = {}
        self.target_website = None

    def normalize_item(self, adapter):
        adapter["title"] = remove_extra_spaces(adapter.get("title"))
        adapter["description"] = remove_extra_spaces(adapter.get("description"))
        adapter["location"] = remove_extra_spaces(adapter.get("location"))
        adapter["country"] = normalize_string(adapter.get("country"))
        adapter["company"] = remove_extra_spaces(adapter.get("company"))
        return adapter
    
    @classmethod
    def from_crawler(cls, crawler):
        pipe = cls()
        crawler.signals.connect(pipe.spider_closed, signal=signals.spider_closed)
        return pipe

    def open_spider(self, spider):
        self.target_website = spider.name
        self.start_time = datetime.now(timezone.utc)

    async def spider_closed(self, spider, reason):
        async with SessionLocal() as session:
            stats = spider.crawler.stats.get_stats()

            try:
                await ScrapeReportService.create_scrape_report(
                    db=session,
                    target_website=self.target_website,
                    scrape_start_time=self.start_time,
                    scrape_stats=stats,
                    end_reason=reason
                )
            except Exception as e:
                spider.logger.error(f"Failed to save scrape report: {e}")
                await session.rollback()

    async def process_item(self, item, spider):
        async with SessionLocal() as session:
            adapter = ItemAdapter(item)
            adapter = self.normalize_item(adapter)

            try:
                seniority_list = parse_seniority_list(adapter.get("seniority_levels"))
                job_data = JobCreate(
                    url=adapter.get("url"),
                    title=adapter.get("title"),
                    description=adapter.get("description"),
                    location=adapter.get("location"),
                    country=adapter.get("country"),
                    company=adapter.get("company"),
                    home_office=adapter.get("home_office"),
                    source_website=self.target_website,
                    seniority_levels=seniority_list,
                )
                result = await JobService.create_or_update_job(session, job_data)
                job = result["job"]
                changed = result["changed"]
                if changed:
                    spider.logger.info(f"Updated job with URL: {job_data.url}")

                skill_ids = []
                for raw_skill in adapter.get("skills", []):
                    canonical_name, category = parse_skill(raw_skill)
                    if canonical_name in self.skill_cache:
                        skill_id = self.skill_cache[canonical_name]
                    else:
                        skill = await SkillService.create_skill(session, canonical_name, category)
                        skill_id = skill.id
                        self.skill_cache[canonical_name] = skill_id
                    skill_ids.append(skill_id)

                for skill_id in skill_ids:
                    await SkillService.link_skill_to_job(session, job.id, skill_id)
            except Exception as e:
                spider.logger.warning(f"Encountered error while adding entry with URL: {adapter.get('url')} \nError: {e}")
                await session.rollback()

            return item
