import scrapy
from typing import Any
from scrapy.http import JsonRequest
from scrapy.crawler import CrawlerProcess


CATEGORIES = {
    "17092": "category_17092",
    "21439": "category_21439",
    "17038": "category_17038",
    "17053": "category_17053",
    "17014": "category_17014",
}

PAGE_SIZE = 20


class DecathlonProductsSpider(scrapy.Spider):

    name = "decathlon_products"

    allowed_domains = ["decathlon.in"]

    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "FEED_EXPORT_ENCODING": "utf-8",

        "FEEDS": {
            "decathlon_1000_products.csv": {
                "format": "csv",
                "overwrite": True,
            }
        }
    }

    async def start(self):

        for category_id in CATEGORIES:
            yield self.api_request(category_id, 0)

    def api_request(self, category_id, page):

        url = (
            f"https://www.decathlon.in/services/api/v1/"
            f"category/{category_id}"
        )

        payload = {
            "filters": {
                "inStock": ["1"]
            },
            "page": page,
            "totalProductsPerPage": PAGE_SIZE
        }

        return JsonRequest(
            url=url,
            data=payload,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Referer": "https://www.decathlon.in/",
                "Origin": "https://www.decathlon.in",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/142.0.0.0 Safari/537.36"
                )
            },
            callback=self.parse,
            cb_kwargs={
                "category_id": category_id
            }
        )

    def parse(self, response, category_id):

        print(
            f"STATUS: {response.status} | "
            f"CATEGORY: {category_id}"
        )

        if response.status != 200:
            print("REQUEST FAILED")
            print(response.text[:500])
            return

        data = response.json().get("data", {})

        current_page = int(data.get("page", 0))
        total_pages = int(data.get("totalPage", 1))

        print(
            f"CATEGORY {category_id} | "
            f"PAGE {current_page + 1}/{total_pages}"
        )

        for hit in data.get("hits", []):

            for product in hit.get("products", []):

                result = self.normalize_product(product)

                result["category_id"] = category_id

                yield result

        if current_page + 1 < total_pages:

            yield self.api_request(
                category_id,
                current_page + 1
            )

    @staticmethod
    def normalize_product(
        product: dict[str, Any]
    ) -> dict[str, Any]:

        price = product.get("price") or {}

        model_id = product.get("modelId")
        slug = product.get("slug")

        web_page = None

        if model_id and slug:
            web_page = (
                f"https://www.decathlon.in/p/"
                f"{model_id}/{slug}"
            )

        return {
            "objectID": product.get("objectID"),
            "modelId": model_id,
            "brand": product.get("brand"),
            "productName": product.get("productName"),
            "slug": slug,
            "web_page": web_page,
            "image": product.get("image"),
            "rating": product.get("rating"),
            "reviews": product.get("reviews"),
            "sellingPrice": price.get("sellingPrice"),
            "mrp": price.get("mrp"),
            "discount": price.get("discount"),
            "isExpressEligible": product.get(
                "isExpressEligible"
            )
        }


if __name__ == "__main__":

    process = CrawlerProcess()

    process.crawl(DecathlonProductsSpider)

    process.start()