import streamlit as st
import snowflake.connector

conn = snowflake.connector.connect(
    account=st.secrets["snowflake"]["account"],
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    role=st.secrets["snowflake"]["role"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"]
)

cur = conn.cursor()

st.title("Smoothie Orders 🍓")

# Load fruits
cur.execute("SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
fruit_list = [r[0] for r in cur.fetchall()]

name = st.text_input("Name on order")

ingredients = st.multiselect("Choose fruits", fruit_list, max_selections=5)

# DORA SAFE STRING (IMPORTANT)
ingredients_string = ",".join(ingredients)

if st.button("Submit") and name and ingredients_string:

    sql = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS (NAME_ON_ORDER, INGREDIENTS)
    VALUES ('{name}', '{ingredients_string}')
    """

    cur.execute(sql)
    st.success("Order submitted ✅")
