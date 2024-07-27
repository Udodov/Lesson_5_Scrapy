import scrapy


class CountriesSpiderSpider(scrapy.Spider):
    name = "countries_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_sovereign_states"]

    def parse(self, response):
        rows = response.xpath("//table[contains(@class,'wikitable')][1]/tbody/tr")
        for row in rows:
            country_name = row.xpath(".//td[1]//a/text()").get()
            membership = row.xpath(".//td[contains(.,'UN')]/text()").get()
            sovereignty_dispute_info = row.xpath(".//td[3]/text()").get()
            country_status = row.xpath(".//td[4]/text()").get()
            link = row.xpath(".//td[1]//a/@href").get()  # Исправлено: правильный путь к ссылке

            # Добавим отладочную информацию
            self.log(
                f"Country Name: {country_name}, Membership: {membership}, Sovereignty Dispute Info: {sovereignty_dispute_info}, Country Status: {country_status}"
            )

            if country_name:  # Проверяем, что country_name не пустое
                yield response.follow(
                    url=response.urljoin(link) if link else "/wiki/Zambia",
                    callback=self.parse_country,
                    meta={
                        "country_name": country_name.strip(),
                        "membership": membership.strip() if membership else "",
                        "sovereignty_dispute_info": sovereignty_dispute_info.strip() if sovereignty_dispute_info else "",
                        "country_status": country_status.strip() if country_status else "",
                    },
                )

    def parse_country(self, response):
        capital = response.xpath("//table[contains(@class,'infobox ib-country vcard')]//th[contains(text(), 'Capital')]/following-sibling::td/a/text()").get()  # Исправлено: более точное извлечение столицы
        country_name = response.request.meta["country_name"]
        membership = response.request.meta["membership"]
        sovereignty_dispute_info = response.request.meta["sovereignty_dispute_info"]
        country_status = response.request.meta["country_status"]

        yield {
            "country_name": country_name,
            "capital": capital.strip() if capital else "",
            "membership": membership,
            "sovereignty_dispute_info": sovereignty_dispute_info,
            "country_status": country_status,
        }
