
import streamlit as st
import pandas as pd

# Initialize session state for meal log
if "meal_log" not in st.session_state:
    st.session_state.meal_log = []

# Initialize food database
food_database = {
    "Chicken Breast": {"Calories": 165, "Protein": 31, "Carbs": 0, "Fats": 3.6},
    "Brown Rice": {"Calories": 215, "Protein": 5, "Carbs": 45, "Fats": 1.8},
    "Broccoli": {"Calories": 55, "Protein": 4.2, "Carbs": 11.2, "Fats": 0.6},
    "Salmon": {"Calories": 206, "Protein": 22, "Carbs": 0, "Fats": 13},
    "Avocado": {"Calories": 234, "Protein": 3, "Carbs": 12, "Fats": 21}
}

# Initialize daily goals
if "daily_goals" not in st.session_state:
    st.session_state.daily_goals = {"Calories": 2000, "Protein": 150, "Carbs": 250, "Fats": 70}

# Sidebar for daily goal settings
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

# Main interface
st.title("Macro & Calorie Tracker")

# Meal logging section
st.header("Log a Meal")

food_choice = st.selectbox("Select a food item:", list(food_database.keys()))
quantity = st.number_input("Enter quantity (multiplier)", min_value=0.1, step=0.1, value=1.0)

if st.button("Log Meal"):
    food_info = food_database[food_choice]
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
