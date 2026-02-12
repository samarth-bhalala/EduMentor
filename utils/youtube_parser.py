"""
YouTube video transcript extraction utilities
"""
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None
import re
from typing import Optional

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL
    
    Args:
        url: YouTube URL (various formats supported)
        
    Returns:
        Video ID or None if not found
    """
    # Support multiple URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_transcript(video_url: str) -> str:
    """
    Get transcript from YouTube video
    
    Args:
        video_url: YouTube video URL
        
    Returns:
        Full transcript text
    """
    if YouTubeTranscriptApi is None:
        raise Exception("youtube-transcript-api is not installed. Run: pip install youtube-transcript-api")
    
    try:
        video_id = extract_video_id(video_url)
        
        if not video_id:
            raise ValueError("Invalid YouTube URL. Could not extract video ID.")
        
        # Get transcript using the correct API
        api = YouTubeTranscriptApi()
        fetched_transcript = api.fetch(video_id)
        
        # Combine all text segments from snippets
        full_transcript = " ".join([snippet.text for snippet in fetched_transcript.snippets])
        
        return full_transcript
    
    except AttributeError as e:
        # Fallback: try alternative import method
        try:
            from youtube_transcript_api import YouTubeTranscriptApi as YTAPI
            video_id = extract_video_id(video_url)
            transcript_list = YTAPI.get_transcript(video_id)
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            return full_transcript
        except Exception as inner_e:
            raise Exception(f"Error fetching transcript: {str(e)}. Please ensure youtube-transcript-api is properly installed.")
    
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")

def chunk_transcript(transcript: str, max_length: int = 3000) -> list[str]:
    """
    Chunk long transcript into smaller pieces for processing
    
    Args:
        transcript: Full transcript text
        max_length: Maximum characters per chunk
        
    Returns:
        List of transcript chunks
    """
    words = transcript.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > max_length and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
