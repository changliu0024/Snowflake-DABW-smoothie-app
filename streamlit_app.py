import streamlit as st

# -------------------------
# CONNECTION
# -------------------------
conn = st.connection("snowflake")
session = conn.session()

st.title("Smoothie Orders 🍓")

# -------------------------
# LOAD FRUITS
# -------------------------
df = session.sql("""
    SELECT FRUIT_NAME
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
""").to_pandas()

fruit_list = df["FRUIT_NAME"].tolist()

# -------------------------
# INPUTS
# -------------------------
name = st.text_input("Name on order")

ingredients = st.multiselect(
    "Choose fruits (max 5)",
    fruit_list,
    max_selections=5
)

st.write("You selected:", ingredients)

# -------------------------
# FORMAT (IMPORTANT FOR DORA)
# -------------------------
def format_ingredients(items):
    return " ".join([i.strip() for i in items])

# -------------------------
# ORDER STATUS RULE (DORA REQUIRED)
# -------------------------
def is_order_filled(name):
    return name in ["Divya", "Xi"]

# -------------------------
# SUBMIT
# -------------------------
if st.button("Submit"):

    if not name or len(ingredients) == 0:
        st.error("Missing input")

    else:

        ingredients_string = format_ingredients(ingredients)
        order_filled = is_order_filled(name)

        sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
        VALUES
        ('{name}', '{ingredients_string}', {order_filled})
        """

        try:
            session.sql(sql).collect()
            st.success("Order submitted 🍓")

        except Exception as e:
            st.error(f"Insert failed: {e}")
