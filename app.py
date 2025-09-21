import streamlit as st
from index import execute_command  # assuming index.py has a function execute_command(cmd)

# Set page configuration
st.set_page_config(page_title="Python Terminal", page_icon="💻", layout="centered")

st.title("Python-Based Command Terminal")
st.write("Type your commands below and see the output:")

# Text input for command
command = st.text_input("Enter Command:", "")

# Button to execute command
if st.button("Run"):
    if command.strip() != "":
        try:
            output = execute_command(command)  # calling the function from index.py
            st.code(output)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a command!")

# Optional: show command history
if 'history' not in st.session_state:
    st.session_state['history'] = []

if command and command.strip() != "":
    st.session_state['history'].append(command)

if st.session_state['history']:
    st.subheader("Command History")
    for i, cmd in enumerate(st.session_state['history']):
        st.write(f"{i+1}. {cmd}")
