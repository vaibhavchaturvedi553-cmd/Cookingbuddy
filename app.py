
import streamlit as st
import requests

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Cooking Buddy",
    page_icon="🍳",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""

<style>

/* Main background */
.stApp {
    background: #090909;
    color: #f5f5f5;
}

/* Main title */
.main-title {
    text-align: center;
    color: #ff9f43;
    font-size: 46px;
    font-weight: 800;
    letter-spacing: 1px;
    text-shadow: 0 0 15px rgba(255, 159, 67, 0.3);
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #b5b5b5;
    font-size: 17px;
}

/* General text */
.stApp p,
.stApp label,
.stApp span,
.stApp li {
    color: #e5e5e5;
}

/* Section headings */
.stApp h1,
.stApp h2,
.stApp h3 {
    color: #ffad60;
}

/* Recipe cards */
.recipe-card {
    background: #171717;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #353535;
    margin-bottom: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.4);
}

/* Section title */
.section-title {
    color: #ffad60;
    font-size: 24px;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ff9f43, #ff6b35);
    color: #111111 !important;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-weight: bold;
    transition: all 0.3s ease;
}

/* Button hover effect */
.stButton > button:hover {
    background: linear-gradient(135deg, #ffc078, #ff8c42);
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(255, 140, 66, 0.35);
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    background-color: #1c1c1c;
    color: white;
    border-radius: 9px;
}

/* Radio buttons */
.stRadio label {
    color: #ffffff !important;
}

/* Dividers */
hr {
    border-color: #333333 !important;
}

/* Images */
.stImage img {
    border-radius: 15px;
    border: 1px solid #383838;
    box-shadow: 0 5px 20px rgba(0,0,0,0.5);
}

/* Success messages */
.stAlert {
    border-radius: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #888888;
    padding: 25px;
    font-size: 14px;
}

/* Links */
a {
    color: #ffad60 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111111;
}

</style>

""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🍳 Cooking Buddy</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal AI-style cooking assistant</div>',
    unsafe_allow_html=True
)

st.write("")

st.info(
    "Discover recipes, check kitchen utensils, "
    "and learn how to prepare your favourite meals!"
)

st.markdown("---")


# ---------------- RECIPE DATABASE ----------------

veg_recipes = {
    "Potato Fry": "Pan",
    "Tomato Soup": "Saucepan",
    "Carrot Cake": "Oven",
    "Vegetable Curry": "Pan",
    "Paneer Butter Masala": "Pan",
    "Mushroom Soup": "Saucepan"
}

nonveg_recipes = {
    "Chicken Curry": "Pan",
    "Boiled Egg": "Saucepan",
    "Grilled Fish": "Oven",
    "Chicken Soup": "Saucepan",
    "Fish Curry": "Pan"
}


# ---------------- USER INPUT ----------------

st.subheader("🥗 Choose Your Food Preference")

food = st.radio(
    "Select food type:",
    ["Veg", "Non-Veg"],
    horizontal=True
)

if food == "Veg":
    recipe_list = veg_recipes
else:
    recipe_list = nonveg_recipes

col1, col2 = st.columns(2)

with col1:
    recipe_name = st.selectbox(
        "🍽️ Select Your Recipe",
        list(recipe_list.keys())
    )

    required_utensil = recipe_list[recipe_name]

with col2:
    utensils = st.multiselect(
        "🔪 Available Kitchen Utensils",
        ["Pan", "Saucepan", "Oven", "Knife",
         "Spoon", "Pressure Cooker", "Grater"]
    )

st.markdown("---")


# ---------------- RECIPE FUNCTION ----------------

def get_recipe(recipe):

    url = "https://www.themealdb.com/api/json/v1/1/search.php"

    try:
        response = requests.get(
            url,
            params={"s": recipe},
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("meals"):
            return data["meals"][0]

        return None

    except requests.exceptions.RequestException:
        st.error("Unable to connect to the recipe API. Please try again.")
        return None

    except ValueError:
        st.error("Invalid response received from the recipe API.")
        return None


# ---------------- GET RECIPE BUTTON ----------------

if st.button("🍳 Get My Recipe", use_container_width=True):

    if required_utensil not in utensils:

        st.error(
            f"You need a {required_utensil} to prepare {recipe_name}."
        )

        st.warning("Please select the required kitchen utensil.")

    else:

        st.success("Perfect! You have selected the correct utensil.")

        with st.spinner("Finding your delicious recipe..."):

            meal = get_recipe(recipe_name)

        if meal:

            st.markdown("---")

            st.header("🍽️ Your Recipe")

            col1, col2 = st.columns([1, 1])

            with col1:
                st.image(
                    meal["strMealThumb"],
                    use_container_width=True
                )

            with col2:
                st.subheader(meal["strMeal"])

                st.write(
                    "**Category:**",
                    meal.get("strCategory", "Not available")
                )

                st.write(
                    "**Cuisine:**",
                    meal.get("strArea", "Not available")
                )

                st.write(
                    "**Food Type:**",
                    food
                )

                st.markdown("### Required Utensil")

                st.success(required_utensil)

                if meal.get("strYoutube"):
                    st.link_button(
                        "▶ Watch Cooking Video",
                        meal["strYoutube"]
                    )

            st.markdown("---")

            # INGREDIENTS

            st.markdown(
                '<div class="section-title">🥕 Ingredients</div>',
                unsafe_allow_html=True
            )

            ingredients = []

            for i in range(1, 21):

                ingredient = meal.get(
                    f"strIngredient{i}", ""
                )

                measure = meal.get(
                    f"strMeasure{i}", ""
                )

                if ingredient and ingredient.strip():

                    ingredients.append(
                        (ingredient.strip(), measure.strip())
                    )

            col1, col2 = st.columns(2)

            for index, (ingredient, measure) in enumerate(ingredients):

                with (col1 if index % 2 == 0 else col2):
                    st.write(
                        f"☑️ **{ingredient}** — {measure}"
                    )

            st.markdown("---")

            # INSTRUCTIONS

            st.markdown(
                '<div class="section-title">👨‍🍳 Cooking Instructions</div>',
                unsafe_allow_html=True
            )

            instructions = meal.get(
                "strInstructions",
                "Instructions not available."
            )

            steps = [
                step.strip()
                for step in instructions.split(".")
                if step.strip()
            ]

            for index, step in enumerate(steps, 1):

                st.markdown(
                    f"**Step {index}:** {step}."
                )

            st.markdown("---")

            st.success(
                "Enjoy your delicious homemade meal! ❤️"
            )

        else:

            st.warning(
                "Sorry! This recipe was not found in the database."
            )


# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    '<div class="footer">'
    'Made with ❤️ | Cooking Buddy | Student Project'
    '</div>',
    unsafe_allow_html=True
)
