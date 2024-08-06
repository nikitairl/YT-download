from moviepy.editor import AudioFileClip, VideoFileClip


def merge_audio_video(audio_title, video_title):
    print(audio_title)
    print(video_title)
    audio = AudioFileClip('./downloads/tmp/' + audio_title)
    video = VideoFileClip('./downloads/tmp/' + video_title)
    video = video.set_audio(audio)
    video.write_videofile('./downloads/' + video_title)
    return
