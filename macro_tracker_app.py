
import streamlit as st
import pandas as pd

# Initialize session states
if "meal_log" not in st.session_state:
    st.session_state.meal_log = []

if "custom_foods" not in st.session_state:
    st.session_state.custom_foods = {}

if "daily_goals" not in st.session_state:
    st.session_state.daily_goals = {"Calories": 2000, "Protein": 150, "Carbs": 250, "Fats": 70}

if "body_weight_log" not in st.session_state:
    st.session_state.body_weight_log = []

# Sidebar for setting daily goals
st.sidebar.header("Set Daily Goals")
calories_goal = st.sidebar.number_input("Calories Goal", value=st.session_state.daily_goals["Calories"])
protein_goal = st.sidebar.number_input("Protein Goal", value=st.session_state.daily_goals["Protein"])
carbs_goal = st.sidebar.number_input("Carbs Goal", value=st.session_state.daily_goals["Carbs"])
fats_goal = st.sidebar.number_input("Fats Goal", value=st.session_state.daily_goals["Fats"])

if st.sidebar.button("Update Goals"):
    st.session_state.daily_goals = {
        "Calories": calories_goal,
        "Protein": protein_goal,
        "Carbs": carbs_goal,
        "Fats": fats_goal
    }
    st.sidebar.success("Goals updated!")

# Custom food entry
st.header("Add a Custom Food")

food_name = st.text_input("Food Name")
calories = st.number_input("Calories", min_value=0.0, step=1.0)
protein = st.number_input("Protein (g)", min_value=0.0, step=0.1)
carbs = st.number_input("Carbs (g)", min_value=0.0, step=0.1)
fats = st.number_input("Fats (g)", min_value=0.0, step=0.1)

if st.button("Add Food"):
    if food_name and food_name not in st.session_state.custom_foods:
        st.session_state.custom_foods[food_name] = {
            "Calories": calories,
            "Protein": protein,
            "Carbs": carbs,
            "Fats": fats
        }
        st.success(f"{food_name} added successfully!")
    else:
        st.error("Please enter a unique food name.")

# Meal logging section
st.header("Log a Meal")

available_foods = list(st.session_state.custom_foods.keys())
if available_foods:
    food_choice = st.selectbox("Select a food item:", available_foods)
    quantity = st.number_input("Enter quantity (multiplier)", min_value=0.1, step=0.1, value=1.0)

    if st.button("Log Meal"):
        food_info = st.session_state.custom_foods[food_choice]
        meal_entry = {
            "Food": food_choice,
            "Calories": food_info["Calories"] * quantity,
            "Protein": food_info["Protein"] * quantity,
            "Carbs": food_info["Carbs"] * quantity,
            "Fats": food_info["Fats"] * quantity,
            "Quantity": quantity
        }
        st.session_state.meal_log.append(meal_entry)
        st.success(f"{food_choice} logged!")
else:
    st.write("No foods available. Add a custom food first.")

# Display meal log
st.header("Meal Log")
if st.session_state.meal_log:
    meal_df = pd.DataFrame(st.session_state.meal_log)
    st.dataframe(meal_df)
else:
    st.write("No meals logged yet.")

# Progress Tracking
st.header("Daily Progress")

total_intake = {
    "Calories": sum(item["Calories"] for item in st.session_state.meal_log),
    "Protein": sum(item["Protein"] for item in st.session_state.meal_log),
    "Carbs": sum(item["Carbs"] for item in st.session_state.meal_log),
    "Fats": sum(item["Fats"] for item in st.session_state.meal_log)
}

progress = {
    "Calories": f"{total_intake['Calories']} / {st.session_state.daily_goals['Calories']}",
    "Protein": f"{total_intake['Protein']} / {st.session_state.daily_goals['Protein']}",
    "Carbs": f"{total_intake['Carbs']} / {st.session_state.daily_goals['Carbs']}",
    "Fats": f"{total_intake['Fats']} / {st.session_state.daily_goals['Fats']}"
}

progress_df = pd.DataFrame([progress])
st.dataframe(progress_df)

# Body Weight Tracking
st.header("Daily Body Weight Tracking")

weight = st.number_input("Enter your weight (lbs or kg)", min_value=0.0, step=0.1)
if st.button("Log Weight"):
    st.session_state.body_weight_log.append({"Weight": weight, "Day": len(st.session_state.body_weight_log) + 1})
    st.success("Weight logged successfully!")

# Display weight log
st.header("Weight Progress")
if st.session_state.body_weight_log:
    weight_df = pd.DataFrame(st.session_state.body_weight_log)
    st.line_chart(weight_df.set_index("Day"))
    st.dataframe(weight_df)
else:
    st.write("No weight data logged yet.")
