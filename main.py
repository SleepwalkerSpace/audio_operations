import os

from pydub import AudioSegment


def get_audio_frame_rate(audio_file_path:str) -> int:
    audio_file = AudioSegment.from_mp3(audio_file_path)
    return audio_file.frame_rate


def tonality_adjustment(level:int, source_path:str, output_path:str):
    frame_rate = get_audio_frame_rate(source_path)

    os.system(
        "ffmpeg -i '{}' -filter_complex 'asetrate={}*2^({}/12),atempo=1/2^({}/12)' {}".format(
            source_path, frame_rate, level, level, output_path
        ))
    pass


project_path = os.getcwd()
project_static_path = os.path.join(project_path, "static")


def main():
    fname = "back.mp3"
    level = 1
    source_path = os.path.join(project_static_path, fname)
    output_path = os.path.join(project_static_path, "output_{}.mp3".format(level))
    tonality_adjustment(level, source_path, output_path)

if __name__ == "__main__":
    main()