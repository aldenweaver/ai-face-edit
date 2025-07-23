# 🎬 AI Face-Aware Video Editor

This project is a smart video highlight tool that uses **AI face detection** to improve the quality of stitched video edits. Unlike most AI video tools that crop faces or overlay captions on top of people, this editor **keeps faces centered**, avoids covering them with text, and generates **10-second reels** from multiple clips.

---

## 📌 Features

- 🤖 **Face Detection:** Uses `face_recognition` to find faces in each frame  
- ✂️ **Smart Cropping:** Centers the frame around the most prominent face  
- 💬 **Dynamic Text Placement:** Automatically places captions above or below faces to avoid covering them  
- 🎞️ **Video Stitching:** Combines multiple 3-4s clips into a single 10s highlight reel  
- 📐 **Standard Output:** 1280×720 resolution  
- 🎯 **Multi-Format Support:** Handles MP4, MOV, and AVI input files
- ⚙️ **Modular Code:** Python-based, easily extendable

---

## 🚀 Quick Start

### 1. Install Python 3.10 (recommended via pyenv)
```bash
pyenv install 3.10.13
pyenv virtualenv 3.10.13 face-ai-env
pyenv activate face-ai-env
```

### 2. Clone the project & install dependencies
```bash
cd ai-face-edit-poc
pip install -r requirements.txt
```

### 3. Choose Your Workflow

#### Option A: Single Video Processing
Place your video in the `data/` folder as `input.mp4` and run:
```bash
python src/main.py
```
Output: `outputs/face_cropped_output.mp4`

#### Option B: Multi-Clip Highlight Reel (Recommended)
Put your clips in the `data/` folder and name them:
```bash
data/input1.mp4
data/input2.mp4  
data/input3.mp4
# (supports .mp4, .mov, .avi)
```

Run the face-aware stitching script:
  # Activate the environment
  ```bash
  source ~/.bash_profile && conda activate face-ai
  ```

  # For single video processing
  ```bash
  python src/main.py
  ```

  # For multi-clip highlight reel
  ```bash
  python src/main_stitch.py
  ```

  Make sure you have video files in the data/ folder (input.mp4 for single
  video or input1.mp4, input2.mp4, etc. for multiple clips).


Output: `outputs/smart_reel.mp4` (exactly 10 seconds)

---

## 📁 Project Structure
```bash
ai-face-edit-poc/
├── data/               # Input video clips
├── outputs/            # Generated videos
├── src/
│   ├── main.py         # Single video face cropper
│   └── main_stitch.py  # Multi-clip highlight reel builder
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── CLAUDE.md          # Development documentation
└── README.md          # This file
```

---

## 🔧 Technical Details

### Requirements
```
opencv-python
face-recognition
moviepy
```
**Note:** Use Python 3.10 for full compatibility with `face_recognition`.

### How It Works
1. **Face Detection:** Analyzes each frame to locate faces using advanced ML models
2. **Smart Cropping:** Centers the crop around the largest detected face
3. **Edge Handling:** Adjusts crop boundaries when faces are near frame edges
4. **Fallback Processing:** Resizes to target resolution when no faces are detected
5. **Text Overlay:** Dynamically places captions based on face position (top/bottom)
6. **Video Assembly:** Uses MoviePy to reconstruct the final video with libx264 codec

### Key Configuration
- **Target Resolution:** 1280×720 (configurable in source files)
- **Clip Duration:** 3.5 seconds per input video for highlight reels
- **Final Duration:** Exactly 10 seconds for highlight reels
- **Text Styling:** White text on black background with padding

---

## 🛠 Development Workflow

The processing pipeline follows these steps:

1. **Load Video:** Extract frames from input video(s)
2. **Detect Faces:** Use `face_recognition` library for face detection
3. **Select Primary Face:** Choose largest face when multiple are detected
4. **Calculate Crop:** Center crop area around the selected face
5. **Apply Text:** Add captions with intelligent placement
6. **Reassemble:** Create final video using MoviePy

---

## 🚀 Future Features

- 🎵 Background music integration
- 😊 Smile and emotional expression detection  
- 📊 Emotion-based highlight scoring
- 🌐 Web UI (Streamlit or Gradio)
- 🖼️ Smart thumbnail generation
- 🔌 API-ready packaging for integrations

---

## 💡 Why This Matters

Most AI video editors suffer from poor face handling - they either crop faces out of frame or overlay text directly on people's faces. This project solves both problems with a **face-aware pipeline** that:

- ✅ Always keeps faces properly centered and visible
- ✅ Intelligently places text to avoid covering faces  
- ✅ Maintains professional video quality at 1280×720
- ✅ Provides both single-video and multi-clip workflows
- ✅ Offers a foundation for truly creator-friendly AI tooling

Perfect for content creators, social media managers, and anyone building AI-powered video tools that respect visual storytelling principles.