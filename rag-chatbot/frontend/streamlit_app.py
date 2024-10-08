import requests
import streamlit as st

# Define the base URL for API
API_BASE_URL = "https://localhost:8000"

# Helper function to make authenticated API requests


def authenticated_request(method, endpoint, token, data=None, params=None, files=None):
    headers = {"Authorization": f"Bearer {token}"}
    if method == "GET":
        response = requests.get(API_BASE_URL + endpoint,
                                headers=headers, params=params)
    elif method == "POST":
        response = requests.post(
            API_BASE_URL + endpoint, headers=headers, json=data)
    elif method == "DELETE":
        response = requests.delete(API_BASE_URL + endpoint, headers=headers)
    return response


# Initialize session state variables for login state and token
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'token' not in st.session_state:
    st.session_state.token = None

# Function for login view


def login_view():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_BASE_URL}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state.logged_in = True
            st.session_state.token = response.json()['access_token']
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your credentials.")

    st.write("Don't have an account?")
    if st.button("Register"):
        registration_view()

# Function for registration view


def registration_view():
    st.title("Register")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        })
        if response.status_code == 201:
            st.success("Registration successful! Please log in.")
        else:
            st.error("Registration failed. Please try again.")

# Function for chat view


def chat_view():
    st.title("Your Chats")

    # Retrieve chat list
    response = authenticated_request("GET", "/chats", st.session_state.token)
    if response.status_code == 200:
        chats = response.json()
        for chat in chats:
            if st.button(f"Chat {chat['id']}"):
                view_chat(chat['id'])
    else:
        st.error("Failed to retrieve chats.")

    # Button to create new chat
    if st.button("Create New Chat"):
        new_chat()

# Function to view a specific chat


def view_chat(chat_id):
    st.title(f"Chat {chat_id}")
    response = authenticated_request(
        "GET", f"/chats/{chat_id}", st.session_state.token)
    if response.status_code == 200:
        chat = response.json()
        st.write(chat['messages'])

        new_message = st.text_input("Type a new message")
        if st.button("Send"):
            post_message(chat_id, new_message)
    else:
        st.error("Failed to retrieve chat.")

# Function to post a message in an existing chat


def post_message(chat_id, message):
    response = authenticated_request(
        "POST", f"/chats/{chat_id}", st.session_state.token, data={"content": message})
    if response.status_code == 200:
        st.success("Message sent.")
    else:
        st.error("Failed to send message.")

# Function to create a new chat


def new_chat():
    st.title("Create New Chat")
    first_message = st.text_input("Enter your message")
    if st.button("Start Chat"):
        response = authenticated_request(
            "POST", "/chats", st.session_state.token, data={"content": first_message})
        if response.status_code == 200:
            st.success("Chat created.")
        else:
            st.error("Failed to create chat.")

# Function for document management view


def document_view():
    st.title("Your Documents")

    # Retrieve document list
    response = authenticated_request("GET", "/docs", st.session_state.token)
    if response.status_code == 200:
        docs = response.json()
        for doc in docs:
            st.write(f"Document {doc['id']}")
            if st.button(f"Delete {doc['id']}"):
                delete_document(doc['id'])
    else:
        st.error("Failed to retrieve documents.")

    # Upload document
    st.title("Upload Document")
    uploaded_file = st.file_uploader("Choose a file")
    if st.button("Upload"):
        if uploaded_file is not None:
            files = {"file": uploaded_file.getvalue()}
            response = authenticated_request(
                "POST", "/docs", st.session_state.token, files=files)
            if response.status_code == 200:
                st.success("Document uploaded.")
            else:
                st.error("Failed to upload document.")

# Function to delete a document


def delete_document(doc_id):
    response = authenticated_request(
        "DELETE", f"/docs/{doc_id}", st.session_state.token)
    if response.status_code == 200:
        st.success("Document deleted.")
    else:
        st.error("Failed to delete document.")

# Main app logic


def main():
    if not st.session_state.logged_in:
        login_view()
    else:
        st.sidebar.title("Navigation")
        option = st.sidebar.selectbox(
            "Choose a view", ["Welcome", "Chats", "Documents"])

        if option == "Welcome":
            st.title("Welcome!")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.token = None
                st.success("Logged out successfully.")
        elif option == "Chats":
            chat_view()
        elif option == "Documents":
            document_view()


if __name__ == "__main__":
    main()
