import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://calorizator.ru/product"

headers = {
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

# req = requests.get(url, headers=headers)
# src = req.text
#
#
# with open('index.html', 'w', encoding='utf-8') as file:
#    file.write(src)

# with open('index.html', 'r', encoding='utf-8') as file:
#    src = file.read()
#
# soup = BeautifulSoup(src, "lxml")
# all_ul = soup.find_all(class_='product')
# z = []
# for i in all_ul:
#    z.extend(i.find_all('a'))
#
# all_categories_dict = {}
#
# for item in range(len(z)-5):
#    item_text = z[item].text
#    item_href = "https://calorizator.ru/" + z[item].get("href")
#
#    all_categories_dict[item_text] = item_href
#
# with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
#    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open('all_categories_dict.json', 'r', encoding='utf-8') as file:
    all_categories = json.load(file)

count = 0
iteration_count = int(len(all_categories)) - 1
print(f"всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():

    category_name = category_name.replace(' ', '_')

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", "r", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    table_head = soup.find(class_="views-table").find("tr").find_all("th")

    product = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text
    calories = table_head[5].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                product,
                proteins,
                fats,
                carbohydrates,
                calories,
            )
        )

    products_data = soup.find(class_="views-table").find("tbody").find_all("tr")
    product_info =[]
    for item in products_data:
        product_tds = item.find_all("td")

        title = product_tds[1].find("a").text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text
        calories = product_tds[5].text

        product_info.append(
            {
                "title": title,
                "proteins": proteins,
                "fats": fats,
                "carbohydrates": carbohydrates,
                "calories": calories,
            }
        )
        with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    title,
                    proteins,
                    fats,
                    carbohydrates,
                    calories,
                )
            )

    count += 1
    print(f"# итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итераций: {iteration_count}")
    sleep(random.randrange(2,4))
