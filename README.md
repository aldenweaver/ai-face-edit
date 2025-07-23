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