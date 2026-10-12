import streamlit as st
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(
    page_title="Web of ACC - Online Admission",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Credentials
SIR_WHATSAPP = os.getenv("NEXT_PUBLIC_SIR_WHATSAPP_NUMBER", "923433000385")  
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

client = None
if OPENROUTER_API_KEY:
    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )

# -------------------------------------------------------------
# 🌐 MAIN VIP WEBSITE
# -------------------------------------------------------------

# Header
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid rgba(245, 158, 11, 0.3);">
    <div>
        <h2 style="color: #fbbf24; margin: 0;">Web of ACC Online Admission</h2>
        <p style="color: #94a3b8; margin: 0; font-size: 12px;">Malir / Alameen City</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="vip-card hover-lift" style="text-align: center; padding: 40px 20px;">
    <span style="background: rgba(245,158,11,0.15); border: 1px solid #f59e0b; color: #fbbf24; padding: 5px 15px; border-radius: 20px; font-size: 12px;">
        ✨ EXCELLENCE IN EDUCATION ✨
    </span>
    <h1 style="font-size: 44px; margin-top: 15px;" class="glow-title">Welcome to ACC Ahmed Coaching Center</h1>
    <p style="color: #cbd5e1; font-size: 17px; max-width: 700px; margin: 0 auto;">
        Empowering students from Class 1 to 2nd Year (Computer Science, Pre-Engineering, Arts, Commerce) with top-tier education and smart guidance in Malir & Alameen City.
    </p>
</div>
""", unsafe_allow_html=True)

# Features Grid
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="vip-card hover-lift">
        <h3 style="color: #fbbf24;">👨‍🏫 Expert Teachers</h3>
        <p style="color: #94a3b8; font-size: 14px;">Highly qualified faculty dedicated to concept clarity and academic growth.</p>
    </div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="vip-card hover-lift">
        <h3 style="color: #fbbf24;">📚 Complete Syllabus</h3>
        <p style="color: #94a3b8; font-size: 14px;">Full course coverage with regular revision and board pattern exam preparation.</p>
    </div>
    """, unsafe_allow_html=True)
with f3:
    st.markdown("""
    <div class="vip-card hover-lift">
        <h3 style="color: #fbbf24;">📝 Weekly Tests</h3>
        <p style="color: #94a3b8; font-size: 14px;">Weekly testing system and monthly performance reports for parents.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Admission Form Section
_, col_form, _ = st.columns([0.5, 2, 0.5])
with col_form:
    st.markdown("""
    <div class="vip-card hover-lift">
        <h2 class="glow-title" style="text-align: center;">Online Admission Form</h2>
        <p style="color: #94a3b8; text-align: center; font-size: 13px;">Fill out details to send request directly to WhatsApp.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("admission_form"):
        s_name = st.text_input("Full Name")
        s_phone = st.text_input("Contact Number")
        s_details = st.text_area("Class & Details (e.g., Computer Science, Pre-Engineering, Arts, Commerce)")
        submitted = st.form_submit_button("📲 Send Request via WhatsApp", use_container_width=True)

        if submitted:
            if s_name and s_phone:
                text_msg = f"*New Online Admission Request - Web of ACC*%0A%0A*Name:* {s_name}%0A*Phone:* {s_phone}%0A*Details:* {s_details}"
                wa_url = f"https://wa.me/{SIR_WHATSAPP}?text={text_msg}"
                st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background:#10b981; color:#020617; text-align:center; padding:12px; border-radius:10px; font-weight:bold; margin-top:10px;">Click Here to Open WhatsApp Chat</div></a>', unsafe_allow_html=True)
            else:
                st.error("Please fill Name and Phone Number!")

# 🤖 100% STRICT GUARDRAILED CHATBOT IN SIDEBAR
with st.sidebar:
    st.markdown("### 🤖 ACC AI Assistant")
    st.markdown("<p style='font-size:12px; color:#94a3b8;'>Ahmed Coaching Center Official Assistant</p>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Assalamualikum! Welcome to Web of ACC. Aap admissions, kisi bhi class ki fee, ya coaching details ke baare mein pooch sakte hain."}
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_query = st.chat_input("Ask about ACC fees, classes...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        q = user_query.lower()
        bot_reply = ""
        
        # 1. Greetings
        if any(w in q for w in ["salam", "assalam", "hi", "hello", "hey"]):
            bot_reply = "Walaikum Assalam! Web of ACC (Ahmed Coaching Center, Malir/Alameen City) mein khushamdeed. Aap kis class ki fee ya admission detail janna chahte hain?"
        
        # 2. Strict Exact Single-Class Match (Hard Guardrail)
        elif any(c in q for c in ["1st year", "eleventh", "11th"]):
            bot_reply = "1st Year ki monthly fee **Rs. 4,000** hai."
        elif any(c in q for c in ["2nd year", "twelfth", "12th"]):
            bot_reply = "2nd Year ki monthly fee **Rs. 4,000** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?1\b', q) and not re.search(r'\b(10|11|12|1st)\b', q):
            bot_reply = "Class 1 ki monthly fee **Rs. 2,000** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?2\b', q) and not re.search(r'\b(12|2nd)\b', q):
            bot_reply = "Class 2 ki monthly fee **Rs. 2,000** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?3\b', q):
            bot_reply = "Class 3 ki monthly fee **Rs. 2,000** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?4\b', q):
            bot_reply = "Class 4 ki monthly fee **Rs. 2,000** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?5\b', q):
            bot_reply = "Class 5 ki monthly fee **Rs. 2,000** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?6\b', q):
            bot_reply = "Class 6 ki monthly fee **Rs. 2,500** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?7\b', q):
            bot_reply = "Class 7 ki monthly fee **Rs. 2,500** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?8\b', q):
            bot_reply = "Class 8 ki monthly fee **Rs. 2,500** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?9\b', q) or "matric" in q or "9th" in q:
            bot_reply = "Class 9th ki monthly fee **Rs. 3,000** hai."
        elif re.search(r'\b(class|cls|grade|class\s*)?10\b', q) or "10th" in q:
            bot_reply = "Class 10th ki monthly fee **Rs. 3,000** hai."

        # 3. All Classes Fee Structure Request
        elif any(w in q for w in ["sari", "sab", "all", "full list", "entire", "structure"]):
            bot_reply = (
                "**ACC Coaching Center Fee Structure:**\n"
                "- Class 1 to 5: Rs. 2,000 / month\n"
                "- Class 6 to 8: Rs. 2,500 / month\n"
                "- Class 9 & 10 (Matric): Rs. 3,000 / month\n"
                "- 1st Year & 2nd Year: Rs. 4,000 / month"
            )

        # 4. OpenRouter API Fallback for Complex Queries
        elif client and OPENROUTER_API_KEY:
            try:
                response = client.chat.completions.create(
                    model="google/gemini-flash-1.5",
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are the strict official AI assistant for ACC (Ahmed Coaching Center) in Malir & Alameen City, Karachi. "
                                "FEE LIST:\n"
                                "- Class 1 to 5: Rs. 2,000\n"
                                "- Class 6 to 8: Rs. 2,500\n"
                                "- Class 9 & 10: Rs. 3,000\n"
                                "- 1st & 2nd Year: Rs. 4,000\n\n"
                                "STRICT RULES:\n"
                                "1. If the user asks for a single specific class fee, answer ONLY for that specific class. Never list other classes.\n"
                                "2. If the user asks anything unrelated to ACC coaching, admissions, classes, or fees, strictly refuse by saying: "
                                "'Maaf kijiye ga, main sirf ACC Coaching Center, classes, fees aur admissions ke hawale se maloomat de sakta hoon.'"
                            )
                        },
                        {"role": "user", "content": user_query}
                    ],
                    max_tokens=100
                )
                bot_reply = response.choices[0].message.content
            except Exception:
                bot_reply = "Maaf kijiye ga, main sirf ACC Coaching Center, classes, fees aur admissions ke hawale se maloomat de sakta hoon."
        else:
            bot_reply = "Maaf kijiye ga, main sirf ACC Coaching Center, classes, fees aur admissions ke hawale se maloomat de sakta hoon."

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.write(bot_reply)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 12px;'>© 2026 Web of ACC - Ahmed Coaching Center. All Rights Reserved.</p>", unsafe_allow_html=True)
