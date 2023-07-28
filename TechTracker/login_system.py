# login_system.py

import streamlit as st

# Create a dictionary to store user credentials (username as key, password as value)
users = {}

def app():
    st.title("Login")

    # Create a dictionary to store user roles (username as key, role as value)
    user_roles = {}

    # Check if the user is logged in or not
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Initialize the username_input variable with an empty string
    username_input = ""

    # Check if the user has submitted the login form
    if not st.session_state['logged_in']:
        st.subheader("New User? Sign Up!")
        new_username = st.text_input("Enter a new username:")
        new_password = st.text_input("Enter a new password:", type="password")

        if st.button("Sign Up"):
            if new_username and new_password:
                users[new_username] = new_password
                st.success("Account created successfully!")

        st.subheader("Login")
        username_input = st.text_input("Username:")
        password_input = st.text_input("Password:", type="password")

        if st.button("Login"):
            if username_input in users and users[username_input] == password_input:
                st.session_state['logged_in'] = True
                st.success("Login successful!")
                if username_input == 'admin':  # You can set different roles here based on your requirements
                    user_roles[username_input] = 'admin'
                else:
                    user_roles[username_input] = 'user'
                #New Change: 
                return True, username_input  # Return the flag and the username
            else:
                st.error("Invalid username or password. Please try again.")
                #New Change: 
                return False, ""  # Return the flag and an empty string

    # Redirect users to different pages based on their roles
    if st.session_state['logged_in']:
        #username = st.text_input("Enter your username:")
        username = username_input
        if username in user_roles:
            role = user_roles[username]
            if role == 'admin':
                st.title("Welcome, Admin!")
                st.write("You have administrative privileges.")
                st.write("Add your web scraping content here!")  # Content for the admin user
            else:
                st.title("Welcome!")
                st.write("You are now logged in.")
                st.write("Add your web scraping content here!")  # Content for regular users
