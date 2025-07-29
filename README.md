# Motivation Shorts Generator
This tool generates motivational short videos.


# Motivation Shorts Generator

This tool generates motivational short videos.

Built with:
- Python
- Coqui-AI TTS

---

## Features

- ✅ Fetches a random motivation quote from the remote server
- ✅ Synthetizes the quote into sound
- ✅ Stitches together AI voice, background video and background music into one continuou video
- ✅ Adds text highlight as the voice is progressing
- ✅ Supports random selection from multiple assets
- ✅ Docker support ready

---

## Generate a Video

Use the `main.py` script:

```bash
python3 main.py
```
---

##  Run via Docker

### 1. Build Docker image

```bash
docker build -t motivation-shorts-generator docker/.
```

### 2. Run Generator Script

```bash
docker run --rm -v "$(pwd)":/app -v "$(pwd)/outputs":/app/outputs motivation-shorts-generator

```