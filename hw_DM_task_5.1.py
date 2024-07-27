import pandas as pd

# Загрузка данных из JSON файла в DataFrame
df = pd.read_json(
    "D:/GB/Data_collection_and_markup/Lesson_5_Scrapy/books_scraper/books.json"
)

# Проверка первых нескольких строк DataFrame
print(df.head())
print("(-------------------------------)")

# Сортировка датафрейма по возрастанию цены
df_sorted = df.sort_values(by="price")

# Вывод всего отсортированного датафрейма
print(df_sorted)

# Вывод первых 10 строк отсортированного датафрейма
# print(df_sorted.head(10))
