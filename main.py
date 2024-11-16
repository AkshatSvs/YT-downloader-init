import tkinter as tk
from tkinter import ttk
import yt_dlp
import subprocess
import os

# Function to download and convert audio/video from YouTube URL
def download_video(url, format_type, save_path='./', update_ui_callback=None):
    try:
        # Define yt-dlp options based on the selected format type (MP3 or MP4)
        if format_type == 'MP3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'quiet': False,
            }
        elif format_type == 'MP4':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'quiet': False,
            }

        # Download the video/audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading {format_type} from: {url}")
            update_ui_callback("Downloading...")  # Update UI to show downloading status
            ydl.download([url])

        # If MP3 was selected, convert the audio from webm to MP3 using FFmpeg
        if format_type == 'MP3':
            video_title = ydl.prepare_filename(ydl.extract_info(url, download=False))
            audio_path = os.path.splitext(video_title)[0] + '.webm'
            mp3_path = os.path.splitext(audio_path)[0] + '.mp3'
            print(f"Converting {audio_path} to MP3...")
            subprocess.run(['ffmpeg', '-i', audio_path, '-vn', '-acodec', 'mp3', '-ab', '192k', mp3_path], check=True)
            os.remove(audio_path)  # Clean up the original webm file
            print(f"Audio downloaded and converted to MP3: {mp3_path}")

        update_ui_callback("Download complete! Check your folder.")  # Update UI to show completion

    except Exception as e:
        update_ui_callback("An error occurred. Please try again.")  # Update UI in case of error
        print(f"An error occurred: {str(e)}")

# GUI Constants
FONT = "sans serif"
BUTTON_COLOR = "#0077B6"
FIELD_COLOR = "#90E0EF"

# Initialize main window
window = tk.Tk()
window.title("YouTube Videos Downloader")
window.geometry("800x400")
window.config(bg="#CAF0F8")

# Label to display status
label = tk.Label(window, text="Enter YouTube URL and select format", font=(FONT, 14), bg="#CAF0F8")
label.pack(pady=20)

# Entry widget for URL input
entry = tk.Entry(window, bg=FIELD_COLOR, font=(FONT, 16), relief="solid", bd=1, width=40)
entry.insert(0, "Enter YouTube URL")
entry.pack(pady=10)

# Function to handle the focus events on the entry widget (clear placeholder text)
def on_focus_in(event):
    if entry.get() == "Enter YouTube URL":
        entry.delete(0, tk.END)  # Clear the placeholder text when the user clicks in

def on_focus_out(event):
    if entry.get() == "":
        entry.insert(0, "Enter YouTube URL")  # Restore the placeholder if the user leaves it blank

# Bind the focus in and focus out events
entry.bind("<FocusIn>", on_focus_in)
entry.bind("<FocusOut>", on_focus_out)

# Dropdown for selecting the video type (MP3 or MP4)
format_label = tk.Label(window, text="Select Format (MP3 or MP4):", font=(FONT, 14), bg="#CAF0F8")
format_label.pack(pady=10)

format_combobox = ttk.Combobox(window, values=["MP3", "MP4"], font=(FONT, 14), width=20)
format_combobox.set("MP3")  # Default value is MP3
format_combobox.pack(pady=10)

# Button click event handler
def on_button_click():
    window.title("Downloading...")
    entered_value = entry.get().strip()
    selected_format = format_combobox.get()
    
    if not entered_value or entered_value == "Enter YouTube URL":
        label.config(text="Please enter a valid YouTube URL!", font=(FONT, 16), fg="red")
    elif selected_format not in ["MP3", "MP4"]:
        label.config(text="Please select a valid format!", font=(FONT, 16), fg="red")
    else:
        video_url = entered_value
        # Pass a callback function to update the label and reset button text
        download_video(video_url, selected_format, update_ui_callback=update_ui)

# Function to update the UI during download and when complete
def update_ui(status_text):
    label.config(text=status_text, font=(FONT, 16), fg="green" if "complete" in status_text else "red")
    if "complete" in status_text or "error" in status_text:
        button.config(text="DOWNLOAD!", state=tk.NORMAL)  # Reset the button text and enable it again

# Download button
button = tk.Button(
    window, 
    text="DOWNLOAD!", 
    font=(FONT, 15), 
    command=on_button_click, 
    bg=BUTTON_COLOR, 
    fg="#fff", 
    width=13, 
    height=2, 
    borderwidth=2, 
    relief="ridge"
)
button.pack(pady=20)

# Run the application
window.mainloop()
