import streamlit as st
import pandas as pd

# Function to load questions from the CSV file
@st.cache_data
def load_questions(csv_file):
    return pd.read_csv(csv_file)

# Function to calculate the score
def calculate_score(user_answers, correct_answers):
    score = 0
    for user_answer, correct_answer in zip(user_answers, correct_answers):
        if user_answer == correct_answer:
            score += 1
    return score

# Streamlit app
def mcq_quiz_app():
    # Load questions
    csv_file = "questions.csv"  # Specify your CSV file path
    questions_df = load_questions(csv_file)

    st.title("Welcome to the MCQ Quiz App!")
    st.subheader("Test your knowledge and see how much you score!")

    # Input for user's name
    user_name = st.text_input("Enter your name:", "")

    if user_name:
        st.write(f"Hello, **{user_name}!** Let's begin the quiz.")

        # Initialize session state to store user answers
        if "user_answers" not in st.session_state:
            st.session_state.user_answers = [""] * len(questions_df)

        # Display questions and collect answers
        for index, row in questions_df.iterrows():
            st.write(f"**Q{index + 1}. {row['question']}**")
            options = [row[f"choice{i}"] for i in range(1, 5)]
            # Use session state to store the selected answer
            st.session_state.user_answers[index] = st.radio(
                f"Select your answer for Q{index + 1}:",
                options,
                key=f"q{index}",
                index=options.index(st.session_state.user_answers[index])
                if st.session_state.user_answers[index] in options
                else 0,
            )

        # Submit button
        if st.button("Submit"):
            correct_answers = questions_df["correct_answer"].tolist()
            user_answers = st.session_state.user_answers
            score = calculate_score(user_answers, correct_answers)
            total_questions = len(questions_df)

            st.success(f"**{user_name}, you scored {score}/{total_questions}!**")
            st.subheader("Correct Answers Review:")
            review_df = questions_df[["question", "correct_answer"]]
            st.dataframe(review_df)

if __name__ == "__main__":
    mcq_quiz_app()
