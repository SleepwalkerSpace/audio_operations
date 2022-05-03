import os

from pydub import AudioSegment


def get_audio_frame_rate(audio_file_path: str) -> int:
    audio_file = AudioSegment.from_mp3(audio_file_path)
    return audio_file.frame_rate

project_path = os.getcwd()
project_static_path = os.path.join(project_path, "static")


def main():

    file_path = os.path.join(project_static_path, "back.mp3")
    rate = get_audio_frame_rate(file_path)
    print(rate)


if __name__ == "__main__":
    main()