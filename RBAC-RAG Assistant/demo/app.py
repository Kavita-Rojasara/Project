import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RBAC RAG Chatbot", layout="wide")

st.title("RBAC RAG Internal Chatbot")

# -----------------------
# SESSION STATE
# -----------------------
if "token" not in st.session_state:
    st.session_state.token = None

# -----------------------
# LOGIN UI
# -----------------------
st.sidebar.header("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    try:
        res = requests.post(
            f"{API_URL}/auth/login",
            params={"username": username, "password": password}
        )

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access_token"]
            st.sidebar.success("Logged in successfully")
        else:
            st.sidebar.error("Invalid credentials")

    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")

# -----------------------
# MAIN CHAT UI
# -----------------------
if st.session_state.token:

    st.header("Ask a Question")

    query = st.text_input("Enter your query")

    if st.button("Ask"):

        if not query.strip():
            st.warning("Please enter a query")
        else:
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                }

                res = requests.post(
                    f"{API_URL}/chat",
                    params={"query": query},
                    headers=headers
                )

                if res.status_code == 200:
                    data = res.json()

                    # ANSWER
                    st.subheader("🧠 Answer")
                    st.write(data.get("answer", "No answer"))

                    # SOURCES 
                    st.subheader("📄 Sources")

                    sources = data.get("sources", [])

                    if sources:
                        for src in sources:
                            st.write(f"- {src}")   
                    else:
                        st.write("No sources found")

                else:
                    st.error("Failed to get response")

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.info("Please login to continue")