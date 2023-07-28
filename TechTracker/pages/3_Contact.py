import streamlit as st 

st.title("Contacts")

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>

    <style>
        form {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        input[type="text"],
        input[type="email"],
        textarea {
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }

        button[type="submit"] {
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            background-color: #4caf50;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
    </style>

    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()