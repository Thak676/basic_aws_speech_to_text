#!/usr/bin/env python3
"""
Simple AWS Transcribe Example
A minimal example showing basic streaming transcription.
"""

import boto3
import json
import pyaudio
import threading
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def simple_transcribe():
    """Simple streaming transcription example"""
    
    # Initialize AWS Transcribe Streaming client
    client = boto3.client('transcribe', region_name='us-east-1')
    
    # Audio settings
    sample_rate = 16000
    chunk_size = 1024
    channels = 1
    format = pyaudio.paInt16
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    # Open microphone stream
    stream = audio.open(
        format=format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size
    )
    
    print("🎤 Listening... Speak now! (Press Ctrl+C to stop)")
    
    try:
        # Audio stream generator
        def audio_stream():
            while True:
                data = stream.read(chunk_size, exception_on_overflow=False)
                yield data
        
        # Start transcription
        response = client.start_stream_transcription(
            LanguageCode='en-US',
            MediaEncoding='pcm',
            MediaSampleRateHertz=sample_rate,
            AudioStream=audio_stream()
        )
        
        # Process results
        for event in response['TranscriptResultStream']:
            if 'TranscriptEvent' in event:
                transcript = event['TranscriptEvent']['Transcript']
                results = transcript['Results']
                
                for result in results:
                    if not result['IsPartial']:
                        text = result['Alternatives'][0]['Transcript']
                        confidence = result['Alternatives'][0].get('Confidence', 0)
                        print(f"📝 {text} (Confidence: {confidence:.2f})")
                        
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    simple_transcribe()
