import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import requests
from selectolax.lexbor import LexborHTMLParser

from config import app_config

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_file_data():
    """
    Получаем данные json дерева только верхнего уровня depth = 2
    """

    try:
        res = requests.get(
            f"https://api.figma.com/v1/files/{app_config.FigmaFileKey}/",
            headers={"X-Figma-Token": app_config.FigmaToken},
            params={"depth": 2},
        )
    except Exception as e:
        print(e)

    with open("figma_dump_3.json", "w") as file:
        file.write(res.text)


def get_all_articles():
    """
    Возвращает массив объектов
    [{
        "article": "123456",
        "count": 9
    },
    ...]
    """

    with open("figma_dump_3.json", "r") as file:
        data = json.load(file)

    all_articles = []
    for item in data["document"]["children"][0]["children"]:
        article_number = item["name"].split(" ")[0]

        if article_number.isdigit():
            all_articles.append(article_number)

    conuts_articles = Counter(all_articles)

    all_articles_list = []
    for article, count in conuts_articles.items():
        all_articles_list.append({"article": article, "count": count})

    return all_articles_list


def fetch_prodict_name(article):
    article_number = article["article"]

    try:
        res = requests.get(
            f"https://www.evruka.ru/img.php?idtov={article_number}",
            headers=HEADERS,
            timeout=5,
        )
        if res.status_code == 200:
            html_text = res.content.decode("windows-1251", errors="ignore")
            tree = LexborHTMLParser(html_text)
            article_name = tree.css_first("title").text()

            if article_name:
                article_name = article_name.split("/")[0].strip()
            else:
                article_name = "Название не найдено"
        else:
            article_name = f"Ошибка: Код {res.status_code}"
    except Exception as e:
        print(e)
        article_name = f"Ошибка: {str(e)}"

    return {"article": article_number, "name": article_name, "count": article["count"]}


def main():
    data = get_all_articles()

    final_results = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_prodict_name, data)
        final_results = list(results)

    with open("final_results.json", "w") as file:
        json.dump(final_results, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
