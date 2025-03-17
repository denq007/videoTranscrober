# Offline Video Transcriber

**Offline Video Transcriber** is an application designed for transcribing video files into text using Whisper, optimized for Apple Silicon via MLX.

## 🚀 Features

- 🎙 Supports English and Russian transcription without translation.
- 💾 Automatically saves the output with the same name as the input file (e.g., `video.mp4` → `video.txt`).
- ⚡ High accuracy and speed thanks to the `mlx-community/whisper-large-v3-mlx` model, optimized for Apple M2 Pro.
- 🌍 Allows language selection, including automatic detection.
- 🖥 Works on macOS (Apple Silicon) and Windows.

## 🔧 Installation

### 1️⃣ Install Dependencies

#### macOS:
```bash
pip install mlx-whisper moviepy tkinter
brew install ffmpeg
```

> **Note:** If you don’t have Homebrew installed, you can install it first:
> ```bash
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> ```

#### Windows:
1. **Download and install FFmpeg** from [ffmpeg.org](https://ffmpeg.org).
2. **Extract FFmpeg** and place it in a folder (e.g., `C:\ffmpeg`).
3. **Add FFmpeg to the system PATH:**
   - Right-click "This PC" → **Properties** → **Advanced system settings**.
   - Go to the **Environment Variables** section.
   - Find `Path` under **System Variables** and add the path to the `bin` folder inside your FFmpeg directory (e.g., `C:\ffmpeg\bin`).
4. **Install Python dependencies:**
   ```bash
   pip install whisper moviepy tkinter
   ```

### 2️⃣ Run the Application

To quickly start the application, copy and paste the following command into your terminal:

#### macOS/Linux:
```bash
python3 transcriber.py
```

#### Windows:
```powershell
python transcriber.py
```

## 🛠 How It Works

1. Select a video file (`.mp4`, `.avi`, `.mkv`, `.mov`).
2. Choose a transcription language (or use auto-detect).
3. Click **Transcribe** and wait for the process to complete.
4. The transcribed text will be saved automatically in the same folder as the video.

Enjoy seamless offline video transcription! 🎉
