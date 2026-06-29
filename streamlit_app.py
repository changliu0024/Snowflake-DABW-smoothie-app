import streamlit as st
import pandas as pd

# -------------------------
# Snowflake connection
# -------------------------
conn = st.connection("snowflake")
session = conn.session()

st.title("Smoothie Orders 🍓")

# -------------------------
# Load fruit list
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

if ingredients:
    st.write("You selected:", ingredients)

# -------------------------
# Submit
# -------------------------
if st.button("Submit"):

    if not name or not ingredients:
        st.error("Please enter name and select fruits.")
    else:

        # ⭐ DORA关键修复：必须严格加 ", "（逗号+空格）
        ingredients_string = ", ".join(ingredients)

        sql = """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
            (NAME_ON_ORDER, INGREDIENTS)
            VALUES (?, ?)
        """

        try:
            session.sql(sql, params=(name, ingredients_string)).collect()
            st.success(f"Order submitted for {name} 🍓")

        except Exception as e:
            st.error(f"Insert failed: {e}")
