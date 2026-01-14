from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from itemadapter import ItemAdapter
from src.db.database import SyncSessionLocal
from src.db.models import JobListing, Skill, JobListingSkill, ScrapeReport
from src.utils.parsers import parse_skill, parse_seniority_list
from src.utils.normalizer import remove_extra_spaces, normalize_string


class JobscraperPipeline:
    def __init__(self):
        self.skill_cache = {}
        self.session = None
        self.target_website = None

    def normalize_item(self, adapter):
        adapter["title"] = remove_extra_spaces(adapter.get("title"))
        adapter["description"] = remove_extra_spaces(adapter.get("description"))
        adapter["location"] = remove_extra_spaces(adapter.get("location"))
        adapter["country"] = normalize_string(adapter.get("country"))
        adapter["company"] = remove_extra_spaces(adapter.get("company"))
        return adapter

    def open_spider(self, spider):
        self.session = SyncSessionLocal()
        self.target_website = spider.name
        self.scraped_count = 0
        self.start_time = datetime.now(timezone.utc)

    def close_spider(self, spider):
        self.end_time = datetime.now(timezone.utc)

        try:
            scrape_report = ScrapeReport()
            scrape_report.target_website = self.target_website
            scrape_report.scrape_started_at = self.start_time
            scrape_report.scrape_finished_at = self.end_time
            scrape_report.total_jobs_scraped = self.scraped_count

            self.session.add(scrape_report)
            self.session.commit()
        except Exception as e:
            spider.logger.error(f"Failed to save scrape report: {e}")
            self.session.rollback()

        if self.session:
            self.session.close()

    def create_or_update_job(self, adapter, spider):
        seniority_list = parse_seniority_list(adapter.get("seniority_levels", []))

        result = self.session.execute(
            select(JobListing).where(JobListing.url == adapter.get("url"))
        )
        job = result.scalar_one_or_none()

        if job:
            changed = False

            fields = {  # I'll add support for checking seniority list changes later but it's always updated for now
                "title": adapter.get("title"),
                "description": adapter.get("description"),
                "location": adapter.get("location"),
                "country": adapter.get("country"),
                "company": adapter.get("company"),
            }

            for field, new_value in fields.items():
                if getattr(job, field) != new_value:
                    setattr(job, field, new_value)
                    changed = True

            if changed:
                setattr(job, "last_updated_at", datetime.now(timezone.utc))
                spider.logger.info(f"Updated job with url {job.url}")
            else:
                spider.logger.info(f"Job unchanged: {job.url}")
            setattr(job, "seniority_levels", seniority_list)
            setattr(job, "last_seen_at", datetime.now(timezone.utc))
        else:
            job = JobListing(
                title=adapter.get("title"),
                description=adapter.get("description"),
                location=adapter.get("location"),
                country=adapter.get("country"),
                company=adapter.get("company"),
                seniority_levels=seniority_list,
                url=adapter.get("url"),
            )
            self.session.add(job)
        self.session.flush()
        return job

    def get_or_create_skill(
        self, canonical_name, category
    ):  # this actually returns a skills id for caching purposes
        if canonical_name in self.skill_cache:
            return self.skill_cache[canonical_name]

        result = self.session.execute(select(Skill).where(Skill.name == canonical_name))
        skill = result.scalar_one_or_none()

        if not skill:
            skill = Skill(name=canonical_name, category=category)
            self.session.add(skill)
            self.session.flush()

        self.skill_cache[canonical_name] = skill.id
        return skill.id

    def try_link_skill_to_job(self, job_id, skill_id):
        result = self.session.execute(
            select(JobListingSkill).where(
                JobListingSkill.job_listing_id == job_id,
                JobListingSkill.skill_id == skill_id,
            )
        )
        link = result.scalar_one_or_none()
        if not link:
            self.session.add(JobListingSkill(job_listing_id=job_id, skill_id=skill_id))

    def process_item(self, item, spider):
        if not self.session:
            raise RuntimeError("Session not initialized")

        adapter = ItemAdapter(item)
        adapter = self.normalize_item(adapter)

        try:
            job = self.create_or_update_job(adapter, spider)

            skill_ids = []
            for raw_skill in adapter.get("skills", []):
                canonical_name, category = parse_skill(raw_skill)
                skill_id = self.get_or_create_skill(canonical_name, category)
                skill_ids.append(skill_id)

            for skill_id in skill_ids:
                self.try_link_skill_to_job(job.id, skill_id)

            self.session.commit()

        except IntegrityError as e:
            spider.logger.warning(f"Failed to add entry with URL: {adapter.get('url')}")
            spider.logger.warning(e)
            self.session.rollback()
        except Exception:
            self.session.rollback()

        self.scraped_count += 1
        return item
