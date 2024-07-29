from langchain.tools import tool
from langchain_openai import ChatOpenAI
import moviepy.editor as mp
import whisper
import os

# Load the Whisper model globally
whisper_model = whisper.load_model("base")

@tool
def extract_video_transcript(video_path: str) -> str:
    """
    Process the video audio, and extract the transcript fromt the audio 

    Parameters:
    video_path (str): The name of the video to prcess

    Returns:
    str: a transcript of a video
    """
    if not video_path:
        return "Error: video_path not provided."
    try:
        # Load the video file
        video = mp.VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        
        # Extract audio from video
        video.audio.write_audiofile(audio_path)
        
        # Transcribe audio to text
        result = whisper_model.transcribe(audio_path)
        transcript = result['text']
        
        # Optionally, clean up the temporary audio file
        os.remove(audio_path)
        
        return transcript
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def summarize_transcript(text: str) -> str:
    """
    Process the video transcript, and summrize it 

    Parameters:
    text (str): the trnascript of a video

    Returns:
    str: a summary of the transcript based on the provided prompmt 
    """
    if not text:
        return "Error: text not provided."
    try:
        model = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = f"Summarize the following text:\n\n{text}"
        response = model.call(prompt)
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        return f"An unexpected error occurred: {e}"
