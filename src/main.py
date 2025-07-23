import cv2
import face_recognition
import os
from moviepy.editor import ImageSequenceClip

# === Config ===
INPUT_VIDEO = "data/input.mp4"
OUTPUT_VIDEO = "outputs/face_cropped_output.mp4"
TARGET_RES = (1280, 720)  # width, height

# === Load video ===
cap = cv2.VideoCapture(INPUT_VIDEO)
fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
frame_count = 0

print("Extracting frames and detecting faces...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    # Detect faces (returns top, right, bottom, left)
    face_locations = face_recognition.face_locations(frame)

    if face_locations:
        # Pick the largest face
        face_location = max(face_locations, key=lambda box: (box[2] - box[0]) * (box[1] - box[3]))
        top, right, bottom, left = face_location

        # Center the crop around the face
        face_center_x = (left + right) // 2
        face_center_y = (top + bottom) // 2

        w, h = TARGET_RES
        x1 = max(face_center_x - w // 2, 0)
        y1 = max(face_center_y - h // 2, 0)
        x2 = x1 + w
        y2 = y1 + h

        cropped = frame[y1:y2, x1:x2]

        # Resize to exact output resolution if needed
        if cropped.shape[:2] != (h, w):
            cropped = cv2.resize(cropped, (w, h))
        frames.append(cropped)
    else:
        # No face detected — just resize or keep the original frame
        resized = cv2.resize(frame, TARGET_RES)
        frames.append(resized)

cap.release()
print(f"Processed {frame_count} frames.")

# === Export video ===
print("Exporting edited video...")
clip = ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames], fps=fps)
clip.write_videofile(OUTPUT_VIDEO, codec='libx264')

print("Done! Output saved to:", OUTPUT_VIDEO)