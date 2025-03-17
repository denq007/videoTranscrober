import tkinter as tk
from tkinter import filedialog, messagebox
import mlx_whisper
import torch
#from moviepy.editor import VideoFileClip
from moviepy import VideoFileClip
import os
import platform

# Import appropriate Whisper library based on OS
if platform.system() == "Darwin":  # macOS
    import mlx_whisper as whisper_engine
else:  # Windows or other
    import whisper as whisper_engine

class VideoTranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Video Transcriber")
        self.root.geometry("400x250")

        # Check device availability (informational, MLX handles optimization itself)
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Detected device: {device}")

        # No model preloading, MLX loads it on demand
        self.model = None
        self.video_path = ""
        self.transcription = ""

        self.label = tk.Label(root, text="Select a video file for transcription")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Video", command=self.select_video)
        self.select_button.pack(pady=5)

        self.video_label = tk.Label(root, text="No video selected")
        self.video_label.pack(pady=5)

        # Выбор языка с опцией "auto"
        self.lang_label = tk.Label(root, text="Transcription language (or auto):")
        self.lang_label.pack()
        self.lang_var = tk.StringVar(value="auto")
        self.lang_menu = tk.OptionMenu(root, self.lang_var, "auto", "ru", "en", "es", "fr", "de")
        self.lang_menu.pack(pady=5)

        self.transcribe_button = tk.Button(root, text="Transcribe", command=self.transcribe_video, state="disabled")
        self.transcribe_button.pack(pady=5)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)

    def select_video(self):
        self.video_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")]
        )
        if self.video_path:
            self.video_label.config(text=f"Selected: {os.path.basename(self.video_path)}")
            self.transcribe_button.config(state="normal")

    def transcribe_video(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please select a video first!")
            return

        try:
            video_filename = os.path.basename(self.video_path)

            self.status_label.config(text=f"Extracting audio from {video_filename}...")
            self.root.update()

            video = VideoFileClip(self.video_path)
            audio_path = "temp_audio.wav"
            video.audio.write_audiofile(audio_path, codec="pcm_s16le", fps=16000)

            self.status_label.config(text=f"Transcribing {video_filename} (detecting Russian and English)...")
            self.root.update()

            print(f"Starting transcription of file: {video_filename}")
            if platform.system() == "Darwin":  # macOS
                if self.lang_var.get() == "auto":
                    result = whisper_engine.transcribe(
                        audio_path,
                        path_or_hf_repo="mlx-community/whisper-large-v3-mlx",
                        task="transcribe",
                        language="ru",
                        verbose=True,
                        initial_prompt="This file contains Russian and English text. Do not translate, just transcribe."
                    )
                else:
                    result = whisper_engine.transcribe(
                        audio_path,
                        path_or_hf_repo="mlx-community/whisper-large-v3-mlx",
                        language=self.lang_var.get(),
                        verbose=True
                    )
            else:  # Windows
                # Load Whisper model for Windows
                self.model = whisper_engine.load_model("large") if self.model is None else self.model
                if self.lang_var.get() == "auto":
                    result = self.model.transcribe(
                        audio_path,
                        task="transcribe",
                        language="ru",
                        verbose=True,
                        initial_prompt="This file contains Russian and English text. Do not translate, just transcribe."
                    )
                else:
                    result = self.model.transcribe(
                        audio_path,
                        language=self.lang_var.get(),
                        verbose=True
                    )
            self.transcription = result["text"]

            self.status_label.config(text=f"Transcription of {video_filename} completed!")

            # Automatically save the transcription
            transcription_filename = os.path.splitext(video_filename)[0] + ".txt"
            save_path = os.path.join(os.path.dirname(self.video_path), transcription_filename)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(self.transcription)
            messagebox.showinfo("Success", f"Transcription saved to: {save_path}")

            os.remove(audio_path)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="")

def main():
    root = tk.Tk()
    app = VideoTranscriberApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()