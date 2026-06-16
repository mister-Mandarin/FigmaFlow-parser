import json
import random
import re
import time
from collections import Counter

import requests
import streamlit as st

from config import app_config

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_file_data():
    """
    Получаем данные json дерева только верхнего уровня depth = 2
    """

    if app_config.AppEnv == "dev":
        with open("data/figma_dump_3.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    try:
        res = requests.get(
            f"https://api.figma.com/v1/files/{app_config.FigmaFileKey}/",
            headers={"X-Figma-Token": app_config.FigmaToken},
            params={"depth": 2},
        )
        res.raise_for_status()

        return res.json()
    except Exception as e:
        print(f"Ошибка при получении данных из Figma API: {str(e)}")


def get_all_articles(data):
    """
    Возвращает массив объектов
    [{
        "article": "123456",
        "count": 9
    },
    ...]
    """

    all_articles = []
    for item in data["document"]["children"][0]["children"]:
        article_number = item["name"].split(" ")[0]

        if article_number.isdigit():
            all_articles.append(article_number)

    counts_articles = Counter(all_articles)

    all_articles_list = []
    for article, count in counts_articles.items():
        all_articles_list.append({"article": article, "count": count})

    return all_articles_list


def fetch_product_name(article: dict) -> dict:
    article_number = article["article"]

    urls = [
        f"https://www.evruka.ru/img.php?idtov={article_number}",
        f"https://www.suvenirow.ru/show_good.php?idtov={article_number}",
    ]

    article_name = ""

    for url in urls:
        try:
            res = requests.get(url, headers=HEADERS, timeout=5)

            if res.status_code == 200:
                html_text = res.content.decode("windows-1251", errors="ignore")
                search_name = re.search(
                    r"<title>(.*?)</title>", html_text, re.IGNORECASE
                )

                if search_name:
                    parsed_name = search_name.group(1).split("/")[0].strip()

                    # Если имя не пустое и это не дефолтная страница ошибки самого сайта
                    if parsed_name and "ошибка" not in parsed_name.lower():
                        article_name = parsed_name
                        break

        except Exception as e:
            print(f"⚠️ Ошибка запроса к {url}: {e}")
            continue

    if not article_name:
        article_name = "Название не найдено (проверены все источники)"

    return {"article": article_number, "name": article_name, "count": article["count"]}


def get_final_data(data, progress_bar):
    final_results = []
    total = len(data)

    for i, item in enumerate(data):
        result = fetch_product_name(item)
        st.write(
            f"✅ Артикул {result['article']} - {result['name']} (Кол-во: {result['count']})"
        )
        final_results.append(result)

        progress_bar.progress((i + 1) / total)

    return final_results


def random_sleep():
    time.sleep(random.uniform(0.5, 3.0))


def main():
    pass


if __name__ == "__main__":
    main()
