"""
Voice to Image Generator - Streamlit Application

AI-powered application that converts voice messages into images using:
- OpenAI Whisper (speech-to-text)
- GPT-4 Turbo (prompt enhancement)
- DALL-E 3 (image generation)
"""

import os
import time
import streamlit as st
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from src.voice.transcriber import VoiceTranscriber
from src.llm.prompt_enhancer import PromptEnhancer
from src.image.generator import ImageGenerator
from src.utils.logger import get_logger

# Import audio recorder
from st_audiorec import st_audiorec

# Page configuration
st.set_page_config(
    page_title="Voice to Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        color: #1e1e1e;
        font-size: 1rem;
        line-height: 1.5;
    }
    .model-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        background-color: #1f77b4;
        color: white;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    .log-entry {
        font-family: monospace;
        font-size: 0.9rem;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-left: 3px solid #1f77b4;
        background-color: #f8f9fa;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
def initialize_session_state():
    """Initialize all session state variables."""
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    if 'enhanced_prompt' not in st.session_state:
        st.session_state.enhanced_prompt = None
    if 'generated_image_path' not in st.session_state:
        st.session_state.generated_image_path = None
    if 'generated_image_url' not in st.session_state:
        st.session_state.generated_image_url = None
    if 'pipeline_time' not in st.session_state:
        st.session_state.pipeline_time = None
    if 'generation_count' not in st.session_state:
        st.session_state.generation_count = 0


def add_log(message: str, level: str = "info"):
    """Add a log entry to session state."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        'timestamp': timestamp,
        'message': message,
        'level': level
    })


def reset_session():
    """Reset the session to start fresh."""
    st.session_state.transcript = None
    st.session_state.enhanced_prompt = None
    st.session_state.generated_image_path = None
    st.session_state.generated_image_url = None
    st.session_state.pipeline_time = None
    st.session_state.logs = []


def main():
    """Main application function."""
    initialize_session_state()

    # Header
    st.title("🎨 Voice to Image Generator")
    st.markdown("Convert your voice descriptions into stunning AI-generated images")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This app converts voice messages to images using OpenAI's AI models:

        **Pipeline:**
        1. 🎤 Record voice message
        2. 🎧 Transcribe with Whisper
        3. ✨ Enhance with GPT-4
        4. 🖼️ Generate with DALL-E 3
        """)

        st.divider()

        st.header("⚙️ Configuration")

        # Get config from environment
        whisper_model = os.getenv("WHISPER_MODEL", "whisper-1")
        gpt_model = os.getenv("GPT_MODEL", "gpt-4-turbo")
        dalle_model = os.getenv("DALLE_MODEL", "dall-e-3")
        dalle_size = os.getenv("DALLE_SIZE", "1024x1024")
        dalle_quality = os.getenv("DALLE_QUALITY", "standard")
        dalle_style = os.getenv("DALLE_STYLE", "vivid")

        st.markdown(f"""
        **Models in use:**
        - Whisper: `{whisper_model}`
        - GPT: `{gpt_model}`
        - DALL-E: `{dalle_model}`

        **Image settings:**
        - Size: `{dalle_size}`
        - Quality: `{dalle_quality}`
        - Style: `{dalle_style}`
        """)

        st.divider()

        st.header("📊 Stats")
        st.metric("Images Generated", st.session_state.generation_count)

        if st.session_state.pipeline_time:
            st.metric("Last Generation Time", f"{st.session_state.pipeline_time:.2f}s")

        st.divider()

        if st.button("🔄 Start New Generation", use_container_width=True):
            reset_session()
            st.rerun()

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("🎤 Step 1: Record Voice")
        st.markdown("Click the microphone button to record your image description")

        # Browser-based audio recorder
        audio_bytes = st_audiorec()

        if audio_bytes:
            # Audio recorded successfully (st_audiorec already shows player)
            add_log("🎤 Audio recording received", "info")

            # Process button
            if st.button("🚀 Generate Image", type="primary", use_container_width=True):
                start_time = time.time()

                try:
                    # Check API key
                    api_key = os.getenv("OPENAI_API_KEY")
                    if not api_key:
                        st.error("❌ OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
                        add_log("❌ Error: OpenAI API key not found", "error")
                        return

                    # Initialize components
                    with st.spinner("Initializing AI models..."):
                        transcriber = VoiceTranscriber(
                            api_key=api_key,
                            model=whisper_model,
                            language="en"
                        )
                        enhancer = PromptEnhancer(
                            api_key=api_key,
                            model=gpt_model,
                            temperature=float(os.getenv("GPT_TEMPERATURE", "0.7"))
                        )
                        generator = ImageGenerator(
                            api_key=api_key,
                            model=dalle_model,
                            size=dalle_size,
                            quality=dalle_quality,
                            style=dalle_style
                        )
                        add_log("✓ AI models initialized", "info")

                    # Step 1: Transcribe audio
                    with st.spinner("🎧 Transcribing audio with Whisper..."):
                        transcript = transcriber.transcribe(audio_bytes, "recording.wav")
                        st.session_state.transcript = transcript
                        add_log(f"✓ Transcription: \"{transcript[:100]}...\"", "info")

                    # Step 2: Enhance prompt
                    with st.spinner("✨ Enhancing prompt with GPT-4..."):
                        enhanced_prompt = enhancer.enhance(transcript)
                        st.session_state.enhanced_prompt = enhanced_prompt
                        add_log(f"✓ Enhanced prompt: \"{enhanced_prompt[:100]}...\"", "info")

                    # Step 3: Generate image
                    with st.spinner("🖼️ Generating image with DALL-E 3..."):
                        image_path, image_url = generator.generate(enhanced_prompt)
                        st.session_state.generated_image_path = image_path
                        st.session_state.generated_image_url = image_url
                        add_log(f"✓ Image generated: {image_path}", "info")

                    # Calculate total time
                    total_time = time.time() - start_time
                    st.session_state.pipeline_time = total_time
                    st.session_state.generation_count += 1

                    add_log(f"🎉 Pipeline completed in {total_time:.2f}s", "info")

                    st.success(f"✅ Image generated successfully in {total_time:.2f}s!")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    add_log(f"❌ Error: {str(e)}", "error")

    with col2:
        st.header("📊 Results")

        # Display transcript
        if st.session_state.transcript:
            st.subheader("📄 Transcript")
            st.markdown(f'<div class="info-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="model-badge">whisper-1 (en)</span>', unsafe_allow_html=True)

        # Display enhanced prompt
        if st.session_state.enhanced_prompt:
            st.subheader("✨ Enhanced Prompt")
            st.markdown(f'<div class="info-box">{st.session_state.enhanced_prompt}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="model-badge">{gpt_model}</span>', unsafe_allow_html=True)

        # Display generated image
        if st.session_state.generated_image_path:
            st.subheader("🖼️ Generated Image")
            st.image(st.session_state.generated_image_path, use_column_width=True)
            st.markdown(
                f'<span class="model-badge">{dalle_model}</span>'
                f'<span class="model-badge">{dalle_size}</span>'
                f'<span class="model-badge">{dalle_quality}</span>',
                unsafe_allow_html=True
            )

            # Download button
            with open(st.session_state.generated_image_path, "rb") as file:
                st.download_button(
                    label="💾 Download Image",
                    data=file,
                    file_name=Path(st.session_state.generated_image_path).name,
                    mime="image/png",
                    use_container_width=True
                )

    # Logs section (collapsible)
    st.divider()
    with st.expander("📊 Console Logs", expanded=False):
        if st.session_state.logs:
            for log in reversed(st.session_state.logs):
                icon = "✓" if log['level'] == "info" else "⚠️" if log['level'] == "warning" else "❌"
                st.markdown(
                    f'<div class="log-entry">[{log["timestamp"]}] {icon} {log["message"]}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No logs yet. Record audio and generate an image to see logs.")

    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            Powered by OpenAI • Whisper + GPT-4 + DALL-E 3
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    # Initialize logger
    logger = get_logger(level=os.getenv("LOG_LEVEL", "INFO"))
    logger.log_info("🚀 Voice to Image Generator started")

    # Run the app
    main()
