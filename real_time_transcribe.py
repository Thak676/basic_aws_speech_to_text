#!/usr/bin/env python3
"""
Real-time AWS Transcribe Speech-to-Text
This example actually performs real-time speech-to-text transcription.
"""

import asyncio
import pyaudio
import threading
import time
from datetime import datetime
from dotenv import load_dotenv
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

# Load environment variables from .env file
load_dotenv()

class MyEventHandler(TranscriptResultStreamHandler):
    """Handle transcription results"""
    
    def __init__(self, output_stream):
        super().__init__(output_stream)
        self.transcript_text = ""
        
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        """Process transcription events"""
        results = transcript_event.transcript.results
        
        for result in results:
            if not result.is_partial:  # Only show final results
                for alt in result.alternatives:
                    transcript = alt.transcript
                    confidence = alt.confidence if hasattr(alt, 'confidence') else 0.0
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] {transcript} (Confidence: {confidence:.2f})")
                    
                    # Store the transcript
                    self.transcript_text += transcript + " "

class RealTimeTranscriber:
    """Real-time speech-to-text transcriber"""
    
    def __init__(self, region='us-east-1'):
        self.region = region
        self.client = TranscribeStreamingClient(region=region)
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
    async def start_transcription(self):
        """Start real-time transcription"""
        print("🎤 Starting real-time speech-to-text transcription...")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        
        try:
            # Start transcription stream
            stream = await self.client.start_stream_transcription(
                language_code="en-US",
                media_sample_rate_hz=self.sample_rate,
                media_encoding="pcm",
            )
            
            # Create event handler
            handler = MyEventHandler(stream.output_stream)
            
            # Start audio streaming and event handling concurrently
            await asyncio.gather(
                self._stream_audio(stream.input_stream),
                handler.handle_events()
            )
            
        except Exception as e:
            print(f"❌ Error during transcription: {e}")
        finally:
            self.cleanup()
    
    async def _stream_audio(self, input_stream):
        """Stream audio from microphone to AWS Transcribe"""
        # Open microphone stream
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print("🎙️  Listening... Speak now!")
        
        try:
            while True:
                # Read audio data
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                
                # Send audio chunk to AWS Transcribe
                await input_stream.send_audio_event(audio_chunk=data)
                
                # Small delay to prevent overwhelming the service
                await asyncio.sleep(0.01)
                
        except Exception as e:
            print(f"❌ Audio streaming error: {e}")
        finally:
            # End the stream
            await input_stream.end_stream()
            stream.stop_stream()
            stream.close()
    
    def cleanup(self):
        """Clean up resources"""
        self.audio.terminate()

async def main():
    """Main function"""
    print("🎤 Real-time AWS Transcribe Speech-to-Text")
    print("=" * 50)
    
    # Test AWS connection first
    try:
        from botocore.session import Session
        session = Session()
        credentials = session.get_credentials()
        if not credentials:
            print("❌ AWS credentials not found!")
            print("Please check your .env file with AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            return
        else:
            print("✅ AWS credentials found")
    except Exception as e:
        print(f"❌ Error checking AWS credentials: {e}")
        return
    
    # Create transcriber and start
    transcriber = RealTimeTranscriber()
    
    try:
        await transcriber.start_transcription()
    except KeyboardInterrupt:
        print("\n🛑 Stopping transcription...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
