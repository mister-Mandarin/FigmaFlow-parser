import streamlit as st


def rebuild_to_final_data(edited_df_list):
    return [
        {
            "job": str(row.get("Наименование услуги") or ""),
            "article": str(row.get("Артикул товара") or ""),
            "name": str(row.get("Название товара") or ""),
            "count": int(row.get("Количество слайдов") or 0),
            "price": str(row.get("Стоимость услуг") or ""),
        }
        for row in edited_df_list
    ]


def stage_2_edit():
    st.subheader("📋 Проверь данные перед созданием отчета")
    st.info(
        """
        При двойном клике на любое поле можно изменить его значение.\n
        Выбери строку и нажми Delete, чтобы удалить ее.\n
        Добавь новую строку, нажав на "+" в последней строке таблицы.\n
        """
    )

    table_rows = []
    for i, item in enumerate(st.session_state.ready_data, start=1):
        table_rows.append(
            {
                "№": f"{i}.",
                "Наименование услуги": item.get("job", "Разработка инфографики"),
                "Артикул товара": item["article"],
                "Название товара": item["name"],
                "Количество слайдов": item["count"],
                "Стоимость услуг": item.get("price", ""),
            }
        )

    st.session_state.final_data = table_rows

    edited_df = st.data_editor(
        table_rows,
        width="stretch",
        disabled=["№"],
        num_rows="dynamic",
        key="my_data_table",
        column_config={
            "Наименование услуги": st.column_config.TextColumn("Наименование\nуслуги"),
            "Количество слайдов": st.column_config.NumberColumn("Количество\nслайдов"),
            "Стоимость услуг": st.column_config.TextColumn("Стоимость\nуслуг"),
        },
    )

    new_ready_data = rebuild_to_final_data(edited_df)

    if new_ready_data != st.session_state.ready_data:
        st.session_state.ready_data = new_ready_data
        st.rerun()
