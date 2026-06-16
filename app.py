import json

import streamlit as st

from config import app_config
from web.stage_1_get import stage_1_get
from web.stage_2_edit import stage_2_edit
from web.stage_3_document import generate_word_live, show_confirm_panel

st.set_page_config(page_title="Генератор Отчетов", page_icon="📄", layout="wide")
st.title("Сбор данных из Figma 🎨")

if "final_data" not in st.session_state:
    st.session_state.run_generation = False  # Флаг процесса генерации документа
    st.session_state.show_confirm = False  # Флаг для диалогового окна
    st.session_state.final_data = None
    st.session_state.edited_df = None

    if app_config.AppEnv == "dev":
        with open("data/final_results.json", "r", encoding="utf-8") as file:
            st.session_state.ready_data = json.load(file)
    else:
        st.session_state.ready_data = None

if st.session_state.ready_data is None:
    stage_1_get()

if st.session_state.ready_data and not st.session_state.run_generation:
    stage_2_edit()
    if st.session_state.show_confirm:
        show_confirm_panel()
    elif st.button("📥 Сформировать Word", type="primary"):
        st.session_state.show_confirm = True
        st.rerun()


if st.session_state.run_generation:
    generate_word_live()
    if st.button("⬅️ Вернуться к редактированию таблицы", type="secondary"):
        st.session_state.run_generation = False
        st.rerun()
