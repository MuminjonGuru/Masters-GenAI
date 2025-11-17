# 🚀 Quick Start Guide

Get up and running with Voice to Image Generator in 5 minutes!

## ⚡ TL;DR

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# 3. Run the app
streamlit run app.py
```

## 📋 Step-by-Step

### 1. Prerequisites Check

Make sure you have:
- ✅ Python 3.9 or higher (`python --version`)
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Working microphone

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Streamlit (UI framework)
- OpenAI SDK (Whisper + GPT-4 + DALL-E)
- Supporting libraries

### 3. Configure API Key

**Option A: Using .env file (recommended)**
```bash
# Copy the example
cp .env.example .env

# Edit .env with your favorite editor
# Add your OpenAI API key:
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Option B: Set environment variable directly**
```bash
# Windows
set OPENAI_API_KEY=sk-proj-your-key-here

# macOS/Linux
export OPENAI_API_KEY=sk-proj-your-key-here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### 5. Generate Your First Image

1. **Click Record** - Click the microphone button in the app
2. **Allow Microphone** - Click "Allow" when browser asks for permission
3. **Speak** - Say: *"A cat sitting on a couch"*
4. **Stop** - Click the stop button when done
5. **Generate** - Click the "🚀 Generate Image" button
6. **Wait** - The pipeline takes ~10-15 seconds
7. **Enjoy** - Your image appears on the right!

## 🎯 What to Try

### Simple Examples
- *"A red sports car"*
- *"A beach at sunset"*
- *"A cute puppy"*

### Detailed Examples
- *"A futuristic cityscape at night with neon lights"*
- *"A magical forest with glowing mushrooms"*
- *"An astronaut riding a horse on Mars"*

### Artistic Styles
- *"A portrait in oil painting style"*
- *"A landscape in watercolor style"*
- *"An abstract geometric design"*

## 🔧 Configuration (Optional)

Want to customize? Edit `.env`:

```env
# Use HD quality images (more expensive)
DALLE_QUALITY=hd

# Use portrait orientation
DALLE_SIZE=1024x1792

# Use natural style (less dramatic)
DALLE_STYLE=natural

# Increase creativity in prompt enhancement
GPT_TEMPERATURE=0.9
```

## ⚠️ Common First-Time Issues

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### "API key not found"
Make sure `.env` file exists and contains:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Microphone not working
- Click "Allow" when browser asks for permission
- Check browser microphone settings
- Try Chrome or Edge browser
- Ensure microphone is connected and working

### Streamlit won't start
```bash
# Try specifying port
streamlit run app.py --server.port 8502
```

## 💡 Pro Tips

1. **Speak clearly** - Better transcription = better images
2. **Be specific** - "A sunny beach" vs "A beach" makes a difference
3. **Check logs** - Expand "Console Logs" to see what's happening
4. **Download images** - Use the download button to save favorites
5. **Start fresh** - Click "🔄 Start New Generation" to reset

## 📊 Expected Performance

| Stage | Time | Cost |
|-------|------|------|
| Transcription | 1-2s | $0.003 |
| Enhancement | 2-3s | $0.02 |
| Image Generation | 5-10s | $0.04 |
| **Total** | **~10-15s** | **~$0.06** |

## 🎉 You're Ready!

That's it! You now have a working voice-to-image generator.

Try different descriptions and see what amazing images you can create!

---

Need help? Check the main [README.md](README.md) for detailed documentation.
