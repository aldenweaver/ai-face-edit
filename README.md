# AI Face Edit PoC

This project auto-edits videos using face detection to improve framing and export. Useful for creators, AI video tools, and generative content pipelines.

## Features

- Face detection using `face_recognition`
- Smart center-cropping on detected faces
- Reassembles edited video using MoviePy

## Usage

1. Place your input video in the `data/` folder and name it `input.mp4`.
2. Run the script:

```bash
python src/main.py
```

3. The edited video will be saved in the `outputs/` folder.

# 🎬 AI Face-Aware Video Editor

This project is a smart video highlight tool that uses **AI face detection** to improve the quality of stitched video edits. Unlike most AI video tools that crop faces or overlay captions on top of people, this editor **keeps faces centered**, avoids covering them with text, and generates **10-second reels** from multiple clips.

---

## 📌 Features

- 🤖 **Face Detection:** Uses `face_recognition` to find faces in each frame  
- ✂️ **Smart Cropping:** Centers the frame around the most prominent face  
- 💬 **Text Placement:** Dynamically places captions above or below faces  
- 🎞️ **Video Stitching:** Combines multiple 3–4s clips into a single 10s highlight  
- 📐 **Standard Output:** 1280×720 resolution  
- ⚙️ **Modular Code:** Python-based, easily extendable

---

## 🚀 Quick Start

### 1. Install Python 3.10 (recommended via pyenv)
```bash
pyenv install 3.10.13
pyenv virtualenv 3.10.13 face-ai-env
pyenv activate face-ai-env
```

2. Clone the project & install dependencies
```bash

cd ai-face-edit-poc
pip install -r requirements.txt
3. Add Input Videos
Put your clips in the data/ folder and name them:

```bash

data/input1.mp4
data/input2.mp4
data/input3.mp4
```

4. Run the face-aware stitching script
```bash
python src/main_stitch.py
```

This creates a 10-second face-aware highlight reel at:

```bash
outputs/smart_reel.mp4
```

📁 Project Structure
```bash
ai-face-edit-poc/
├── data/               # Input video clips
├── outputs/            # Generated highlight reel
├── src/
│   ├── main.py         # Face cropper (single video)
│   └── main_stitch.py  # Full highlight reel builder
├── requirements.txt
├── .gitignore
└── README.md
```

🔧 Requirements
```
opencv-python
face-recognition
moviepy
```
Use Python 3.10 for full compatibility with face_recognition.

🛠 Development Workflow
Detect face in each frame

Crop and center the face

Dynamically place captions outside the face box

Rebuild each video segment

Stitch all clips together into a highlight reel

Future Features
Add background music
Detect smiles or emotional expression
Emotion-based highlight scoring
Web UI (e.g. Streamlit or Gradio)
Smart thumbnail picker
API-ready packaging for integrations

💡 Why This Matters
AI editors often cut off faces or overlay text poorly. This project fixes that with a face-aware pipeline that respects visual storytelling, improves UX, and sets the foundation for truly creator-friendly AI tooling.