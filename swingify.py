from pathlib import Path
import subprocess
from io import BytesIO
from pydub import AudioSegment


def stretch_audio(audio: Path, speed_up_factor: float) -> AudioSegment:
    audio_segment = stretch_audio_ffmpeg(audio, speed_up_factor)
    return audio_segment


def stretch_audio_ffmpeg(audio: Path, speed_up_factor: float):
    command = [
        "ffmpeg", "-i", audio.__str__(),
        "-filter:a", f"atempo={speed_up_factor}",
        "-f", "wav", "pipe:1"
    ]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    output_audio_bytes = BytesIO(process.stdout)
    audio_segment = AudioSegment.from_file(output_audio_bytes, format="wav")
    return audio_segment


def swing_ify(audio: Path, bpm: float) -> AudioSegment:
    """Swing-ifies the audio.

    :param audio: Path to audio
    :param bpm: Tempo of audio
    :return: AudioSegment instance of swinged audio, call export() on it
    """
    spb = 60 / bpm
    ms_pb = spb * 1000
    stretched = stretch_audio(audio, 3 / 4)  # "slower"
    squished = stretch_audio(audio, 3 / 2)  # "faster"

    combined_segments: list[AudioSegment] = []

    # pad silence to avoid OOB issues
    stretched_proc = stretched + AudioSegment.silent(duration=10)
    squished_proc = squished + AudioSegment.silent(duration=10)

    # splice together stuff
    i = 0
    while True:
        if i % 2 == 0:
            ms_pb_s = ms_pb * (4 / 3)  # slower, milliseconds per beat
            target_audio = stretched_proc
        else:
            ms_pb_s = ms_pb * (2 / 3)  # faster
            target_audio = squished_proc

        seg_start = round(ms_pb_s * i / 2)
        seg_end = round(ms_pb_s * (i + 1) / 2)

        combined_segments.append(target_audio[seg_start:seg_end])
        if seg_end > target_audio.duration_seconds * 1000:
            break
        i += 1

    combined = AudioSegment.empty()
    for sample in combined_segments:
        combined += sample

    return combined
