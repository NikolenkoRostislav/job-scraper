import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies import SiemensStrategy


PAGE_SIZE = 6
PAGINATION_LIMIT = 30


class SiemensSpider(BaseSpider):
    name = "siemens"

    allowed_domains = ["jobs.siemens.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = SiemensStrategy()

    async def start(self):
        folder_offset = 0
        url = f"https://jobs.siemens.com/en_US/externaljobs/SearchJobs/?folderRecordsPerPage={PAGE_SIZE}&folderOffset={folder_offset}"

        yield scrapy.Request(url, callback=self.parse, meta={"folder_offset": folder_offset})

    def parse(self, response):
        job_hrefs = response.css("a.button.button--primary::attr(href)").getall()

        if (not job_hrefs or response.meta["folder_offset"] >= PAGINATION_LIMIT * PAGE_SIZE):
            return

        yield from self.job_requests(
            response=response,
            job_links=job_hrefs,
        )

        next_folder = response.meta["folder_offset"] + PAGE_SIZE
        yield scrapy.Request(
            f"https://jobs.siemens.com/en_US/externaljobs/SearchJobs/?folderRecordsPerPage={PAGE_SIZE}&folderOffset={next_folder}",
            callback=self.parse,
            meta={"folder_offset": next_folder},
        )
