from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from itemadapter import ItemAdapter
from src.db.database import SessionLocal
from src.db.models import JobListing, Skill, JobListingSkill
from src.utils.parsers import parse_skill, parse_seniority_list
from src.utils.normalizer import remove_extra_spaces, normalize_string


class JobscraperPipeline:
    def __init__(self):
        self.skill_cache = {}
        self.session = None

    def normalize_item(self, adapter):
        adapter["title"] = remove_extra_spaces(adapter.get("title"))
        adapter["description"] = remove_extra_spaces(adapter.get("description"))
        adapter["location"] = remove_extra_spaces(adapter.get("location"))
        adapter["country"] = normalize_string(adapter.get("country"))
        return adapter
    
    def open_spider(self, spider):
        self.session = SessionLocal()

    async def close_spider(self, spider):
        if self.session:
            await self.session.close()

    async def get_or_create_job(self, adapter, spider):
        seniority_list = parse_seniority_list(adapter.get("seniority_levels", []))

        result = await self.session.execute(
            select(JobListing).where(JobListing.url == adapter.get("url"))
        )
        job = result.scalar_one_or_none()

        if job:
            changed = False
            if job.title != adapter.get("title"):
                job.title = adapter.get("title")
                changed = True
            if job.description != adapter.get("description"):
                job.description = adapter.get("description")
                changed = True
            if job.location != adapter.get("location"):
                job.location = adapter.get("location")
                changed = True
            if job.country != adapter.get("country"):
                job.country = adapter.get("country")
                changed = True
            if job.seniority_levels != seniority_list:
                job.seniority_levels = seniority_list
                changed = True
            
            if changed:
                spider.logger.info(f"Updated job with url {job.url}")
                await self.session.flush()
            else:
                spider.logger.info(f"Job unchanged: {job.url}")
        else:
            job = JobListing(
                title=adapter.get("title"),
                description=adapter.get("description"),
                location=adapter.get("location"),
                country=adapter.get("country"),
                seniority_levels=seniority_list,
                url=adapter.get("url")
            )
            self.session.add(job)
            await self.session.flush()
        return job

    async def get_or_create_skill(self, canonical_name, category): #this actually returns a skills id for caching purposes
        if canonical_name in self.skill_cache:
            return self.skill_cache[canonical_name]

        result = await self.session.execute(select(Skill).where(Skill.name == canonical_name))
        skill = result.scalar_one_or_none()

        if not skill:
            skill = Skill(name=canonical_name, category=category)
            self.session.add(skill)
            await self.session.flush()

        self.skill_cache[canonical_name] = skill.id
        return skill.id
    
    async def try_link_skill_to_job(self, job_id, skill_id):
        result = await self.session.execute(
            select(JobListingSkill).where(
                JobListingSkill.job_listing_id == job_id,
                JobListingSkill.skill_id == skill_id
            )
        )
        link = result.scalar_one_or_none()
        if not link:
            self.session.add(JobListingSkill(job_listing_id=job_id, skill_id=skill_id))

    async def process_item(self, item, spider):
        if not self.session:
            raise RuntimeError("Session not initialized")
        
        adapter = ItemAdapter(item)
        adapter = self.normalize_item(adapter)

        try:
            job = await self.get_or_create_job(adapter, spider)

            skill_ids = []
            for raw_skill in adapter.get("skills", []):
                canonical_name, category = parse_skill(raw_skill)
                skill_id = await self.get_or_create_skill(canonical_name, category)
                skill_ids.append(skill_id)

            for skill_id in skill_ids:
                await self.try_link_skill_to_job(job.id, skill_id)

            await self.session.commit()
            
        except IntegrityError as e:
            spider.logger.warning(f"Failed to add entry with URL: {adapter.get('url')}")
            spider.logger.warning(e)
            await self.session.rollback()
        except Exception:
            await self.session.rollback()

        return item
