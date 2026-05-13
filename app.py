import streamlit as st
from google import genai
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests
import os

# Load environment variables
load_dotenv()

# Gemini Text Client
text_client = genai.Client(
    api_key=os.getenv("GEMINI_TEXT_API_KEY")
)

# Streamlit Page Config
st.set_page_config(
    page_title="AI Creator Assistant",
    page_icon="🎬",
    layout="wide"
)

# Purple Theme UI
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
    );
    color: white;
    border: none;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #9d4edd,
        #c77dff
    );
}

/* Download Buttons */
.stDownloadButton > button {
    background: #7b2cbf;
    color: white;
    border-radius: 10px;
    border: none;
}

/* Input Fields */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #2d2d5a;
    color: white;
    border-radius: 10px;
    border: 1px solid #9d4edd;
}

/* Text Area */
textarea {
    background-color: #1f1f3d !important;
    color: white !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid #9d4edd;
    padding: 15px;
    border-radius: 15px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: white;
    font-size: 16px;
}

.stTabs [aria-selected="true"] {
    background-color: #7b2cbf;
    border-radius: 10px;
}

/* Images */
img {
    border-radius: 15px;
    border: 2px solid #9d4edd;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title("🎬 AI Creator Assistant")
st.write("Generate viral short-form video,images,reels scripts and AI thumbnails using AI")

# Metrics
m1, m2, m3 = st.columns(3)

m1.metric("Scripts Generated", "100+")
m2.metric("AI Thumbnails", "300+")
m3.metric("Platforms Supported", "3")

# Sidebar
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

# Generate Button
generate_btn = st.button("🚀 Generate Content")

# Text Generation Function
def generate_script(topic, niche, platform, style, duration):

    prompt = f"""
    You are a professional viral content creator.

    Generate a high-engagement short-form video script.

    Topic: {topic}
    Niche: {niche}
    Platform: {platform}
    Content Style: {style}
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
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text

# Thumbnail Generation Function
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

# Main Logic
if generate_btn:

    if topic.strip() == "":
        st.warning("Please enter a topic")

    else:

        # Generate Script
        with st.spinner("Generating AI Script..."):

            generated_script = generate_script(
                topic,
                niche,
                platform,
                content_style,
                duration
            )

        # Thumbnail Prompt
        thumbnail_prompt = f"""
        Create a viral cinematic thumbnail.

        Topic: {topic}
        Niche: {niche}
        Style: {content_style}

        Ultra realistic,
        highly engaging,
        social media optimized,
        neon lighting,
        trendy aesthetic,
        clickworthy YouTube thumbnail
        """

        # Generate 3 Thumbnails
        with st.spinner("Generating AI Thumbnails..."):

            thumbnails = generate_thumbnails(
                thumbnail_prompt,
                count=3
            )

        # Tabs
        tab1, tab2 = st.tabs(
            ["📜 AI Script", "🖼️ AI Thumbnails"]
        )

        # Script Tab
        with tab1:

            st.subheader("📜 AI Generated Script")

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

            with st.expander("See Thumbnail Prompt"):

                st.write(thumbnail_prompt)

        # Thumbnail Tab
        with tab2:

            st.subheader("🖼️ AI Generated Thumbnails")

            cols = st.columns(3)

            for idx, image in enumerate(thumbnails):

                with cols[idx]:

                    st.image(
                        image,
                        use_container_width=True
                    )

                    image_path = f"thumbnail_{idx+1}.png"

                    image.save(image_path)

                    with open(image_path, "rb") as file:

                        st.download_button(
                            label=f"📥 Download {idx+1}",
                            data=file,
                            file_name=image_path,
                            mime="image/png"
                        )

# Footer
st.markdown("---")

