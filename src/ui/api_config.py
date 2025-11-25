"""
API Key Configuration UI.
Provides a centered form for users to enter their API keys before using the application.
"""
import streamlit as st
from src.config import get_settings
from src.utils.logger import logger
from src.ui.theme import DARK_GLASS_THEME


def render_api_config() -> bool:
    """Render the API key configuration screen.
    
    Returns:
        True if configuration is complete and valid, False otherwise
    """
    settings = get_settings()
    
    # ONLY check session state - ignore .env file completely
    if "api_configured" in st.session_state and st.session_state.api_configured:
        return True
    
    # Apply dark glossy glass theme
    st.markdown(DARK_GLASS_THEME, unsafe_allow_html=True)
    
    # Center the configuration form
    st.markdown("""
        <style>
        .main > div {
            padding-top: 3rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg",
            width=200
        )
        
        st.title("🔑 API Configuration")
        st.markdown("### OnBoard AI - Employee Onboarding System")
        st.markdown("---")
        
        st.info(
            "**Required API Keys:**\n\n"
            "To access the onboarding system, you must provide valid API credentials.\n\n"
            "- **Groq API Key**: For AI language model access\n"
            "- **LangChain API Key**: For conversation tracking and analytics"
        )
        
        st.markdown("#### Enter Your API Keys")
        
        # Show error message if exists
        if "config_error" in st.session_state:
            st.error(st.session_state.config_error)
        
        # Create form for API keys
        with st.form("api_config_form", clear_on_submit=False):
            groq_key = st.text_input(
                "Groq API Key *",
                type="password",
                placeholder="gsk_...",
                help="Get your API key from https://console.groq.com",
                key="groq_input"
            )
            
            langchain_key = st.text_input(
                "LangChain API Key *",
                type="password",
                placeholder="ls__...",
                help="Get your API key from https://smith.langchain.com",
                key="langchain_input"
            )
            
            st.caption("* Both fields are required")
            
            submitted = st.form_submit_button(
                "🚀 Initialize System",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                # Clear previous errors
                if "config_error" in st.session_state:
                    del st.session_state.config_error
                
                # Validate inputs - both are required
                if not groq_key or not groq_key.strip():
                    st.session_state.config_error = "❌ Groq API Key is required. Please enter a valid key."
                    st.rerun()
                
                if not langchain_key or not langchain_key.strip():
                    st.session_state.config_error = "❌ LangChain API Key is required. Please enter a valid key."
                    st.rerun()
                
                # Both keys provided - save them
                try:
                    settings.set_api_keys(groq_key.strip(), langchain_key.strip())
                    st.session_state.api_configured = True
                    logger.info("API keys configured successfully")
                    
                    # Show success and proceed
                    st.success("✅ API keys configured successfully!")
                    st.balloons()
                    
                    # Small delay for user to see success message
                    import time
                    time.sleep(1)
                    
                    # Force rerun to proceed to main app
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Error configuring API keys: {e}")
                    st.session_state.config_error = f"❌ Configuration error: {str(e)}"
                    st.rerun()
        
        st.markdown("---")
        st.caption(
            "🔒 Your API keys are stored securely in environment variables "
            "and are not saved to disk."
        )
        st.caption(
            "⚠️ **Security Notice**: Ensure you are on a secure network. "
            "Unauthorized access will be logged and reported."
        )
    
    return False
