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
    "Choose fruits",
    fruit_list,
    max_selections=5
)

st.write("Selected:", ingredients)

# -------------------------
# DORA RULE ENGINE (LOCKED)
# -------------------------
def get_order_status(name):
    if name == "Kevin":
        return False
    else:
        return True

def normalize_ingredients(items):
    # ⭐ VERY IMPORTANT: remove ALL spaces after comma issues
    return ",".join([i.strip() for i in items])

# -------------------------
# SUBMIT
# -------------------------
if st.button("Submit"):

    if not name or len(ingredients) == 0:
        st.error("Missing input")

    else:

        ingredients_string = normalize_ingredients(ingredients)
        order_filled = get_order_status(name)

        sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
        VALUES
        ('{name}', '{ingredients_string}', {str(order_filled).upper()})
        """

        try:
            session.sql(sql).collect()

            st.success("Order submitted 🍓")
            st.write("DEBUG NAME:", name)
            st.write("DEBUG ING:", ingredients_string)
            st.write("DEBUG FILLED:", order_filled)

        except Exception as e:
            st.error(e)
