import os
import time
import random
import string
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
from TTS.api import TTS

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.getbbox(test_line)[2] > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)
    return lines

def render_text(text, highlight_index, font_path, fontsize=80, max_width=600, intermediates_dir=None):
    font = ImageFont.truetype(font_path, fontsize)
    lines = wrap_text(text, font, max_width)
    max_text_width = max(font.getbbox(line)[2] for line in lines)
    height = (font.getbbox(lines[0])[3] - font.getbbox(lines[0])[1]) * len(lines) + 20
    width = max_text_width + 40

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0, 180))

    y_offset = 5
    word_index = 0
    found_highlight = False

    for line in lines:
        line_width = font.getbbox(line)[2]
        x_offset = (width - line_width) // 2
        for word in line.split():
            stripped_word = word.strip(string.punctuation)
            color = (255, 255, 0, 255) if word_index == highlight_index and not found_highlight else (255, 255, 255, 255)
            if word_index == highlight_index:
                found_highlight = True
            draw.text((x_offset, y_offset), stripped_word, font=font, fill=color)
            x_offset += font.getbbox(stripped_word + " ")[2]
            word_index += 1
        y_offset += font.getbbox(line)[3] - font.getbbox(line)[1]

    if intermediates_dir is None:
        intermediates_dir = "generator/intermediates"
    os.makedirs(intermediates_dir, exist_ok=True)

    frame_path = os.path.join(intermediates_dir, f"highlighted_text_{highlight_index}.png")
    image.save(frame_path)
    return frame_path

def pick_random_file(folder, extensions):
    files = [f for f in os.listdir(folder) if f.lower().endswith(extensions)]
    if not files:
        raise FileNotFoundError(f"No files with extensions {extensions} found in {folder}")
    return os.path.join(folder, random.choice(files))

def create_video(
    quote,
    fonts_dir,
    backgrounds_dir,
    music_dir,
    intermediates_dir,
    outputs_dir,
):
    os.makedirs(intermediates_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    # Create a timestamped folder inside outputs_dir
    output_folder = os.path.join(outputs_dir, timestamp)
    os.makedirs(output_folder, exist_ok=True)

    # Save video as "short.mp4" inside that folder
    video_output = os.path.join(output_folder, "short.mp4")

    # Save the quote text to quote.txt inside the output folder
    quote_txt_path = os.path.join(output_folder, "quote.txt")
    with open(quote_txt_path, "w", encoding="utf-8") as f:
        f.write(quote)

    tts_path = os.path.join(intermediates_dir, f"speech_{timestamp}.mp3")

    font_path = pick_random_file(fonts_dir, ('.ttf', '.otf'))
    background_path = pick_random_file(backgrounds_dir, ('.mp4', '.mov'))
    music_path = pick_random_file(music_dir, ('.mp3', '.wav'))

    # FGoogle TTS
    #tts = gTTS(quote, lang="en")
    #tts.save(tts_path)

    # Coqui TTS
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    tts.tts_to_file(text=quote, file_path=tts_path)

    audio_clip = AudioFileClip(tts_path)
    music_clip = AudioFileClip(music_path).set_duration(audio_clip.duration + 1).volumex(0.3)
    duration = audio_clip.duration

    original_video = VideoFileClip(background_path).subclip(0, duration + 1)
    w, h = original_video.size
    target_aspect = 9 / 16
    new_width = int(h * target_aspect)
    x_center = w // 2
    crop_x1 = max(0, x_center - new_width // 2)
    crop_x2 = min(w, x_center + new_width // 2)
    video_clip = original_video.crop(x1=crop_x1, x2=crop_x2, y1=0, y2=h)

    words = quote.replace('"', '').split()
    text_clips = []
    for i in range(len(words)):
        text_frame = render_text(
            quote,
            i,
            font_path=font_path,
            max_width=new_width - 40,
            intermediates_dir=intermediates_dir,
        )
        text_clip = ImageClip(text_frame).set_position("center").set_start(i * (duration / len(words))).set_duration(duration / len(words))
        text_clips.append(text_clip)

    final_audio = CompositeAudioClip([audio_clip, music_clip])
    final_video = CompositeVideoClip([video_clip] + text_clips).set_audio(final_audio)
    final_video.write_videofile(video_output, fps=30, codec="libx264")

    # Clean up intermediates
    for f in os.listdir(intermediates_dir):
        os.remove(os.path.join(intermediates_dir, f))

    return video_output

