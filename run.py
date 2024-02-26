import cv2
import imageio
import colorama
import numpy as np
import os
import sys
import threading
import time
from pytube import YouTube
from PIL import Image
from ascii_magic import AsciiArt
from moviepy.editor import *
from pathlib import Path
import pygame
import argparse

colorama.init()

def play_wav(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def convert_frame_to_ascii(frame):
    ascii_frame = AsciiArt.from_pillow_image(Image.fromarray(frame))
    ascii_frame.to_terminal()


def video_to_ascii(file_path, width=400, speed=6):
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        sys.exit(1)

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            convert_frame_to_ascii(frame)
            time.sleep(0.1 / speed)

    except KeyboardInterrupt:
        pass

    cap.release()
    cv2.destroyAllWindows()

def download_complete(stream, file_path):

    video = VideoFileClip(file_path)
    audio_file_path = Path(file_path).stem+".wav"
    video.audio.write_audiofile(audio_file_path)

    animation_thread = threading.Thread(target=video_to_ascii, args=(file_path,))
    wav_thread = threading.Thread(target=play_wav, args=(audio_file_path,))

    
    try:
        animation_thread.start()
        wav_thread.start()

        animate_frame.join()
        wav_thread.join()

    except KeyboardInterrupt:
        pass

def main():

    parser = argparse.ArgumentParser("ASCII Music Video Player")
    parser.add_argument("-l", "--link", help="Link to youtube music video", type=str)
    args = parser.parse_args()

    if args.link:
        #'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        yt = YouTube(args.link, on_complete_callback=download_complete)
        yt.streams.filter(progressive=True, file_extension='mp4')\
        .order_by('resolution')\
        .desc()\
        .first()\
        .download()
    else: 
        print("Please add youtube link as argument\n")
        print("python3 run.py -l https://www.youtube.com/watch?v=dQw4w9WgXcQ\n")

if __name__ == "__main__":
    main()