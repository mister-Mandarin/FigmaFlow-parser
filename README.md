# Спринт 1. Коннект к Figma API и выгрузка дерева документа

**Цель:** Скрипт получает JSON-структуру макета из Figma API и сохраняет в файл.

## Задачи

1. Создать проект с venv, `main.py`, `.env`
2. В `.env` сохранить: `FIGMA_TOKEN` и `FILE_KEY`
3. Реализовать GET-запрос к `https://api.figma.com/v1/files/{FILE_KEY}` с токен в заголовке `X-Figma-Token`
4. Обработать ошибки (сеть, 401, 404)
5. Сохранить JSON в `figma_dump.json`

## Зависимости

```bash
pip install requests python-dotenv
```
