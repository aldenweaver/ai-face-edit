# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered face-aware video editor that automatically centers video frames around detected faces and creates highlight reels. The project uses OpenCV for video processing, face_recognition for face detection, and MoviePy for video assembly.

## Architecture

### Core Components
- **Face Detection Pipeline**: Uses `face_recognition` library to detect faces in video frames
- **Smart Cropping**: Centers crop around the largest detected face, falls back to standard resize if no faces found
- **Dynamic Text Placement**: Automatically positions captions above or below faces to avoid covering them
- **Video Processing**: Frame-by-frame processing with OpenCV, reassembled using MoviePy
- **Multi-clip Stitching**: Combines multiple 3-4s clips into 10-second highlight reels

### Project Structure
```
ai-face-edit-poc/
├── data/               # Input video files (input.mp4, input1.mp4, etc.)
├── outputs/            # Generated output videos
├── src/
│   ├── main.py         # Single video face-cropping processor
│   └── main_stitch.py  # Multi-clip highlight reel builder
└── requirements.txt    # Python dependencies
```

### Key Technical Details
- **Target Resolution**: 1280×720 (configurable in main.py)
- **Face Selection**: Selects largest face when multiple faces detected
- **Fallback Handling**: Resizes to target resolution when no faces detected
- **Color Space**: Handles BGR→RGB conversion for MoviePy compatibility

## Development Commands

### Environment Setup
```bash
# Recommended: Use Python 3.10 for face_recognition compatibility
pyenv install 3.10.13
pyenv virtualenv 3.10.13 face-ai-env
pyenv activate face-ai-env

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Single video processing (requires data/input.mp4)
python src/main.py

# Multi-clip highlight reel creation (requires data/input*.mp4)
python src/main_stitch.py

# Outputs:
# - Single video: outputs/face_cropped_output.mp4
# - Highlight reel: outputs/smart_reel.mp4
```

### Input/Output
- **Single video input**: Place video file as `data/input.mp4`
- **Multi-clip input**: Place videos as `data/input1.mp4`, `data/input2.mp4`, etc.
- **Outputs**: 
  - Single video: `outputs/face_cropped_output.mp4`
  - Highlight reel: `outputs/smart_reel.mp4` (10-second duration)
- **Supported formats**: MP4, MOV, AVI (output uses libx264 codec)

## Dependencies
- `opencv-python`: Video frame processing and computer vision
- `face-recognition`: Face detection and location
- `moviepy`: Video assembly and export

## Implementation Details

### main_stitch.py Features
- **Multi-video Processing**: Automatically finds and processes input*.mp4/mov/avi files
- **Clip Duration**: Extracts 3.5 seconds from each input video 
- **Text Overlay**: Adds configurable captions with smart placement around faces
- **Target Duration**: Creates exactly 10-second highlight reels
- **Frame Distribution**: Intelligently samples frames when content exceeds target duration

### Face Detection & Cropping Logic
- Detects all faces in each frame using face_recognition library
- Selects largest face when multiple faces are present  
- Centers crop around the selected face
- Handles edge cases when face is near frame boundaries
- Falls back to standard resize when no faces detected

### Text Placement Algorithm
- Analyzes face position in frame (upper/lower half)
- Places text at bottom if face is in upper half, top otherwise
- Uses white text on black background for visibility
- Adds padding around text for better readability