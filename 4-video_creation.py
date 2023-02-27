from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.AudioClip import AudioFileClip

def make_video(questions_and_responses):
    video_clips = []
    for question, response in questions_and_responses.items():
        question_image = VideoFileClip(f"{question.replace(' ', '_')}.png")
        response_image = VideoFileClip(f"{response.replace(' ', '_')}.png")
        question_audio = AudioFileClip(f"{question.replace(' ', '_')}.mp3")
        response_audio = AudioFileClip(f"{response.replace(' ', '_')}.mp3")
        video = CompositeVideoClip([question_image, response_image],
                                   size=(1280, 720),
                                   bg_color=(255, 255, 255))
        video = video.set_audio(question_audio.set_duration(5).audio_fadeout(1))
        video = video.set_audio(response_audio.set_start(5).audio_fadein(1))
        video_clips.append(video)

    final_video = concatenate_videoclips(video_clips)
    final_video.write_videofile("final_video.mp4", fps=24)
