import streamlit as st
import pandas as pd


# Load questions from CSV
def load_questions(file):
    return pd.read_csv(file, encoding='utf-8')

# CSS for Styling
def add_custom_styles():
    st.markdown(
        """ 
        <style>
        .question-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            min-height: 100px;
            font-family: Arial, sans-serif;
        }

        .button-container {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }

        button {
            background-color: #007BFF;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def add_marathi_font_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');

        .marathi-text {
            font-family: 'Noto Sans Devanagari', sans-serif;
            font-size: 20px;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Welcome Page
def welcome_page():
    st.image('assets\\front-banner.png')
    st.title("Welcome to the MCQ Test")
    name = st.text_input("Enter your name:")
    language = st.selectbox("Choose the test language:", ("English", "Marathi"))

    if st.button("Start Test"):
        if name.strip():
            st.session_state["name"] = name
            st.session_state["language"] = language

            # Load the questions based on the language selected
            if language == "English":
                st.session_state["questions"] = load_questions("english.csv")
            elif language == "Marathi":
                st.session_state["questions"] = load_questions("marathi.csv")

            if not st.session_state["questions"].empty:
                st.session_state["selected_questions"] = st.session_state["questions"].sample(25).reset_index(drop=True)
                st.session_state["current_question"] = 0
                st.session_state["user_answers"] = [None] * len(st.session_state["selected_questions"])
                st.session_state["page"] = "quiz"
            else:
                st.error("Failed to load questions. Please check the CSV file.")
        else:
            st.warning("Please enter your name!")

# Quiz Page
def quiz_page():
    st.title(f"Good Luck, {st.session_state['name']}!")
    st.markdown(f"**Language:** {st.session_state['language']}")

    # Get the current question index
    current_question = st.session_state["current_question"]
    questions = st.session_state["selected_questions"]

    # Display the current question with Marathi font styling
    st.markdown(
        f'<div class="marathi-text">Q{current_question + 1}: {questions.iloc[current_question]["Question"]}</div>',
        unsafe_allow_html=True
    )

    options = {
        "A": questions.iloc[current_question]["Option A"],
        "B": questions.iloc[current_question]["Option B"],
        "C": questions.iloc[current_question]["Option C"],
        "D": questions.iloc[current_question]["Option D"]
    }

    # Radio buttons for options
    selected_option = st.radio(
        "Choose an answer:",
        [f"{key}: {value}" for key, value in options.items()],
        index=0 if st.session_state["user_answers"][current_question] is None else ["A", "B", "C", "D"].index(
            st.session_state["user_answers"][current_question]
        ),
        key=f"q{current_question}"
    )

    # Save the selected answer
    st.session_state["user_answers"][current_question] = selected_option.split(":")[0]

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous") and current_question > 0:
            st.session_state["current_question"] -= 1
    with col2:
        if st.button("Next") and current_question < len(questions) - 1:
            st.session_state["current_question"] += 1

    # Submit button on the last question
    if current_question == len(questions) - 1:
        if st.button("Submit Exam"):
            st.session_state["page"] = "result"

# Result Page
def result_page():
    st.title("Your Results")
    correct = 0
    questions = st.session_state["selected_questions"]

    for i, row in questions.iterrows():
        # correct_answer = row["Answer"].strip()
        correct_answer = row["Answer"]
        user_answer = st.session_state["user_answers"][i]
        if user_answer == correct_answer:
            correct += 1

    score = correct * 2
    st.write(f"**Name:** {st.session_state['name']}")
    st.write(f"**Language:** {st.session_state['language']}")
    st.write(f"**Score:** {score}/50")

    if score >= 25:
        st.success("🎉 Congratulations! You Passed!")
    else:
        st.error("❌ Better luck next time!")
        
    st.image('assets\\end-banner.png')

# Main Function
def main():
    add_marathi_font_styles()
    add_custom_styles()  # Other styles for buttons and layout

    if "page" not in st.session_state:
        st.session_state["page"] = "welcome"

    if st.session_state["page"] == "welcome":
        welcome_page()
    elif st.session_state["page"] == "quiz":
        quiz_page()
    elif st.session_state["page"] == "result":
        result_page()


if __name__ == "__main__":
    main()
