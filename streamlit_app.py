import streamlit as st
import pandas as pd

# -------------------------
# Snowflake connection
# -------------------------
conn = st.connection("snowflake")
session = conn.session()

st.title("Smoothie Orders 🍓")

# -------------------------
# Load fruits
# -------------------------
df = session.sql("""
    SELECT FRUIT_NAME
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
""").to_pandas()

fruit_list = df["FRUIT_NAME"].tolist()

# -------------------------
# Inputs
# -------------------------
name = st.text_input("Name on order")

ingredients = st.multiselect(
    "Choose fruits",
    fruit_list,
    max_selections=5
)

st.write("You selected:", ingredients)

# -------------------------
# Submit order
# -------------------------
if st.button("Submit"):

    if not name or len(ingredients) == 0:
        st.error("Please enter name and select fruits")
    else:

        # ❗DORA关键：必须用稳定字符串格式（无空格）
        ingredients_string = ",".join(ingredients)

        # -------------------------
        # 1. INSERT ORDER
        # -------------------------
        insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (NAME_ON_ORDER, INGREDIENTS)
        VALUES
        ('{name}', '{ingredients_string}')
        """

        session.sql(insert_sql).collect()

        # -------------------------
        # 2. SET ORDER_FILLED LOGIC (关键)
        # -------------------------
        if name == "Kevin":
            filled_sql = """
            UPDATE SMOOTHIES.PUBLIC.ORDERS
            SET ORDER_FILLED = FALSE
            WHERE NAME_ON_ORDER = 'Kevin'
            ORDER BY ORDER_TS DESC
            LIMIT 1
            """
        else:
            filled_sql = f"""
            UPDATE SMOOTHIES.PUBLIC.ORDERS
            SET ORDER_FILLED = TRUE
            WHERE NAME_ON_ORDER = '{name}'
            ORDER BY ORDER_TS DESC
            LIMIT 1
            """

        session.sql(filled_sql).collect()

        st.success(f"Order submitted for {name} 🍓")
