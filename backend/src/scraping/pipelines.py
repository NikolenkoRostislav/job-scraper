from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from itemadapter import ItemAdapter
from src.db.database import SessionLocal
from src.db.models import JobListing, Skill, JobListingSkill
from src.utils.parsers import parse_skill, parse_seniority_list


class JobscraperPipeline:
    def __init__(self):
        self.skill_cache = {}

    async def get_or_create_job(self, session, adapter):
        seniority_list = parse_seniority_list(adapter.get("seniority_levels", []))

        job = JobListing(
            title=adapter.get("title"),
            description=adapter.get("description"),
            location=adapter.get("location"),
            country=adapter.get("country"),
            seniority_levels=seniority_list,
            url=adapter.get("url")
        )
        session.add(job)
        try:
            await session.commit()
            await session.refresh(job)
            print(f"Saved job: {job.title}")
        except IntegrityError:
            await session.rollback()
            result = await session.execute(
                select(JobListing).where(JobListing.url == job.url)
            )
            job = result.scalar_one()
            print(f"Job already exists: {job.title}")
        return job

    async def get_or_create_skill(self, session, canonical_name, category): #this actually returns a skills id for caching purposes
        if canonical_name in self.skill_cache:
            return self.skill_cache[canonical_name]

        result = await session.execute(select(Skill).where(Skill.name == canonical_name))
        skill = result.scalar_one_or_none()

        if not skill:
            skill = Skill(name=canonical_name, category=category)
            session.add(skill)
            try:
                await session.commit()
                await session.refresh(skill)
            except IntegrityError:
                await session.rollback()
                result = await session.execute(select(Skill).where(Skill.name == canonical_name))
                skill = result.scalar_one()

        self.skill_cache[canonical_name] = skill.id
        return skill.id

    async def process_item(self, item, spider):
        print("\nPROCESSING ITEM\n")
        adapter = ItemAdapter(item)

        async with SessionLocal() as session:
            job = await self.get_or_create_job(session, adapter)

            skill_ids = []
            for raw_skill in adapter.get("skills", []):
                canonical_name, category = parse_skill(raw_skill)
                skill_id = await self.get_or_create_skill(session, canonical_name, category)
                skill_ids.append(skill_id)

            for skill_id in skill_ids:
                session.add(JobListingSkill(job_listing_id=job.id, skill_id=skill_id))
            try:
                await session.commit()
                print(f"Added {len(skill_ids)} skills to job")
            except IntegrityError:
                await session.rollback()

        return item
