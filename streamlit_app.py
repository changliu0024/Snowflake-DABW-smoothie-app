import streamlit as st
import pandas as pd

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

order_filled = st.checkbox("Mark as filled")

# -------------------------
# Preview
# -------------------------
if ingredients:
    st.write("You selected:", ingredients)

# -------------------------
# Submit
# -------------------------
if st.button("Submit") and name and ingredients:

    # ⚠️ IMPORTANT: EXACT format (DORA depends on this)
    ingredients_string = ", ".join(ingredients)

    sql = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS
    (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
    VALUES
    ('{name}', '{ingredients_string}', {str(order_filled).upper()})
    """

    session.sql(sql).collect()

    st.success("Order submitted 🍓")

# -------------------------
# Show pending orders (optional UI)
# -------------------------
st.divider()

orders_df = session.sql("""
SELECT *
FROM SMOOTHIES.PUBLIC.ORDERS
ORDER BY ORDER_TS DESC
""").to_pandas()

st.dataframe(orders_df)
