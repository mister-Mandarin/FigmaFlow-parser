from datetime import datetime

import streamlit as st

from main import random_sleep


@st.dialog("Проверка данных перед отправкой")
def confirm_data_dialog():
    st.warning("⚠️ **Точно ли данные проверены?**")
    st.write("Внимательно посмотри на артикулы, названия и количество слайдов.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Да, всё верно 👍", type="primary", use_container_width=True):
            print(f"внутри кнопки да вход {st.session_state.run_generation}")
            st.session_state.run_generation = True
            st.session_state.start_heavy_task = False
            print(f"внутри кнопки да вход {st.session_state.run_generation}")
            st.rerun()
    with col2:
        if st.button(
            "Нет, я перепроверю ✍️", type="secondary", use_container_width=True
        ):
            print(f"внутри кнопки нет вход {st.session_state.run_generation}")
            st.session_state.run_generation = False
            st.session_state.start_heavy_task = False
            print(f"внутри кнопки нет выход {st.session_state.run_generation}")

            st.rerun(scope="app")


def show_confirm_panel():
    """Inline-панель подтверждения (вместо модального диалога)."""
    with st.container(border=True):
        st.warning("⚠️ **Точно ли данные проверены?**")
        st.write("Внимательно посмотри на артикулы, названия и количество слайдов.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Да, всё верно 👍", type="primary", use_container_width=True):
                st.session_state.run_generation = True
                st.session_state.show_confirm = False
                st.rerun()
        with col2:
            if st.button(
                "Нет, я перепроверю ✍️", type="secondary", use_container_width=True
            ):
                st.session_state.show_confirm = False
                st.rerun()


def generate_word_live():
    st.session_state.run_generation = False
    st.subheader("📥 Процесс генерации документа")

    # Контейнер st.status красиво анимирует процесс выполнения шагов
    with st.status("Сборка Word файла...", expanded=True):
        st.write("🔄 **Шаг 1:** Получение актуальных данных из таблицы...")
        random_sleep()

        st.write("📝 **Шаг 2:** Инициализация структуры шаблона Word (строк:)...")
        random_sleep()

        st.write(
            "📊 **Шаг 3:** Заполнение финальной таблицы и нормализация нумерации..."
        )
        random_sleep()

        st.write("💾 **Шаг 4:** Финализация стилей и сохранение файла...")
        random_sleep()

        html_document = generate_word_table_native(st.session_state.ready_data)

        # 2. Переводим строку в байты (строго в utf-8)
        file_bytes = html_document.encode("utf-8")

        st.write("✅ Документ успешно сгенерирован!")

    now = datetime.now()

    st.download_button(
        label="💾 Скачать готовый Word",
        data=file_bytes,
        file_name=f"Отчет_{now.strftime('%Y-%m-%d_%H-%M-%S')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary",
        use_container_width=True,
        key="download_button",
    )


def generate_word_table_native(data_list):
    """Генерирует строку в формате HTML, оптимизированную для MS Word."""
    # Начало HTML-документа со специальными вордовскими пространствами имен
    html_template = """
    <html xmlns:o="urn:schemas-microsoft-com:office:office" 
          xmlns:w="urn:schemas-microsoft-com:office:word" 
          xmlns="http://www.w3.org/TR/REC-html40">
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type">
        <style type="text/css">
            table {
                border-collapse: collapse;
                width: 100%;
                font-family: "Arial", sans-serif;
                font-size: 10.5pt;
            }
            th, td {
                border: 1px solid #A0A0A0;
                padding: 8px 10px;
                vertical-align: middle;
            }
            th {
                background-color: #F2F2F2;
                font-weight: bold;
                text-align: center;
            }
            .center { text-align: center; }
            .left { text-align: left; }
        </style>
    </head>
    <body>
        <h2>Отчет по инфографике</h2>
        <br>
        <table>
            <thead>
                <tr>
                    <th style="width: 5%;">№</th>
                    <th style="width: 25%;">Наименование услуги</th>
                    <th style="width: 15%;">Артикул товара</th>
                    <th style="width: 30%;">Название товара</th>
                    <th style="width: 10%;">Количество слайдов</th>
                    <th style="width: 15%;">Стоимость услуг</th>
                </tr>
            </thead>
            <tbody>
    """

    # Динамически наполняем строки из твоего st.session_state.ready_data
    for i, row in enumerate(data_list, start=1):
        html_template += f"""
                <tr>
                    <td class="center">{i}.</td>
                    <td class="left">{row.get("job", "Разработка инфографики")}</td>
                    <td class="center">{row.get("article", "")}</td>
                    <td class="left">{row.get("name", "")}</td>
                    <td class="center">{row.get("count", 0)}</td>
                    <td class="center">{row.get("price", "")}</td>
                </tr>
        """

    # Закрываем теги
    html_template += """
            </tbody>
        </table>
    </body>
    </html>
    """

    return html_template
