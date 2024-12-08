import streamlit as st
import time
import json
from crew import mental_health_support_crew

# Custom styling and setup
st.set_page_config(
    page_title="MindMate: AI Mental Health Support",
    page_icon="🧠",
    layout="wide"
)

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'agent_interactions' not in st.session_state:
    st.session_state.agent_interactions = []


# Styling for agent interaction visualization
def display_agent_interaction(interaction):
    """
    Create a detailed visualization of agent interactions and decision-making.
    """
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"**🤖 Interaction: {interaction['agent']}**")
        st.json(interaction['details'], expanded=False)

    with col2:
        status_color = "green" if interaction.get('status', 'processing') == "completed" else "orange"
        st.markdown(f"**Status:** <span style='color:{status_color}'>{interaction.get('status', 'Processing')}</span>",
                    unsafe_allow_html=True)


def process_user_input(user_input):
    """
    Process user input through the mental health support crew
    and track agent interactions.
    """
    # Reset agent interactions for new input
    st.session_state.agent_interactions = []

    # Track and visualize each agent's processing
    def track_agent_process(agent_name, description):
        interaction = {
            'agent': agent_name,
            'details': {'description': description},
            'status': 'processing'
        }
        st.session_state.agent_interactions.append(interaction)
        return interaction

    # User Interaction Agent
    user_interaction = track_agent_process(
        "User Interaction Agent",
        "Receiving and analyzing initial user input"
    )

    # Prepare inputs
    inputs = {'user_input': user_input}

    try:
        # Run the crew
        with st.spinner('Analyzing your input...'):
            result = mental_health_support_crew.kickoff(inputs=inputs)

        # Update agent statuses
        user_interaction['status'] = 'completed'
        user_interaction['details']['output'] = "Initial input processed successfully"

        # Add to chat history
        st.session_state.chat_history.append({
            'user': user_input,
            'assistant': result
        })

        return result

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "I'm sorry, but there was an error processing your request. Could you please try again?"


# Main Streamlit App Layout
def main():
    st.title("🧠 MindMate: AI Mental Health Support System")

    # Sidebar for additional information
    st.sidebar.header("How It Works")
    st.sidebar.info(
        "This system uses multiple AI agents to provide compassionate and "
        "comprehensive mental health support. Each interaction goes through "
        "careful analysis and personalized recommendations."
    )

    # Agent Overview
    with st.sidebar.expander("Agent Roles"):
        st.markdown("""
        - 🤝 **User Interaction Agent**: First point of contact
        - 🔍 **Assessment Agent**: Analyze emotional state
        - 📚 **Resource Recommendation Agent**: Provide personalized resources
        - 📊 **Monitoring Agent**: Track progress over time
        - 🚨 **Crisis Management Agent**: Handle high-risk situations
        """)

    # Chat History Display
    st.subheader("Conversation")
    for chat in st.session_state.chat_history:
        st.chat_message("user").write(chat['user'])
        st.chat_message("assistant").write(chat['assistant'])

    # Agent Interactions Visualization
    if st.session_state.agent_interactions:
        st.subheader("Agent Interaction Details")
        for interaction in st.session_state.agent_interactions:
            display_agent_interaction(interaction)

    # User Input
    user_input = st.chat_input("Share your thoughts or concerns...")

    if user_input:
        # Process user input
        assistant_response = process_user_input(user_input)

        # Rerun to update the UI
        st.rerun()


if __name__ == "__main__":
    main()