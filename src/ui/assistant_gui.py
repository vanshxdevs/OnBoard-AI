"""
Main Assistant GUI for interacting with employees.
"""
import streamlit as st
from src.utils.logger import logger
from src.ui.theme import DARK_GLASS_THEME


class AssistantGUI:
    """GUI for the AI Assistant chat interface."""
    
    def __init__(self, assistant):
        """Initialize the GUI with an assistant instance.
        
        Args:
            assistant: The Assistant instance to use for responses
        """
        self.assistant = assistant
        self.messages = assistant.messages
        self.employee_information = assistant.employee_information

    def get_response(self, user_input: str):
        """Get response from the assistant.
        
        Args:
            user_input: User's message
            
        Returns:
            Response generator
        """
        return self.assistant.get_response(user_input)

    def render_messages(self):
        """Render all chat messages."""
        for message in self.messages:
            if message["role"] == "user":
                st.chat_message("human").markdown(message["content"])
            elif message["role"] == "ai":
                st.chat_message("ai").markdown(message["content"])

    def set_state(self, key: str, value):
        """Update session state.
        
        Args:
            key: Session state key
            value: Value to store
        """
        st.session_state[key] = value

    def render_user_input(self):
        """Render the chat input and handle user messages."""
        user_input = st.chat_input("Type here...", key="input")
        
        if user_input and user_input.strip():
            # Display user message
            st.chat_message("human").markdown(user_input)

            # Get AI response
            response_generator = self.get_response(user_input)

            with st.chat_message("ai"):
                response = st.write_stream(response_generator)

            # Update message history
            self.messages.append({"role": "user", "content": user_input})
            self.messages.append({"role": "ai", "content": response})
            self.set_state("messages", self.messages)

    def render_sidebar(self):
        """Render the sidebar with logo and employee information."""
        with st.sidebar:
            st.logo(
                "https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg"
            )
            st.title("🤖 OnBoard AI")
            st.subheader("Employee Onboarding Assistant")
            
            st.markdown("---")
            
            st.subheader("📋 Employee Information")
            
            # Display employee info in a structured format
            emp = self.employee_information
            st.markdown(f"**Name:** {emp.get('name', '')} {emp.get('lastname', '')}")
            st.markdown(f"**ID:** `{emp.get('employee_id', 'N/A')[:8]}...`")
            st.markdown(f"**Position:** {emp.get('position', 'N/A')}")
            st.markdown(f"**Department:** {emp.get('department', 'N/A')}")
            st.markdown(f"**Location:** {emp.get('location', 'N/A')}")
            
            with st.expander("📧 Contact Details"):
                st.markdown(f"**Email:** {emp.get('email', 'N/A')}")
                st.markdown(f"**Phone:** {emp.get('phone_number', 'N/A')}")
            
            with st.expander("👤 Additional Info"):
                st.markdown(f"**Supervisor:** {emp.get('supervisor', 'N/A')}")
                st.markdown(f"**Hire Date:** {emp.get('hire_date', 'N/A')}")
                if emp.get('skills'):
                    st.markdown(f"**Skills:** {', '.join(emp.get('skills', []))}")
            
            st.markdown("---")
            st.caption("🔒 Confidential Information")
            st.caption("⚠️ Clearance Level: Restricted")

    def render(self):
        """Render the complete GUI."""
        logger.info("Rendering AssistantGUI")
        
        # Apply dark glossy glass theme
        st.markdown(DARK_GLASS_THEME, unsafe_allow_html=True)
        
        # Render sidebar
        self.render_sidebar()
        
        # Main chat area
        st.title("💬 Onboarding Chat")
        st.caption("Ask questions about company policies, procedures, and your role")
        
        # Render chat history
        self.render_messages()
        
        # Render input
        self.render_user_input()
        
        logger.debug("GUI render complete")
