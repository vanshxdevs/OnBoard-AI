"""
Premium Dark Glossy Glass Theme for OnBoard AI
Provides a sleek black glassmorphism design with royal blue accents
"""


DARK_GLASS_THEME = """
<style>
/* Import Premium Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ==================== ROOT VARIABLES ==================== */
:root {
    --primary-blue: #2563eb;
    --blue-glow: rgba(37, 99, 235, 0.4);
    --glass-black: rgba(0, 0, 0, 0.7);
    --glass-border: rgba(255, 255, 255, 0.1);
    --text-white: #ffffff;
    --text-gray: #9ca3af;
    --background-dark: #000000;
}

/* ==================== GLOBAL RESET ==================== */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ==================== MAIN BACKGROUND ==================== */
.stApp {
    background: linear-gradient(135deg, #000000 0%, #0a0a0a 50%, #000000 100%);
    background-attachment: fixed;
}

/* Add subtle grid pattern */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

/* ==================== GLOSSY GLASS CONTAINERS ==================== */
.block-container {
    background: rgba(0, 0, 0, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
}

/* ==================== SIDEBAR ==================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(0, 0, 0, 0.95) 0%, rgba(10, 10, 10, 0.95) 100%) !important;
    backdrop-filter: blur(30px) !important;
    -webkit-backdrop-filter: blur(30px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5) !important;
}

[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* Sidebar Logo Glow */
[data-testid="stSidebar"] img {
    filter: drop-shadow(0 0 20px var(--blue-glow)) brightness(1.1);
    transition: all 0.3s ease;
}

[data-testid="stSidebar"] img:hover {
    filter: drop-shadow(0 0 30px var(--blue-glow)) brightness(1.2);
}

/* ==================== HEADERS ==================== */
h1, h2, h3 {
    color: var(--text-white) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
}

h1 {
    background: linear-gradient(135deg, #ffffff 0%, var(--primary-blue) 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: 0 0 40px var(--blue-glow);
}

h2, h3 {
    color: var(--primary-blue) !important;
    text-shadow: 0 0 20px var(--blue-glow);
}

/* ==================== CHAT MESSAGES ==================== */
.stChatMessage {
    background: rgba(0, 0, 0, 0.8) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin: 0.75rem 0 !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6) !important;
    transition: all 0.3s ease !important;
}

.stChatMessage:hover {
    border-color: rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7) !important;
}

/* User Messages - Royal Blue */
.stChatMessage[data-testid*="user"] {
    background: rgba(37, 99, 235, 0.08) !important;
    border-left: 3px solid var(--primary-blue) !important;
    box-shadow: 0 0 30px var(--blue-glow), 0 8px 24px rgba(0, 0, 0, 0.6) !important;
}

/* AI Messages */
.stChatMessage[data-testid*="assistant"] {
    border-left: 3px solid rgba(255, 255, 255, 0.15) !important;
}

/* ==================== INPUT FIELDS ==================== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: var(--text-white) !important;
    padding: 0.875rem !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.4) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 30px var(--blue-glow), inset 0 2px 8px rgba(0, 0, 0, 0.4) !important;
    background: rgba(10, 10, 20, 0.8) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-gray) !important;
}

/* Password Input */
input[type="password"] {
    letter-spacing: 0.2em !important;
}

/* ==================== BUTTONS ==================== */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-blue) 0%, #1e40af 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.875rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px var(--blue-glow), 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 30px var(--blue-glow), 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    background: linear-gradient(135deg, #3b82f6 0%, var(--primary-blue) 100%) !important;
}

.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* Form Submit Button */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, var(--primary-blue) 0%, #1e40af 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 25px var(--blue-glow) !important;
    width: 100% !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.stFormSubmitButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 40px var(--blue-glow) !important;
}

/* ==================== ALERTS & INFO BOXES ==================== */
.stAlert {
    background: rgba(0, 0, 0, 0.8) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: var(--text-white) !important;
    padding: 1rem !important;
}

[data-baseweb="notification"] {
    background: rgba(0, 0, 0, 0.9) !important;
    backdrop-filter: blur(15px) !important;
    border-left: 3px solid var(--primary-blue) !important;
    box-shadow: 0 0 20px var(--blue-glow) !important;
}

/* ==================== EXPANDERS ==================== */
.streamlit-expanderHeader {
    background: rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: var(--text-white) !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 20px var(--blue-glow) !important;
}

/* ==================== CHAT INPUT ==================== */
.stChatInputContainer {
    background: rgba(0, 0, 0, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 16px !important;
    padding: 0.75rem !important;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.5) !important;
}

.stChatInputContainer:focus-within {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 30px var(--blue-glow), 0 -4px 20px rgba(0, 0, 0, 0.6) !important;
}

/* ==================== SCROLLBAR ==================== */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--primary-blue) 0%, #1e40af 100%);
    border-radius: 10px;
    border: 2px solid rgba(0, 0, 0, 0.8);
    transition: all 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #3b82f6 0%, var(--primary-blue) 100%);
    box-shadow: 0 0 10px var(--blue-glow);
}

/* ==================== TEXT & LINKS ==================== */
.stMarkdown {
    color: var(--text-gray) !important;
}

p, span, div {
    color: var(--text-gray) !important;
}

a {
    color: var(--primary-blue) !important;
    text-decoration: none !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
}

a:hover {
    color: #3b82f6 !important;
    text-shadow: 0 0 15px var(--blue-glow) !important;
}

/* ==================== DIVIDER ==================== */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--primary-blue), transparent) !important;
    margin: 2rem 0 !important;
    box-shadow: 0 0 10px var(--blue-glow) !important;
}

/* ==================== CAPTIONS ==================== */
.caption, [data-testid="stCaptionContainer"] {
    color: var(--text-gray) !important;
    font-size: 0.85rem !important;
}

/* ==================== SELECT & RADIO ==================== */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(0, 0, 0, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: var(--text-white) !important;
}

.stRadio > div {
    background: rgba(0, 0, 0, 0.6) !important;
    padding: 1rem !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* ==================== METRIC CARDS ==================== */
[data-testid="stMetricValue"] {
    color: var(--primary-blue) !important;
    font-weight: 700 !important;
    text-shadow: 0 0 20px var(--blue-glow) !important;
}

/* ==================== SPINNER ==================== */
.stSpinner > div {
    border-color: var(--primary-blue) transparent transparent transparent !important;
}

/* ==================== TOP ACCENT LINE ==================== */
.stApp::after {
    content: '' !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, var(--primary-blue), transparent) !important;
    box-shadow: 0 0 20px var(--blue-glow) !important;
    z-index: 9999 !important;
}

/* ==================== ANIMATIONS ==================== */
@keyframes glow {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes pulse-blue {
    0%, 100% { box-shadow: 0 0 20px var(--blue-glow); }
    50% { box-shadow: 0 0 35px var(--blue-glow); }
}

/* ==================== FORM STYLING ==================== */
[data-testid="stForm"] {
    background: rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
}

/* ==================== LABELS ==================== */
label {
    color: var(--text-white) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* ==================== MARKDOWN CODE BLOCKS ==================== */
code {
    background: rgba(0, 0, 0, 0.8) !important;
    color: var(--primary-blue) !important;
    padding: 0.2rem 0.4rem !important;
    border-radius: 4px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

pre {
    background: rgba(0, 0, 0, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
}
</style>
"""
