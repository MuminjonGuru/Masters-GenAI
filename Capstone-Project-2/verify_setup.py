"""
Setup Verification Script
Checks that all modules can be imported and basic functionality works.
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Voice to Image Generator - Setup Verification")
print("=" * 60)
print()

# Check Python version
print("1. Checking Python version...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 9:
    print(f"   ✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} (OK)")
else:
    print(f"   ✗ Python {python_version.major}.{python_version.minor}.{python_version.micro} (Need 3.9+)")
    sys.exit(1)
print()

# Check environment file
print("2. Checking environment configuration...")
env_file = Path(".env")
env_example = Path(".env.example")

if env_example.exists():
    print("   ✓ .env.example found")
else:
    print("   ✗ .env.example not found")

if env_file.exists():
    print("   ✓ .env file found")
    # Check for API key
    with open(env_file) as f:
        content = f.read()
        if "OPENAI_API_KEY" in content and "your_openai_api_key_here" not in content:
            print("   ✓ OpenAI API key configured")
        else:
            print("   ⚠ OpenAI API key not set (add your key to .env)")
else:
    print("   ⚠ .env file not found (copy from .env.example)")
print()

# Check directories
print("3. Checking directory structure...")
required_dirs = ["src", "src/voice", "src/llm", "src/image", "src/utils", "outputs", "screenshots"]
for dir_path in required_dirs:
    if Path(dir_path).exists():
        print(f"   ✓ {dir_path}/")
    else:
        print(f"   ✗ {dir_path}/ (missing)")
print()

# Check required files
print("4. Checking required files...")
required_files = [
    "app.py",
    "requirements.txt",
    "README.md",
    "src/__init__.py",
    "src/voice/__init__.py",
    "src/voice/transcriber.py",
    "src/llm/__init__.py",
    "src/llm/prompt_enhancer.py",
    "src/image/__init__.py",
    "src/image/generator.py",
    "src/utils/__init__.py",
    "src/utils/logger.py",
]
for file_path in required_files:
    if Path(file_path).exists():
        print(f"   ✓ {file_path}")
    else:
        print(f"   ✗ {file_path} (missing)")
print()

# Test imports
print("5. Testing module imports...")
try:
    from src.utils.logger import get_logger
    print("   ✓ Logger module")
except ImportError as e:
    print(f"   ✗ Logger module: {e}")

try:
    from src.voice.transcriber import VoiceTranscriber
    print("   ✓ Voice transcriber module")
except ImportError as e:
    print(f"   ✗ Voice transcriber module: {e}")

try:
    from src.llm.prompt_enhancer import PromptEnhancer
    print("   ✓ Prompt enhancer module")
except ImportError as e:
    print(f"   ✗ Prompt enhancer module: {e}")

try:
    from src.image.generator import ImageGenerator
    print("   ✓ Image generator module")
except ImportError as e:
    print(f"   ✗ Image generator module: {e}")

try:
    import streamlit as st
    print("   ✓ Streamlit")
except ImportError:
    print("   ✗ Streamlit (run: pip install -r requirements.txt)")

try:
    import openai
    print("   ✓ OpenAI SDK")
except ImportError:
    print("   ✗ OpenAI SDK (run: pip install -r requirements.txt)")

try:
    import colorlog
    print("   ✓ Colorlog")
except ImportError:
    print("   ✗ Colorlog (run: pip install -r requirements.txt)")

try:
    from dotenv import load_dotenv
    print("   ✓ Python-dotenv")
except ImportError:
    print("   ✗ Python-dotenv (run: pip install -r requirements.txt)")

try:
    import requests
    print("   ✓ Requests")
except ImportError:
    print("   ✗ Requests (run: pip install -r requirements.txt)")

try:
    from PIL import Image
    print("   ✓ Pillow")
except ImportError:
    print("   ✗ Pillow (run: pip install -r requirements.txt)")

print()

# Summary
print("=" * 60)
print("Verification complete!")
print("=" * 60)
print()
print("Next steps:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Configure API key in .env file")
print("3. Run the app: streamlit run app.py")
print()
print("For detailed instructions, see README.md or QUICKSTART.md")
print()
