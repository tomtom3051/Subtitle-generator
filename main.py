import time
import math
import ffmpeg

from faster_whisper import WhisperModel
import whisper


#Based on:
#https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg


input_video = "input.mp4"


input_video_name = input_video.replace(".mp4", "")



def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio


def transcribe(audio):
    # model = WhisperModel("small")
    # segments, info = model.transcribe(audio)
    # language = info[0]
    # print("Transcription language", info[0])
    # segments = list(segments)
    # for segment in segments:
    #     # print(segment)
    #     print("[%.2fs -> %.2fs] %s" %
    #           (segment.start, segment.end, segment.text))
    # return language, segments
    model = whisper.load_model("small")
    result = model.transcribe(audio)
    language = result["language"]
    segments = result["segments"]
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" %
               (segment["start"], segment["end"], segment["text"]))
    return language, segments


def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def generate_subtitle_file(language, segments):
    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment["start"])
        segment_end = format_time(segment["end"])
        segment_text = segment["text"]
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment_text} \n"
        text += "\n"
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    return subtitle_file

def run():

    extracted_audio = extract_audio()

    language, segments = transcribe(audio=extracted_audio)
    subtitle_file = generate_subtitle_file(language=language,segments=segments)
run()