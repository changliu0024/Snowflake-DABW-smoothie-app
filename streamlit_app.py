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
# 修复核心：确保插入了所有必需的列（特别是 ORDER_FILLED 和 ORDER_TS）
# 使用 ? 占位符进行参数化查询，防止 SQL 注入和语法错误
if st.button("Submit") and name and ingredients:

    ingredients_string = ", ".join(ingredients)

    # 构造 SQL，显式插入 ORDER_FILLED 为 FALSE (默认未完成)
    # 并使用 CURRENT_TIMESTAMP() 填入时间戳
    sql = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS 
        (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
        VALUES (?, ?, FALSE, CURRENT_TIMESTAMP())
    """
    
    # 使用 session.sql 配合 collect() 执行，通过元组传入参数
    session.sql(sql, params=(name, ingredients_string)).collect()

    st.success(f"Order for {name} submitted 🍓")
