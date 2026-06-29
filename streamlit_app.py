import streamlit as st

# -------------------------
# Snowflake connection
# -------------------------
conn = st.connection("snowflake")

st.title("Smoothie Orders 🍓")

# -------------------------
# Load fruit list
# -------------------------
df = conn.query("""
    SELECT FRUIT_NAME
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
""")

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

    if not name or len(ingredients) == 0:
        st.error("Please enter name and select fruits")
    else:

        ingredients_string = ", ".join(ingredients)

        sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (NAME_ON_ORDER, INGREDIENTS)
        VALUES
        ('{name}', '{ingredients_string}')
        """

        try:
            conn.query(sql)
            st.success("Order submitted 🍓")
        except Exception as e:
            st.error(f"Error: {e}")
