# video_processing_tool.py
import moviepy.editor as mp
import whisper

class VideoProcessingTool:
    def __init__(self, model='base'):
        self.transcriber = whisper.load_model(model)
    
    def extract_text_from_video(self, video_path):
        # Load video file
        video = mp.VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        
        # Extract audio from video
        video.audio.write_audiofile(audio_path)
        
        # Transcribe audio to text
        result = self.transcriber.transcribe(audio_path)
        transcript = result['text']
        
        return transcript
