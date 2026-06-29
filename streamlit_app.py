# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Title
st.title("Customize Your Smoothie! :balloon:")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Session
session = get_active_session()

# Name input
name_on_order = st.text_input("Name for your order:")

# Fruit list
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Show selection
if ingredients_list:
    st.write("You selected:")
    st.write(ingredients_list)

# Build string
ingredients_string = ""

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

    ingredients_string = ingredients_string[:-2]

# Build SQL
my_insert_stmt = ""

if name_on_order and ingredients_string:
    my_insert_stmt = (
        "insert into smoothies.public.orders(name_on_order, ingredients) "
        "values ('" + name_on_order + "', '" + ingredients_string + "')"
    )

    st.write(my_insert_stmt)

# Submit
submit = st.button("Submit Order")

if submit and name_on_order and ingredients_string:
    session.sql(my_insert_stmt).collect()

    st.success(
        f"Thanks {name_on_order}, your smoothie is ordered! 🥤",
        icon="✅"
    )
