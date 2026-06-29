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
if st.button("Submit") and name and ingredients:

    ingredients_string = ", ".join(ingredients)

    # ❗正确 Snowflake SQL（不能用 %s）
    sql = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS
    (NAME_ON_ORDER, INGREDIENTS)
    VALUES
    ('{name}', '{ingredients_string}')
    """

    session.sql(sql).collect()

    st.success("Order submitted 🍓")
