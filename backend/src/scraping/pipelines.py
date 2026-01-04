from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from itemadapter import ItemAdapter
from src.db.database import SessionLocal
from src.db.models import JobListing, Skill, JobListingSkill
from src.utils.skill_parser import parse_skill


class JobscraperPipeline:
    def __init__(self):
        self.skill_cache = {}

    async def process_item(self, item, spider):
        print("\n PROCESSING ITEM \n")
        
        adapter = ItemAdapter(item)
        async with SessionLocal() as session:
            job = JobListing(
                title=adapter.get('title'),
                description=adapter.get('description'),
                location=adapter.get('location'),
                seniority_levels=adapter.get('seniority_levels'),
                url=adapter.get('url')
            )
            session.add(job)
            try:
                await session.commit()
                await session.refresh(job)
                print(f"Saved job: {job.title}")
            except IntegrityError:
                await session.rollback()
                result = await session.execute(select(JobListing).where(JobListing.url == job.url))
                job = result.scalar_one()
                print(f"Job already exists: {job.title}")

            skills = []
            for raw_skill in adapter.get('skills', []):
                canonical_name, category = parse_skill(raw_skill)

                if canonical_name in self.skill_cache:
                    skill = self.skill_cache[canonical_name]
                    skills.append(skill)
                    continue

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

                skills.append(skill)
                self.skill_cache[canonical_name] = skill

            for skill in skills:
                session.add(JobListingSkill(job_listing_id=job.id, skill_id=skill.id))
            try:
                await session.commit()
                print(f"Added {len(skills)} skills to job")
            except IntegrityError:
                await session.rollback()
        
        return item
