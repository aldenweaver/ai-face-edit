import cv2
import face_recognition
import os
import glob
# from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageSequenceClip  # Not needed, using OpenCV
import numpy as np

# === Config ===
INPUT_DIR = "data/"
OUTPUT_VIDEO = "outputs/smart_reel.mp4"
TARGET_RES = (1280, 720)  # width, height
TARGET_DURATION = 10.0  # seconds for final highlight reel
CLIP_DURATION = 3.5  # seconds per input clip (3-4s as mentioned in README)

def add_text_overlay(frame, text, face_location=None):
    """
    Add text overlay dynamically placed to avoid covering faces
    """
    if text is None or text == "":
        return frame
    
    height, width = frame.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    font_thickness = 2
    text_color = (255, 255, 255)  # White text
    bg_color = (0, 0, 0)  # Black background
    
    # Get text size
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_width, text_height = text_size
    
    # Default position (center top)
    text_x = (width - text_width) // 2
    text_y = 60
    
    # If face detected, place text to avoid covering it
    if face_location:
        top, right, bottom, left = face_location
        face_center_y = (top + bottom) // 2
        
        # If face is in upper half, place text at bottom
        if face_center_y < height // 2:
            text_y = height - 40
        # Otherwise keep text at top
    
    # Draw background rectangle
    padding = 10
    cv2.rectangle(frame, 
                 (text_x - padding, text_y - text_height - padding),
                 (text_x + text_width + padding, text_y + padding),
                 bg_color, -1)
    
    # Draw text
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    
    return frame

def process_video_clip(input_path, clip_text=None):
    """
    Process a single video clip with face detection and text overlay
    """
    print(f"Processing {input_path}...")
    
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate frames to extract for target clip duration
    frames_to_extract = min(int(fps * CLIP_DURATION), total_frames)
    frames = []
    
    frame_count = 0
    while cap.isOpened() and frame_count < frames_to_extract:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Detect faces
        face_locations = face_recognition.face_locations(frame)
        primary_face = None
        
        if face_locations:
            # Pick the largest face
            primary_face = max(face_locations, key=lambda box: (box[2] - box[0]) * (box[1] - box[3]))
            top, right, bottom, left = primary_face
            
            # Center the crop around the face
            face_center_x = (left + right) // 2
            face_center_y = (top + bottom) // 2
            
            w, h = TARGET_RES
            x1 = max(face_center_x - w // 2, 0)
            y1 = max(face_center_y - h // 2, 0)
            x2 = min(x1 + w, frame.shape[1])
            y2 = min(y1 + h, frame.shape[0])
            
            # Adjust if we're at edges
            if x2 - x1 < w:
                x1 = max(0, x2 - w)
            if y2 - y1 < h:
                y1 = max(0, y2 - h)
                
            cropped = frame[y1:y2, x1:x2]
            
            # Resize to exact output resolution if needed
            if cropped.shape[:2] != (h, w):
                cropped = cv2.resize(cropped, (w, h))
                
            # Update face location for text placement (relative to cropped frame)
            primary_face = (
                max(0, top - y1),
                min(w, right - x1), 
                min(h, bottom - y1),
                max(0, left - x1)
            )
            
            processed_frame = cropped
        else:
            # No face detected — just resize
            processed_frame = cv2.resize(frame, TARGET_RES)
        
        # Add text overlay if provided
        if clip_text:
            processed_frame = add_text_overlay(processed_frame, clip_text, primary_face)
            
        frames.append(processed_frame)
    
    cap.release()
    return frames, fps

def main():
    """
    Main function to create face-aware highlight reel
    """
    # Find all input videos
    video_patterns = [
        os.path.join(INPUT_DIR, "input*.mp4"),
        os.path.join(INPUT_DIR, "input*.mov"),
        os.path.join(INPUT_DIR, "input*.avi")
    ]
    
    input_videos = []
    for pattern in video_patterns:
        input_videos.extend(glob.glob(pattern))
    
    input_videos.sort()  # Process in order
    
    if not input_videos:
        print("No input videos found in data/ directory.")
        print("Please add videos named input1.mp4, input2.mp4, etc.")
        return
    
    print(f"Found {len(input_videos)} input videos:")
    for video in input_videos:
        print(f"  - {video}")
    
    # Process each video clip
    all_frames = []
    fps = 30  # Default fps, will be updated from first video
    
    for i, video_path in enumerate(input_videos):
        # Generate sample text for each clip (you can customize this)
        clip_text = f"Clip {i+1}"  # Simple text, can be made more sophisticated
        
        frames, video_fps = process_video_clip(video_path, clip_text)
        if i == 0:
            fps = video_fps
            
        all_frames.extend(frames)
        print(f"  Added {len(frames)} frames from {os.path.basename(video_path)}")
    
    if not all_frames:
        print("No frames processed. Check your input videos.")
        return
    
    # Trim to target duration
    target_frame_count = int(fps * TARGET_DURATION)
    if len(all_frames) > target_frame_count:
        # Take frames evenly distributed across the content
        indices = np.linspace(0, len(all_frames) - 1, target_frame_count, dtype=int)
        all_frames = [all_frames[i] for i in indices]
        print(f"Trimmed to {len(all_frames)} frames for {TARGET_DURATION}s duration")
    
    # Export final video
    print("Creating final highlight reel...")
    os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)
    
    # Use OpenCV VideoWriter instead of MoviePy to avoid FFmpeg issues
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, int(fps), TARGET_RES)
    
    for frame in all_frames:
        out.write(frame)
    
    out.release()
    
    print(f"✅ Done! Face-aware highlight reel saved to: {OUTPUT_VIDEO}")
    print(f"   Duration: {len(all_frames) / fps:.1f} seconds")
    print(f"   Resolution: {TARGET_RES[0]}x{TARGET_RES[1]}")
    print(f"   FPS: {fps}")

if __name__ == "__main__":
    main()