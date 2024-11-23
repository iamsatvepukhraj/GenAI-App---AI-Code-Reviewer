import streamlit as st
import openai

# Configure OpenAI API Key
openai.api_key = "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"

# Page Setup
st.set_page_config(
    page_title="GenAI Code Reviewer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("GenAI Code Reviewer")
st.sidebar.markdown("Upload your code or paste it below for AI-powered review.")

# Code Input Section
st.header("Upload or Paste Your Code")
code = st.text_area("Paste your code here:", height=300, placeholder="Enter Python Code.")

uploaded_file = st.file_uploader("Or upload a code file:", type=["py"])

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded Code Preview:", code, height=300)

# AI Feedback Button
if st.button("Get AI Review"):
    if code.strip():
        with st.spinner("Analyzing your code..."):
            # AI Review using OpenAI API
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Review this code and suggest improvements:\n\n{code}",
                    max_tokens=500,
                    temperature=0.5,
                )
                feedback = response['choices'][0]['text']
                st.success("Code review completed!")
                st.subheader("AI Feedback:")
                st.write(feedback)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please paste code or upload a file.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built with using Streamlit and OpenAI.")

import google.generativeai as genai
import streamlit as st

# Setting up the API key
with open("requirements.txt") as f:
    key = f.read().strip()  # Remove any surrounding whitespace or newline characters

genai.configure(api_key=key)

# Streamlit setup
st.title("👨‍💻Your Code Review 🈂")
st.subheader('Issues with your python code? Review your codebase now!')

# Taking user input (Python code)
user_prompt = st.text_area("Enter your Python code...")

# If the button is clicked, generate responses
if st.button("Review"):
    if user_prompt:
        try:
            # Configure the model (ensure model name matches the available models in the Gemini API)
            model = genai.GenerativeModel(model_name='models/gemini-1.5-pro-latest',
                                          system_instruction="""You are a friendly AI assistant.
                                                                Given a Python code to review, analyze the submitted code and identify bugs, errors or areas of improvement.
                                                                Provide the fixed code snippets.
                                                                Explain the reasoning behind code corrections or suggestions. 
                                                                If the code is not in Python, politely remind the user that you are a Python code review assistant.
                                                                """)

            # Generate the response
            response = model.generate(user_prompt)

            # Display the response (Make sure the response has text field)
            if response and hasattr(response, 'text'):
                st.write(response.text)
            else:
                st.write("Sorry, I couldn't process your request. Please check your code or try again later.")
        except Exception as e:
            st.write(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter some Python code for review.")
