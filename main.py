import streamlit as st
from crew import MentalHealthSupportCrew

# Initialize Crew
crew = MentalHealthSupportCrew()

# Set up Streamlit
st.set_page_config(
    page_title="MindMate: AI Mental Health Chat",
    page_icon="🧠",
    layout="wide"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def main():
    st.title("🧠 MindMate: AI Mental Health Chatbot")
    st.markdown("Your mental health companion, here to help.")

    # Display chat history
    for chat in st.session_state.chat_history:
        st.chat_message("user").write(chat["user"])
        st.chat_message("assistant").write(chat["assistant"])

    # User Input
    user_input = st.chat_input("How are you feeling today?")
    if user_input:
        # Run Crew
        result = crew.kickoff({"user_input": user_input})

        # Add to chat history
        st.session_state.chat_history.append({
            "user": user_input,
            "assistant": result["response"]
        })

        # Show tasks executed
        st.sidebar.header("Tasks Executed")
        for task in result["tasks_executed"]:
            st.sidebar.write(f"- {task}")

        # Refresh UI
        # st.experimental_rerun()


if __name__ == "__main__":
    main()
