import subprocess
import os

def merge_audio_video(video_path, audio_path, output_path):
    """
    Merges audio and video using ffmpeg.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return

    # ffmpeg command
    # -i video: input video
    # -stream_loop -1 -i audio: loop input audio indefinitely
    # -filter_complex: 
    #   [1:a]volume=0.1[bg]: reduce volume of background music (input 1) to 10%
    #   [0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[a]: mix original audio (0) and bg music. Stop when first input ends.
    # -map 0:v: use video from first input
    # -map "[a]": use mixed audio
    # -c:v copy: copy video stream
    # -shortest: end when shortest stream ends (video)
    # -y: overwrite
    command = [
        "ffmpeg",
        "-i", video_path,
        "-stream_loop", "-1",
        "-i", audio_path,
        "-filter_complex", "[1:a]volume=0.5[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",
        "-shortest",
        "-y",
        output_path
    ]

    print(f"Running command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
        print(f"Successfully created {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running ffmpeg: {e}")

if __name__ == "__main__":
    video_file = "/Users/sathwikbadda/Assigment/Manim-Assignment/Management_Concept_Explainer.mp4"
    audio_file = "/Users/sathwikbadda/Assigment/Manim-Assignment/sigmamusicart-soft-corporate-presentation-background-music-434437.mp3"
    output_file = "/Users/sathwikbadda/Assigment/Manim-Assignment/Management_Concept_Explainer_With_Music.mp4"

    merge_audio_video(video_file, audio_file, output_file)
