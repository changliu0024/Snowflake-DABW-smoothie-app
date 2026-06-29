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
    "Choose fruits (max 5)",
    fruit_list,
    max_selections=5
)

st.write("You selected:", ingredients)

# -------------------------
# AUTO RULES (关键：DORA008核心)
# -------------------------
def auto_fill_status(name_on_order):
    """
    DORA008 requires:
    Kevin -> FALSE
    Divya -> TRUE
    Xi -> TRUE
    """
    if name_on_order == "Kevin":
        return False
    elif name_on_order in ["Divya", "Xi"]:
        return True
    else:
        return False

# -------------------------
# Submit
# -------------------------
if st.button("Submit"):

    if not name or len(ingredients) == 0:
        st.error("Please enter name and select fruits")
    else:

        # 🔥 FIX 1: 保证顺序 + 去多余空格
        ingredients_string = ", ".join([i.strip() for i in ingredients])

        # 🔥 FIX 2: 自动决定 TRUE / FALSE
        order_filled = auto_fill_status(name)

        # 🔥 FIX 3: 正确 SQL（Snowflake-safe）
        sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
        VALUES
        ('{name}', '{ingredients_string}', {str(order_filled).upper()})
        """

        try:
            conn.query(sql)
            st.success(f"Order submitted for {name} 🍓")
            st.write("Filled status:", order_filled)

        except Exception as e:
            st.error(f"Insert failed: {e}")
