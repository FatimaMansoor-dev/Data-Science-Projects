import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

api = 'AIzaSyBUFwHsf_r3u1tLVuBk2z6vxiCG4XkMJcM'
st.sidebar.title("Quiz Generator")




genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-pro')



def generate_questions_and_answers(text):
    # Define the prompt for generating questions and answers
    prompt = f"""Generate questions and answers:
Text: {text}
Questions:
Answers:
"""

    # Generate questions and answers using the Gemini API
    response = genai.generate_text(prompt=prompt)
    questions_and_answers = response.result.strip().split("\n")
    
    # Separate questions and answers
    questions = []
    answers = []
    for i, line in enumerate(questions_and_answers):
        if i % 2 == 0:
            questions.append(line)
        else:
            answers.append(line)
    
    return questions, answers

def main():
    # Import file option 
    uploaded_file = st.sidebar.file_uploader("Upload your PDF")
    if uploaded_file is not None:
        # Read the PDF file
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Generate questions and answers from the extracted text
        quiz_questions, quiz_answers = generate_questions_and_answers(text)
        
        # Ensure questions and answers are aligned
        max_length = max(len(quiz_questions), len(quiz_answers))
        quiz_questions += [''] * (max_length - len(quiz_questions))
        quiz_answers += [''] * (max_length - len(quiz_answers))
        
        # Display the generated quiz questions and answers
        for i, (question, answer) in enumerate(zip(quiz_questions, quiz_answers), start=1):
            st.write(f" {question}")
            st.write(f" {answer}")

if __name__ == "__main__":
    main()