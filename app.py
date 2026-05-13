import streamlit as st
from google import genai
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests
import pyrebase
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Creator Assistant",
    page_icon="🎬",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(
        135deg,
        #0f0c29,
        #302b63,
        #24243e
    );
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1b1636;
    border-right: 1px solid #9d4edd;
}

/* Sidebar Labels */
section[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600 !important;
}

/* Titles */
h1, h2, h3 {
    color: #d0aaff;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(
        90deg,
        #7b2cbf,
        #9d4edd
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 50px !important;
    width: 100% !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

/* Inputs */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #2d2d5a !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #9d4edd !important;
}

/* Placeholder */
input::placeholder {
    color: #cccccc !important;
}

/* Text Area */
textarea {
    background-color: #1f1f3d !important;
    color: white !important;
}

/* Metric Containers */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid #9d4edd;
    padding: 15px;
    border-radius: 15px;
}

/* ALL metric text */
[data-testid="metric-container"] * {
    color: white !important;
}

/* Metric labels */
[data-testid="metric-container"] label,
[data-testid="metric-container"] p,
[data-testid="metric-container"] div {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

/* Metric numbers */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 42px !important;
    font-weight: bold !important;
}

/* Images */
img {
    border-radius: 15px;
    border: 2px solid #9d4edd;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: white !important;
    font-size: 18px;
}

/* Footer */
hr {
    border: 1px solid #9d4edd;
}

</style>
""", unsafe_allow_html=True)

# =========================
# FIREBASE CONFIG
# =========================

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# GEMINI CLIENT
# =========================

text_client = genai.Client(
    api_key=os.getenv("GEMINI_TEXT_API_KEY")
)

# =========================
# LOGIN / SIGNUP
# =========================

if 'user' not in st.session_state:

    st.title("🔐 AI Creator Authentication")

    choice = st.selectbox(
        "Login/Signup",
        ["Login", "Sign Up"]
    )

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    # =========================
    # SIGNUP
    # =========================

    if choice == "Sign Up":

        username = st.text_input("Username")

        if st.button("Create Account"):

            try:

                auth.create_user_with_email_and_password(
                    email,
                    password
                )

                st.success(
                    "Account Created Successfully"
                )

                st.info(
                    "Now login using your email and password"
                )

            except Exception:

                st.error(
                    "Email already exists or password too weak"
                )

    # =========================
    # LOGIN
    # =========================

    if choice == "Login":

        if st.button("Login"):

            try:

                user = auth.sign_in_with_email_and_password(
                    email,
                    password
                )

                st.session_state['user'] = email

                st.success("Login Successful")

                st.rerun()

            except Exception:

                st.error(
                    "Invalid Email or Password"
                )

# =========================
# MAIN APP
# =========================

else:

    # =========================
    # SIDEBAR
    # =========================

    st.sidebar.success(
        f"Logged in as\n\n{st.session_state['user']}"
    )

    if st.sidebar.button("Logout"):

        del st.session_state['user']

        st.rerun()

    # =========================
    # TITLE
    # =========================

    st.title("🎬 AI Creator Assistant")

    st.write(
        "Generate viral short-form videos, reels scripts and AI thumbnails using AI"
    )

    # =========================
    # METRICS
    # =========================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Scripts Generated",
            "100+"
        )

    with col2:
        st.metric(
            "AI Thumbnails",
            "300+"
        )

    with col3:
        st.metric(
            "Platforms Supported",
            "3"
        )

    # =========================
    # SIDEBAR SETTINGS
    # =========================

    st.sidebar.header("⚙️ Content Settings")

    topic = st.sidebar.text_input(
        "Enter Video Topic",
        placeholder="Example: AI replacing jobs"
    )

    niche = st.sidebar.selectbox(
        "Select Niche",
        [
            "Technology",
            "Finance",
            "Fitness",
            "Gaming",
            "Education",
            "Motivation",
            "Travel",
            "Fashion",
            "Food"
        ]
    )

    platform = st.sidebar.selectbox(
        "Select Platform",
        [
            "YouTube Shorts",
            "Instagram Reels",
            "TikTok"
        ]
    )

    content_style = st.sidebar.selectbox(
        "Content Style",
        [
            "Professional",
            "Funny",
            "Motivational",
            "Storytelling",
            "Emotional",
            "Educational"
        ]
    )

    duration = st.sidebar.selectbox(
        "Video Duration",
        [
            "30 Seconds",
            "60 Seconds",
            "90 Seconds"
        ]
    )

    # =========================
    # GENERATE BUTTON
    # =========================

    generate_btn = st.button(
        "🚀 Generate Content"
    )

    # =========================
    # SCRIPT FUNCTION
    # =========================

    def generate_script(
        topic,
        niche,
        platform,
        style,
        duration
    ):

        prompt = f"""
        You are a professional viral content creator.

        Generate a high-engagement short-form video script.

        Topic: {topic}
        Niche: {niche}
        Platform: {platform}
        Style: {style}
        Duration: {duration}

        Generate:
        1. Video Title
        2. Hook
        3. Short-form Script
        4. Scene Structure
        5. CTA
        6. Hashtags
        """

        response = text_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    # =========================
    # THUMBNAIL FUNCTION
    # =========================

    def generate_thumbnails(prompt, count=3):

        url = "https://imageapi.juideepadas1234.workers.dev"

        headers = {
            "Authorization": "Bearer 12345678",
            "Content-Type": "application/json"
        }

        images = []

        for i in range(count):

            data = {
                "prompt": prompt + f" variation {i+1}"
            }

            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            if response.status_code == 200:

                image = Image.open(
                    BytesIO(response.content)
                )

                images.append(image)

        return images

    # =========================
    # GENERATE CONTENT
    # =========================

    if generate_btn:

        if topic.strip() == "":

            st.warning(
                "Please enter a topic"
            )

        else:

            # =========================
            # GENERATE SCRIPT
            # =========================

            with st.spinner(
                "Generating AI Script..."
            ):

                generated_script = generate_script(
                    topic,
                    niche,
                    platform,
                    content_style,
                    duration
                )

            # =========================
            # THUMBNAIL PROMPT
            # =========================

            thumbnail_prompt = f"""
            Create a viral cinematic thumbnail.

            Topic: {topic}
            Niche: {niche}
            Style: {content_style}

            Ultra realistic,
            social media optimized,
            futuristic,
            neon lighting,
            highly engaging,
            clickworthy thumbnail
            """

            # =========================
            # GENERATE THUMBNAILS
            # =========================

            with st.spinner(
                "Generating AI Thumbnails..."
            ):

                thumbnails = generate_thumbnails(
                    thumbnail_prompt,
                    count=3
                )

            # =========================
            # TABS
            # =========================

            tab1, tab2 = st.tabs(
                [
                    "📜 AI Script",
                    "🖼️ AI Thumbnails"
                ]
            )

            # =========================
            # SCRIPT TAB
            # =========================

            with tab1:

                st.subheader(
                    "📜 AI Generated Script"
                )

                st.text_area(
                    "Generated Content",
                    generated_script,
                    height=600
                )

                st.download_button(
                    label="📥 Download Script",
                    data=generated_script,
                    file_name="ai_script.txt",
                    mime="text/plain"
                )

            # =========================
            # THUMBNAILS TAB
            # =========================

            with tab2:

                st.subheader(
                    "🖼️ AI Generated Thumbnails"
                )

                cols = st.columns(3)

                for idx, image in enumerate(
                    thumbnails
                ):

                    with cols[idx]:

                        st.image(
                            image,
                            use_container_width=True
                        )

                        image_path = (
                            f"thumbnail_{idx+1}.png"
                        )

                        image.save(image_path)

                        with open(
                            image_path,
                            "rb"
                        ) as file:

                            st.download_button(
                                label=f"📥 Download {idx+1}",
                                data=file,
                                file_name=image_path,
                                mime="image/png"
                            )

    # =========================
    # FOOTER
    # =========================

    st.markdown("---")


