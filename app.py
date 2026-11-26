import hmac
import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()


def get_secret(key: str) -> str:
    """Read a secret from Streamlit secrets first, falling back to environment variables."""
    try:
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return os.getenv(key, "").strip()


WEBHOOK_URL = get_secret("N8N_WEBHOOK_URL")
OWNER_ACCESS_CODE = get_secret("OWNER_ACCESS_CODE")

# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant | n8n Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Responsive Animated CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Background & Container Tweaks */
    .stMainBlockContainer,
    .main .block-container {
        max-width: 1040px;
        margin: 0 auto;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }

    /* Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulseGlow {
        0%, 100% {
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.45);
        }
        50% {
            box-shadow: 0 0 28px rgba(168, 85, 247, 0.7);
        }
    }

    @keyframes floatAnimation {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-4px); }
    }

    /* Hero Header Styling */
    .hero-container {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
        animation: fadeInUp 0.8s ease-out;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #A5B4FC;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
        animation: pulseGlow 2s infinite ease-in-out;
    }

    /* Feature Cards Grid (3x2 desktop, 2x3 tablet, 1x6 mobile) */
    .capabilities-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin: 1.2rem 0 1.8rem 0;
        animation: fadeInUp 1s ease-out;
    }

    .cap-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 14px 16px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        height: 100%;
        box-sizing: border-box;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(12px);
    }

    .cap-card:hover {
        transform: translateY(-3px) scale(1.02);
        border-color: rgba(168, 85, 247, 0.45);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
    }

    .cap-icon {
        font-size: 1.6rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 10px;
    }

    .cap-text h4 {
        margin: 0;
        font-size: 0.92rem;
        font-weight: 600;
        color: #F1F5F9;
    }

    .cap-text p {
        margin: 2px 0 0 0;
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.3;
    }

    /* Subheader styling */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: 700;
        color: #E2E8F0;
        margin: 1.5rem 0 0.8rem 0;
    }

    /* Responsive Chat Messages */
    .stChatMessage {
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease;
    }

    /* Quick suggestion buttons */
    .quick-title {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Tablet & Mobile Responsive Adjustments */
    @media (max-width: 1024px) {
        .capabilities-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 8px !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 calc(50% - 8px) !important;
            min-width: calc(50% - 8px) !important;
        }
    }

    @media (max-width: 640px) {
        .hero-container {
            padding: 0.75rem 0.25rem;
        }
        .hero-title {
            font-size: 1.85rem;
        }
        .stMainBlockContainer,
        .main .block-container {
            padding-left: 0.9rem;
            padding-right: 0.9rem;
            padding-top: 1rem;
        }
        .capabilities-grid {
            grid-template-columns: 1fr;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "is_owner" not in st.session_state:
    st.session_state.is_owner = False

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    st.markdown("#### 🔐 Access Mode")

    if st.session_state.is_owner:
        st.success("🔓 **Owner Mode Active** (Live n8n Agent)")
        if WEBHOOK_URL:
            st.caption("Webhook: `Configured via secrets/env` ✅")
        else:
            st.warning("⚠️ `N8N_WEBHOOK_URL` is not configured.")
        if st.button("🔒 Lock & Switch to Demo Mode", use_container_width=True):
            st.session_state.is_owner = False
            st.rerun()
    else:
        st.info("🛡️ **Public Demo Mode** (Safe Simulated Responses)")
        with st.form("owner_auth_form", clear_on_submit=True):
            entered_code = st.text_input(
                "Owner Access Code",
                type="password",
                placeholder="Enter passcode for live agent...",
                help="Protects personal Gmail, Calendar, Tasks, Docs, and Sheets from unauthorized public access."
            )
            unlock_clicked = st.form_submit_button("🔓 Unlock Live Agent", use_container_width=True)
            if unlock_clicked:
                if not OWNER_ACCESS_CODE:
                    st.error("Owner mode is disabled (`OWNER_ACCESS_CODE` is not set).")
                elif hmac.compare_digest(entered_code.strip(), OWNER_ACCESS_CODE):
                    st.session_state.is_owner = True
                    st.rerun()
                else:
                    st.error("Invalid access code. Staying in Public Demo Mode.")
    
    st.markdown("---")
    st.markdown("### 🛠️ Connected Tools & APIs")
    st.markdown("""
    - 🔍 **SerpApi** *(Live Google Search)*
    - 📅 **Google Calendar** *(Create & Manage Events)*
    - 📋 **Google Tasks** *(Smart To-Do Lists)*
    - ✉️ **Gmail** *(Inbox Reader & Email Sender)*
    - 📄 **Google Docs** *(Note-taking & Document Edits)*
    - 💰 **Expense Tracker** *(Google Sheets + Calculator)*
    - 🧠 **OpenAI LLM** + **Window Memory**
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    msg_count = len(st.session_state.get("messages", []))
    st.metric(label="Messages Exchanged", value=msg_count)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("🚀 **Live App**: [Streamlit Cloud](https://agenticai-28f4o89zzdnxz2nwwqqtd2.streamlit.app/)")

# Hero Header with Live Pulse Badge
mode_badge = "Live n8n Multi-Agent Online (Owner Mode)" if st.session_state.is_owner else "Public Demo Mode · Personal Tools Protected"
st.markdown(f"""
<div class="hero-container">
    <div class="hero-badge">
        <span class="pulse-dot"></span>
        <span>{mode_badge}</span>
    </div>
    <div class="hero-title">Personal AI Assistant</div>
    <p style="color: #94A3B8; font-size: 0.95rem; margin-top: 0;">
        Autonomous agent powered by OpenAI, n8n automations, and Google Workspace tools.
    </p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.is_owner:
    st.info(
        "🛡️ **Recruiter / Public Demo Mode:** Responses are simulated so visitors can safely explore the workflow "
        "without accessing private Gmail, Calendar, Tasks, Docs, or Expense data. "
        "The owner can unlock the live n8n agent from the sidebar."
    )

# Subheader: What can your personal assistant do?
st.markdown('<div class="section-title"><span>⚡</span> What can your personal assistant do?</div>', unsafe_allow_html=True)

# Dynamic Interactive Cards
st.markdown("""
<div class="capabilities-grid">
    <div class="cap-card">
        <div class="cap-icon">💡</div>
        <div class="cap-text">
            <h4>Answer Any Question</h4>
            <p>Researches deep queries with real-time web search via SerpApi.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">📅</div>
        <div class="cap-text">
            <h4>Calendar & Meetings</h4>
            <p>Schedules, checks, and manages Google Calendar events seamlessly.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">✉️</div>
        <div class="cap-text">
            <h4>Emails & Summaries</h4>
            <p>Reads Gmail inbox, summarizes threads, and drafts replies.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">📋</div>
        <div class="cap-text">
            <h4>Tasks & To-Do Lists</h4>
            <p>Organizes action items and checklists directly in Google Tasks.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">📝</div>
        <div class="cap-text">
            <h4>Quick Notes & Docs</h4>
            <p>Captures ideas and updates documents in Google Docs.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">💰</div>
        <div class="cap-text">
            <h4>Expense & Budgeting</h4>
            <p>Calculates and logs financial records directly into Google Sheets.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Section Header
st.markdown('<div class="section-title"><span>💬</span> Chat with your assistant</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Prompt Suggestions (Interactive buttons)
st.markdown('<div class="quick-title">✨ Try asking:</div>', unsafe_allow_html=True)
quick_cols = st.columns([1, 1, 1, 1])
clicked_prompt = None

with quick_cols[0]:
    if st.button("📅 My schedule today", use_container_width=True):
        clicked_prompt = "What events and meetings do I have on my calendar for today?"
with quick_cols[1]:
    if st.button("✉️ Check unread emails", use_container_width=True):
        clicked_prompt = "Can you check my latest unread emails in Gmail and summarize them?"
with quick_cols[2]:
    if st.button("💰 Log ₹350 coffee expense", use_container_width=True):
        clicked_prompt = "Log an expense of 350 INR for Coffee in my expense sheet."
with quick_cols[3]:
    if st.button("📋 Show my tasks", use_container_width=True):
        clicked_prompt = "Show my pending tasks in Google Tasks."

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

def generate_demo_response(user_input: str) -> str:
    """Return a safe, realistic simulated response for public demo visitors."""
    q = user_input.lower()
    footer = "\n\n---\n*🛡️ Simulated Demo Response — Live personal tools (Gmail, Calendar, Tasks, Docs, Sheets) are locked in Public Demo Mode.*"

    if any(k in q for k in ("calendar", "schedule", "meeting", "event", "today")):
        return (
            "📅 **Sample Calendar Summary (Demo Data)**\n\n"
            "- **10:00 AM – 10:30 AM**: Architecture Sync *(Google Meet)*\n"
            "- **02:00 PM – 03:00 PM**: n8n Workflow Review\n"
            "- **05:00 PM – 05:30 PM**: Sprint Wrap-up\n\n"
            "*(Tool simulated: Google Calendar — Get Many Events)*" + footer
        )
    if any(k in q for k in ("email", "gmail", "unread", "inbox", "mail", "send")):
        return (
            "✉️ **Sample Gmail Summary (Demo Data)**\n\n"
            "- **Project Update**: Weekly deployment checklist is ready for review.\n"
            "- **Newsletter**: Latest AI agent orchestration patterns.\n\n"
            "*(Outbound email sending & real inbox reads are disabled in Public Demo Mode)*" + footer
        )
    if any(k in q for k in ("expense", "coffee", "inr", "sheet", "budget", "spend", "rupee", "₹")):
        return (
            "💰 **Sample Expense Log (Demo Data)**\n\n"
            "- **Category**: Food & Beverage\n"
            "- **Item**: Coffee\n"
            "- **Amount**: ₹350 INR\n"
            "- **Status**: Simulated append to Google Sheets Expense Tracker" + footer
        )
    if any(k in q for k in ("task", "todo", "to-do", "checklist")):
        return (
            "📋 **Sample Pending Tasks (Demo Data)**\n\n"
            "1. Finalize README documentation\n"
            "2. Review n8n agent prompt guardrails\n"
            "3. Prepare live walkthrough for recruiters\n\n"
            "*(Tool simulated: Google Tasks — Get Many Tasks)*" + footer
        )
    if any(k in q for k in ("doc", "note", "report")):
        return (
            "📄 **Sample Google Docs Action (Demo Data)**\n\n"
            "Drafted structured notes under **\"Agentic AI Roadmap\"** with key milestones.\n\n"
            "*(Tool simulated: Google Docs — Create/Update Document)*" + footer
        )
    return (
        "🤖 **n8n Multi-Agent Workflow (Demo Simulation)**\n\n"
        f"Received your prompt: *\"{user_input}\"*\n\n"
        "In **Owner Mode**, the n8n AI Agent routes this through OpenAI + Window Memory and selects from "
        "SerpApi Search, Google Calendar, Gmail, Google Tasks, Google Docs, or Google Sheets.\n\n"
        "Try one of the quick-action buttons above (Calendar, Emails, Expense, or Tasks) to preview each tool's output!"
        + footer
    )


# Function to execute assistant response
def handle_assistant_interaction(user_input: str):
    # Display user message in chat message container
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call n8n webhook (Owner Mode) or return safe simulated output (Demo Mode)
    with st.chat_message("assistant", avatar="🤖"):
        if not st.session_state.is_owner:
            assistant_response = generate_demo_response(user_input)
            st.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            return

        if not WEBHOOK_URL:
            st.error("⚠️ `N8N_WEBHOOK_URL` is not configured. Set it in `.env` or Streamlit Secrets.")
            return

        with st.spinner("🤖 Agent is thinking & executing tools..."):
            try:
                response = requests.post(WEBHOOK_URL, json={"message": user_input}, timeout=120)

                if response.status_code == 200:
                    data = response.json()
                    # Handling various n8n response structures:
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "output" in data[0]:
                        assistant_response = data[0]["output"]
                    elif isinstance(data, dict) and "output" in data:
                        assistant_response = data["output"]
                    elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
                        assistant_response = data[0]
                    elif isinstance(data, dict) and "text" in data:
                        assistant_response = data["text"]
                    else:
                        assistant_response = str(data)

                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    error_msg = f"⚠️ **Error {response.status_code}**: Unable to get response from n8n. Please ensure the workflow is published or active."
                    st.error(error_msg)
            except requests.exceptions.Timeout:
                st.error("⏳ **Request Timed Out**: The agent is taking longer to process the multi-step tools.")
            except requests.exceptions.RequestException:
                st.error("❌ **Connection Error**: Could not reach the configured n8n webhook.")

# Trigger from quick button click or chat input
if clicked_prompt:
    handle_assistant_interaction(clicked_prompt)
    st.rerun()

if prompt := st.chat_input("Ask your assistant anything (e.g. 'Add a meeting tomorrow at 3 PM')..."):
    handle_assistant_interaction(prompt)
