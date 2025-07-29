from generator.create_video import create_video
from generator.fetch_quote import fetch_quote
import os

if __name__ == "__main__":
    quote = fetch_quote()

    # Define your asset directories here
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
    BACKGROUNDS_DIR = os.path.join(BASE_DIR, "assets", "background")
    MUSIC_DIR = os.path.join(BASE_DIR, "assets", "music")
    INTERMEDIATES_DIR = os.path.join(BASE_DIR, "outputs", "intermediates")
    OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs", "shorts")

    output_path = create_video(
        quote,
        fonts_dir=FONTS_DIR,
        backgrounds_dir=BACKGROUNDS_DIR,
        music_dir=MUSIC_DIR,
        intermediates_dir=INTERMEDIATES_DIR,
        outputs_dir=OUTPUTS_DIR,
    )
    print(f"Video created at: {output_path}")
