# 🎬 AI Face-Aware Video Editor

This project is a smart video highlight tool that uses **AI face detection** to improve the quality of stitched video edits. Unlike most AI video tools that crop faces or overlay captions on top of people, this editor **keeps faces centered**, avoids covering them with text, and generates **10-second reels** from multiple clips.

---

## 📌 Features

- 🤖 **Face Detection:** Uses `face_recognition` to find faces in each frame
- ✂️ **Smart Cropping:** Centers the frame around the most prominent face with stabilized tracking
- 💬 **Dynamic Text Placement:** Automatically places captions above or below faces with fixed positioning per clip
- 🎞️ **Video Stitching:** Combines multiple 3-4s clips into a single 10s highlight reel
- 📐 **Standard Output:** 720×1280 resolution (vertical 9:16 phone format)
- 🎯 **Multi-Format Support:** Handles MP4, MOV, and AVI input files
- ⚙️ **Modular Code:** Python-based, easily extendable
- 🛡️ **Stable Processing:** Face detection smoothing eliminates glitching

---

## 🚀 Quick Start

Choose your preferred installation method:

### Option A: Docker (Recommended - Works on Any Platform)

#### Prerequisites
- Docker and Docker Compose installed

#### 1. Clone and Prepare
```bash
git clone <repository-url>
cd ai-face-edit-poc

# Create data directory if it doesn't exist
mkdir -p data outputs
```

#### 2. Add Your Videos
Place your video files in the `data/` folder:
```bash
data/input1.mp4
data/input2.mp4
data/input3.mp4
# (supports .mp4, .mov, .avi)
```

#### 3. Run with Docker
```bash
# Multi-clip highlight reel (default)
docker-compose up

# Single video processing
docker-compose --profile single up face-editor-single

# Development shell access
docker-compose --profile dev up face-editor-dev
```

Output videos will appear in the `outputs/` folder.

### Option B: Local Installation (macOS)

#### Prerequisites
- macOS (tested on macOS 12+)
- Homebrew package manager

#### 1. Install Miniconda (Recommended for Fast Setup)
```bash
# Install miniconda via Homebrew
brew install miniconda

# Initialize conda (restart terminal after this)
conda init

# Accept terms of service
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

#### 2. Create Environment and Install Dependencies
```bash
# Create conda environment with Python 3.10
conda create -n face-ai python=3.10 -y

# Activate environment
conda activate face-ai

# Install packages via conda-forge (much faster than pip)
conda install -c conda-forge opencv face_recognition moviepy -y
```

#### 3. Prepare Your Videos
Place your video files in the `data/` folder:

**For Single Video Processing:**
```bash
data/input.mp4
```

**For Multi-Clip Highlight Reel:**
```bash
data/input1.mp4
data/input2.mp4
data/input3.mp4
# (supports .mp4, .mov, .avi)
```

#### 4. Run the Editor

**Activate Environment (each session):**
```bash
# Source bash profile first (if needed)
source ~/.bash_profile
conda activate face-ai
```

**Single Video Processing:**
```bash
python src/main.py
```
Output: `outputs/face_cropped_output.mp4`

**Multi-Clip Highlight Reel:**
```bash
python src/main_stitch.py
```
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
├── Dockerfile         # Docker container definition
├── docker-compose.yml # Docker Compose configuration
├── .dockerignore      # Docker ignore rules
├── .gitignore         # Git ignore rules
├── CLAUDE.md          # Development documentation
└── README.md          # This file
```

---

## 🔧 Technical Details

### Environment
- **Python Version:** 3.10.x (required for face_recognition compatibility)
- **Installation Method:** Conda (recommended) or pip + virtual environment
- **Platform:** macOS (primary), Linux/Windows (untested)

### Dependencies
```
opencv-python    # Computer vision and video processing
face-recognition # Face detection using dlib
moviepy         # Video assembly (legacy - now using OpenCV)
```

### How It Works
1. **Face Detection:** Analyzes each frame to locate faces using advanced ML models
2. **Face Smoothing:** Averages last 5 detections to eliminate jitter and glitching
3. **Smart Cropping:** Centers the crop around the largest detected face
4. **Edge Handling:** Adjusts crop boundaries when faces are near frame edges
5. **Fallback Processing:** Resizes to target resolution when no faces are detected
6. **Text Positioning:** Determines fixed text position per clip to prevent jumping
7. **Video Assembly:** Uses OpenCV VideoWriter with mp4v codec for compatibility

### Key Configuration
- **Target Resolution:** 720×1280 - vertical phone format (configurable in source files)
- **Clip Duration:** 3.5 seconds per input video for highlight reels
- **Final Duration:** Exactly 10 seconds for highlight reels
- **Text Styling:** White text on black background with padding
- **Face Smoothing:** 5-frame rolling average with 3-frame minimum for processing

---

## 🐛 Troubleshooting

### Docker Issues
- **Docker build fails:** Ensure you have enough disk space (build requires ~2-3GB)
- **Permission denied:** Make sure Docker has access to the project directory
- **Slow build:** First build takes time due to compiling face_recognition dependencies
- **Out of memory:** Increase Docker memory allocation in Docker Desktop settings

### Installation Issues
- **Slow pip installation:** Use conda instead - it's much faster for these packages
- **face_recognition build errors:** Ensure you're using Python 3.10.x
- **FFmpeg errors:** The project now uses OpenCV VideoWriter instead of MoviePy to avoid codec issues

### Runtime Issues
- **No faces detected:** Check video quality and lighting
- **Text jumping:** Fixed in latest version with per-clip position locking
- **First clip glitching:** Fixed with face detection smoothing
- **Empty output:** Ensure input videos are in correct format and location

### macOS Specific
- **Bash profile errors:** The `bind` command error can be ignored
- **conda activate fails:** Run `conda init` and restart your terminal

---

## 🛠 Development Workflow

The processing pipeline follows these steps:

1. **Load Video:** Extract frames from input video(s)
2. **Detect Faces:** Use `face_recognition` library with smoothing
3. **Select Primary Face:** Choose largest face when multiple are detected
4. **Calculate Crop:** Center crop area around the smoothed face position
5. **Determine Text Position:** Fix text placement per clip to prevent jumping
6. **Apply Text:** Add captions with consistent positioning
7. **Reassemble:** Create final video using OpenCV VideoWriter

---

## 🚀 Future Features

- 🎵 Background music integration
- 😊 Smile and emotional expression detection
- 📊 Emotion-based highlight scoring
- 🌐 Web UI (Streamlit or Gradio)
- 🖼️ Smart thumbnail generation
- 🔌 API-ready packaging for integrations
- 🎨 Custom text styling options
- 🔄 Batch processing for multiple video sets

---

## 💡 Why This Matters

Most AI video editors suffer from poor face handling - they either crop faces out of frame or overlay text directly on people's faces. This project solves both problems with a **face-aware pipeline** that:

- ✅ Always keeps faces properly centered and visible
- ✅ Intelligently places text to avoid covering faces
- ✅ Eliminates glitching with smoothed face detection
- ✅ Maintains professional video quality at 720×1280 (vertical phone format)
- ✅ Provides both single-video and multi-clip workflows
- ✅ Offers fast, reliable installation via conda
- ✅ Uses stable OpenCV backend for maximum compatibility

Perfect for content creators, social media managers, and anyone building AI-powered video tools that respect visual storytelling principles.