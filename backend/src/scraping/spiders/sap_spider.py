from itertools import product
import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies.sap import SapStrategy


PAGE_SIZE = 25
PAGINATION_LIMIT = 20

DEPARTMENTS = [
    "Software-Design+and+Development",
    "Software-Development+Operations",
    "Software-Quality+Assurance",
    "Information+Technology",
]

COUNTRIES = {
    "AR": "Argentina",
    "AU": "Australia",
    "AT": "Austria",
    "BH": "Bahrain",
    "BE": "Belgium",
    "BR": "Brazil",
    "BG": "Bulgaria",
    "CA": "Canada",
    "CL": "Chile",
    "CN": "China",
    "CO": "Colombia",
    "HR": "Croatia",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "EG": "Egypt",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IN": "India",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IT": "Italy",
    "JP": "Japan",
    "KZ": "Kazakhstan",
    "MY": "Malaysia",
    "MX": "Mexico",
    "MA": "Morocco",
    "NL": "Netherlands",
    "NZ": "New Zealand",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PH": "Philippines",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SA": "Saudi Arabia",
    "RS": "Serbia",
    "SG": "Singapore",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "ZA": "South Africa",
    "KR": "South Korea",
    "ES": "Spain",
    "SE": "Sweden",
    "CH": "Switzerland",
    "TW": "Taiwan",
    "TH": "Thailand",
    "TR": "Türkiye",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "VN": "Vietnam",
    "US": "United States",
}


class SapSpider(BaseSpider):
    name = "sap"

    allowed_domains = ["jobs.sap.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = SapStrategy(countries_dict=COUNTRIES)

    async def start(self):
        for department, country in product(DEPARTMENTS, COUNTRIES.keys()):
            startrow = 0
            url = f"https://jobs.sap.com/search/?startrow={startrow}&optionsFacetsDD_department={department}&optionsFacetsDD_country={country}"

            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"startrow": startrow, "department": department, "country": country},
            )

    def parse(self, response):
        jobs = response.css("tr.data-row")

        if not jobs or response.meta["startrow"] >= PAGINATION_LIMIT * PAGE_SIZE:
            return

        for job in jobs:
            job_href = job.css("a.jobTitle-link::attr(href)").get(default="")
            if job_href:
                job_url = "https://jobs.sap.com" + job_href

                yield scrapy.Request(
                    job_url,
                    callback=self.parse_job,
                    meta={
                        "department": response.meta["department"],
                        "country": response.meta["country"],
                    },
                )

        next_row = response.meta["startrow"] + PAGE_SIZE
        yield scrapy.Request(
            f"https://jobs.sap.com/search/?startrow={next_row}&optionsFacetsDD_department={response.meta['department']}&optionsFacetsDD_country={response.meta['country']}",
            callback=self.parse,
            meta={
                "startrow": next_row,
                "department": response.meta["department"],
                "country": response.meta["country"],
            },
        )
