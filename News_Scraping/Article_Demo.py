from newspaper import Article

url="https://www.ndtv.com/chennai-news/4-000-cops-at-chennai-stadium-today-amid-cauvery-protesters-ipl-threat-1835027?pfrom=home-topscroll"

article=Article(url)

article.download()

article.parse()

html_data=article.html

text_data=article.text

