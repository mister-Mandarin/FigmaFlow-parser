import streamlit as st

from config import app_config
from main import get_all_articles, get_file_data, get_final_data, random_sleep


def stage_1_get():
    figma_input = st.text_input(
        "Введи ссылку на файл Figma:",
        placeholder="Например: https://www.figma.com/design/sWaMIS1...",
    )

    if st.button("Загрузить и проверить данные", type="primary"):
        if not figma_input:
            st.warning("Лена, ты забыла ввести ссылку... 😅")
        else:
            with st.status("Идет магия... 🪄", expanded=True) as status:
                random_sleep()
                try:
                    st.write("📥 Получаю структуру из Figma...")
                    random_sleep()
                    app_config.parse_link_url(figma_input)
                    st.write(
                        f"✅ Ссылка распознана, ключ файла {app_config.FigmaFileKey}!"
                    )
                except ValueError:
                    status.update(
                        label="Ошибка в ссылке!", state="error", expanded=True
                    )
                    st.error(
                        "Кажется, ссылка неправильная. Проверь, скопирована ли она полностью."
                    )
                    st.stop()

                st.write("🔍 Получаю все данные из файла Figma...")
                try:
                    figma_data = get_file_data()
                    random_sleep()
                    st.write("✅ Данные успешно получены!")
                except Exception as e:
                    status.update(
                        label="Ошибка при получении данных!",
                        state="error",
                        expanded=True,
                    )
                    st.error(f"Проблема с Figma API: {str(e)}")
                    st.stop()

                st.write("🔍 Извлекаю артикулы...")
                articles_data = get_all_articles(figma_data)
                random_sleep()

                st.write(f"✅ Найдено {len(articles_data)} уникальных артикулов!")

                st.write("🌐 Иду на сайт за названиями...")
                # прогресс-бар
                progress_bar = st.progress(0)

                st.session_state.final_data = get_final_data(
                    articles_data, progress_bar
                )

                status.update(
                    label="Данные успешно загружены!", state="complete", expanded=False
                )
