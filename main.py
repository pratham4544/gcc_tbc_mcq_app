import streamlit as st
import pandas as pd
import random
import time

# Load questions from CSV
def load_questions(file="mcq.csv"):
    data = pd.read_csv(file)
    return data

# Welcome Page
def welcome_page():
    st.title("Welcome to the MCQ Test")
    name = st.text_input("Enter your name:")
    if st.button("Start Test"):
        if name.strip():
            st.session_state['name'] = name
            st.session_state['page'] = "quiz"
        else:
            st.warning("Please enter your name!")
# Quiz Page
def quiz_page():
    st.title(f"Good Luck, {st.session_state['name']}!")
    st.markdown("**Timer:** 25 minutes")
    timer = st.empty()
    start_time = st.session_state.get("start_time", time.time())
    st.session_state["start_time"] = start_time

    # Ensure questions are fixed for the session
    if "selected_questions" not in st.session_state:
        st.session_state["selected_questions"] = st.session_state["questions"].sample(25).reset_index(drop=True)

    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = {}

    questions = st.session_state["selected_questions"]

    for i, row in questions.iterrows():
        st.write(f"**Q{i+1}: {row['Question']}**")
        options = {
            "A": row['Option A'],
            "B": row['Option B'],
            "C": row['Option C'],
            "D": row['Option D']
        }

        # Display the full text options but store only the key (A, B, C, D)
        selected_option_text = st.radio(
            f"Choose an answer for Q{i+1}:",
            [f"{key}: {value}" for key, value in options.items()],
            key=f"q{i+1}"
        )

        # Extract the selected letter (A, B, C, D)
        selected_option = selected_option_text.split(":")[0]
        st.session_state["user_answers"][i] = selected_option

    if st.button("Submit"):
        st.session_state['page'] = "result"
    


# Result Page
def result_page():
    st.title("Your Result")
    correct = 0
    questions = st.session_state["selected_questions"]

    for i, row in questions.iterrows():
        correct_answer = row['Answer'].strip().upper()  # Correct answer from CSV (A, B, C, D)
        user_answer = st.session_state["user_answers"].get(i, "").strip().upper()  # User's choice (A, B, C, D)

        if user_answer == correct_answer:
            correct += 1
        else:
            st.write(f"Q{i+1}: Incorrect (Your Answer: {user_answer}, Correct Answer: {correct_answer})")

    # Calculate the score
    score = correct * 2
    st.write(f"**Name:** {st.session_state['name']}")
    st.write(f"**Score:** {score}/50")

    # Passing condition
    if score >= 25:
        st.success("🎉 Congratulations! You Passed!")
    else:
        st.error("❌ Better luck next time.")


# Main Function
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = "welcome"
    if 'questions' not in st.session_state:
        st.session_state['questions'] = load_questions()

    if st.session_state['page'] == "welcome":
        welcome_page()
    elif st.session_state['page'] == "quiz":
        quiz_page()
    elif st.session_state['page'] == "result":
        result_page()

if __name__ == "__main__":
    main()
