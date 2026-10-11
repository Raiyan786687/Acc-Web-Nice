import streamlit as st
import streamlit.components.v1 as components
import os
import time
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
SIR_WHATSAPP = os.getenv("NEXT_PUBLIC_SIR_WHATSAPP_NUMBER", "923492584693")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

client = None
if OPENROUTER_API_KEY:
    try:
        client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENROUTER_API_KEY,
        )
    except Exception:
        client = None

# Query Parameter & Session Check for Permanent 1-Time Surprise
if "seen" in st.query_params or "has_seen_birthday" in st.session_state:
    st.session_state.has_seen_birthday = True
else:
    st.session_state.has_seen_birthday = False

if "show_celebration" not in st.session_state:
    st.session_state.show_celebration = False

# -------------------------------------------------------------
# 🎁 1. MAILBOX SURPRISE (STRICT 1-TIME ONLY)
# -------------------------------------------------------------
if not st.session_state.has_seen_birthday and not st.session_state.show_celebration:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="vip-card hover-lift" style="text-align: center;">
            <div style="font-size: 70px;">🎁</div>
            <h2 class="glow-title">Special Surprise Mailbox</h2>
            <p style="color: #cbd5e1;">Click below to open your birthday surprise card!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("👆 Open Surprise Gift", use_container_width=True):
            st.session_state.has_seen_birthday = True
            st.session_state.show_celebration = True
            # Set permanent query parameter in URL so it never repeats
            st.query_params["seen"] = "true"
            st.rerun()

# -------------------------------------------------------------
# 🎈 2. CELEBRATION SCREEN
# -------------------------------------------------------------
elif st.session_state.show_celebration:
    st.balloons()
    _, col2, _ = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div class="vip-card hover-lift" style="text-align: center; border-color: #f59e0b;">
            <div style="font-size: 50px;">🎆✨🎇</div>
            <h1 class="glow-title" style="font-size: 40px;">🎉 Happy Birthday Sir! 🎉</h1>
            <p style="font-size: 18px; color: #e2e8f0; font-style: italic; margin: 20px 0;">
                "To an incredible mentor who inspires, guides, and shapes the future of students every single day. Thank you for your leadership at ACC!" ❤️✨
            </p>
            <p style="color: #94a3b8; font-size: 13px;">Opening Web of ACC in 5 seconds...</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(5)
        st.session_state.show_celebration = False
        st.rerun()

# -------------------------------------------------------------
# 🌐 3. MAIN VIP WEBSITE
# -------------------------------------------------------------
else:
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

    # 🤖 DYNAMIC & GUARDRAILED CHATBOT IN SIDEBAR
    with st.sidebar:
        st.markdown("### 🤖 ACC AI Assistant")
        st.markdown("<p style='font-size:12px; color:#94a3b8;'>Smart ACC Admission Assistant</p>", unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Assalamualikum! ACC Ahmed Coaching Center mein khushamdeed. Aap classes ya admission ke hawale se kya poochna chahte hain?"}
            ]

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_query = st.chat_input("Ask about ACC...")
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)

            q = user_query.lower()
            bot_reply = ""
            
            if client and OPENROUTER_API_KEY:
                try:
                    messages_for_api = [
                        {
                            "role": "system",
                            "content": (
                                "You are the official AI Assistant for ACC Ahmed Coaching Center located in Malir / Alameen City. "
                                "Be polite, helpful, and concise. ACC offers classes from Class 1 to Class 10, as well as 11th & 12th "
                                "(Computer Science, Pre-Engineering, Arts, Commerce). "
                                "Respond in friendly Roman Urdu or English matching the user. "
                                "If the user asks general greetings like salam/hi, greet them back nicely. "
                                "If the user asks off-topic questions unrelated to studies or coaching, politely state that you can only answer queries about ACC Coaching Center."
                            )
                        }
                    ]
                    for m in st.session_state.chat_history[-5:]:
                        messages_for_api.append({"role": m["role"], "content": m["content"]})

                    response = client.chat.completions.create(
                        model="meta-llama/llama-3.2-3b-instruct:free",
                        messages=messages_for_api,
                        max_tokens=150
                    )
                    bot_reply = response.choices[0].message.content
                except Exception:
                    bot_reply = ""

            if not bot_reply:
                if "salam" in q or "assalam" in q:
                    bot_reply = "Walaikum Assalam! Web of ACC mein aapka istiqbaal hai. Main aapki kya madad kar sakta hoon?"
                elif any(w in q for w in ["hi", "hello", "hey", "hlo"]):
                    bot_reply = "Hello! ACC Ahmed Coaching Center ki janib se khushamdeed. Aap admission ke bare mein pooch rahe hain?"
                elif any(w in q for w in ["class", "course", "subject", "field", "stream"]):
                    bot_reply = "ACC mein Class 1 se 2nd Year (Computer Science, Pre-Engineering, Arts, Commerce) ki tayyari karwai jaati hai."
                elif any(w in q for w in ["admission", "apply", "fee", "form", "daakhla"]):
                    bot_reply = "Online admission ke liye baraye meherbani saath diye gaye form ko fill karke WhatsApp button par click karein."
                elif any(w in q for w in ["location", "address", "kahan", "place"]):
                    bot_reply = "ACC Coaching Center Malir / Alameen City mein sthit hai."
                elif any(w in q for w in ["teacher", "faculty", "sir"]):
                    bot_reply = "ACC mein highly qualified aur experienced teachers parhenay ke liye maujood hain."
                else:
                    bot_reply = "Main ACC Coaching Center ka official assistant hoon. Main sirf admissions, classes, aur coaching ke hawale se madad kar sakta hoon."

            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.write(bot_reply)

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 12px;'>© 2026 Web of ACC - Ahmed Coaching Center. All Rights Reserved.</p>", unsafe_allow_html=True)
