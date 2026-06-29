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
        st.error("请确保输入了名字并选择了水果。")
    else:
        ingredients_string = ", ".join(ingredients)
        
        # 修复 SQL：只插入 NAME 和 INGREDIENTS
        # ORDER_UID 使用 DEFAULT (自动序列)
        # ORDER_FILLED 使用 FALSE (默认值)
        # ORDER_TS 使用 CURRENT_TIMESTAMP (默认值)
        
        sql = """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS 
            (NAME_ON_ORDER, INGREDIENTS)
            VALUES (?, ?)
        """
        
        try:
            # 执行查询
            session.sql(sql, params=(name, ingredients_string)).collect()
            st.success(f"订单已为 {name} 成功提交! 🍓")
        except Exception as e:
            # 打印详细错误方便排查
            st.error(f"插入失败: {e}")
