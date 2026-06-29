import streamlit as st
import pandas as pd

# NEW Snowflake connection system
conn = st.connection("snowflake")

st.title("Customize Your Smoothie 🍓")

# -------------------------
# Load data
# -------------------------
df = conn.query("SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS")

fruit_list = df["FRUIT_NAME"].tolist()

# -------------------------
# UI
# -------------------------
name = st.text_input("Name for your order")

ingredients = st.multiselect(
    "Choose fruits:",
    fruit_list,
    max_selections=5
)

# -------------------------
# Build string
# -------------------------
ingredients_string = ""

if ingredients:
    for f in ingredients:
        ingredients_string += f + ", "

# -------------------------
# Submit
# -------------------------
if st.button("Submit") and name and ingredients_string:

    sql = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS (NAME_ON_ORDER, INGREDIENTS)
    VALUES ('{name}', '{ingredients_string}')
    """

    conn.query(sql)
    st.success("Order submitted!")

st.write(st.secrets)
