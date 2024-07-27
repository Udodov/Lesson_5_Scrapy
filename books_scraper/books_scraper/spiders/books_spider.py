import scrapy

class BooksSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        for book in response.xpath("//article[@class='product_pod']"):
            try:
                title = book.xpath(".//h3/a/@title").get()
                price = book.xpath(".//div[@class='product_price']/p[@class='price_color']/text()").get()
                book_url = response.urljoin(book.xpath(".//h3/a/@href").get())
                
                # Преобразуем цену в float, удаляя символ валюты и пробелы
                price = float(price.replace('£', '').replace('Â', '').strip())

                # Переходим на страницу книги для извлечения описания и категории
                yield response.follow(book_url, self.parse_book_details, meta={'title': title, 'price': price})
            except (AttributeError, TypeError, ValueError, IndexError, KeyError) as e:
                self.logger.error(f"Error parsing book: {e}")

        # Переход к следующей странице
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_book_details(self, response):
        title = response.meta['title']
        price = response.meta['price']

        try:
            # Извлекаем количество товара в наличии
            in_stock_text = response.xpath("//p[@class='instock availability']/text()").getall()
            in_stock_text = ''.join(in_stock_text).strip()
            if 'In stock' in in_stock_text:
                try:
                    in_stock = int(in_stock_text.split('(')[1].split()[0])
                except (IndexError, ValueError):
                    in_stock = 0
            else:
                in_stock = 0

            # Извлекаем описание
            description_tag = response.xpath("//meta[@name='description']/@content").get()
            description = description_tag.strip() if description_tag else "No description available"

            # Извлекаем категорию
            category_tag = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()
            category = category_tag.strip() if category_tag else "Unknown"

            # Извлекаем рейтинг книги
            star_rating_class = response.xpath("//p[contains(@class, 'star-rating')]/@class").get().split()[-1]
            rating_map = {
                'One': 1,
                'Two': 2,
                'Three': 3,
                'Four': 4,
                'Five': 5
            }
            rating = rating_map.get(star_rating_class, 0)

            yield {
                'title': title,
                'price': price,
                'in_stock': in_stock,
                'description': description,
                'category': category,
                'rating': rating
            }
        except (AttributeError, TypeError, ValueError, IndexError, KeyError) as e:
            self.logger.error(f"Error parsing book details: {e}")