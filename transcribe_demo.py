#!/usr/bin/env python3
"""
AWS Transcribe Streaming Demo
A simple Python demo showing how to use Amazon Transcribe for real-time speech-to-text.
"""

import boto3
import json
import time
import threading
from datetime import datetime
import pyaudio
import wave
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TranscribeStreamingDemo:
    def __init__(self, region='us-east-1'):
        """
        Initialize the Transcribe Streaming Demo
        
        Args:
            region (str): AWS region for Transcribe service
        """
        self.region = region
        self.transcribe_client = boto3.client('transcribe', region_name=region)
        self.streaming_client = boto3.client('transcribe', region_name=region)
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
    def start_streaming_transcription(self, audio_source='microphone'):
        """
        Start streaming transcription from audio source
        
        Args:
            audio_source (str): 'microphone' or path to audio file
        """
        print(f"🎤 Starting streaming transcription from {audio_source}...")
        print("Press Ctrl+C to stop")
        
        try:
            if audio_source == 'microphone':
                self._stream_from_microphone()
            else:
                self._stream_from_file(audio_source)
        except KeyboardInterrupt:
            print("\n🛑 Stopping transcription...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _stream_from_microphone(self):
        """Stream audio from microphone"""
        # Open microphone stream
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print("🎙️  Listening... Speak now!")
        
        # Start streaming
        self._start_transcription_stream(stream)
        
        stream.stop_stream()
        stream.close()
    
    def _stream_from_file(self, file_path):
        """Stream audio from file"""
        if not os.path.exists(file_path):
            print(f"❌ Audio file not found: {file_path}")
            return
            
        print(f"📁 Streaming from file: {file_path}")
        
        # Open audio file
        wf = wave.open(file_path, 'rb')
        
        # Create PyAudio stream
        stream = self.audio.open(
            format=self.audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=False,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        self._start_transcription_stream(stream, wf)
        
        stream.stop_stream()
        stream.close()
        wf.close()
    
    def _start_transcription_stream(self, stream, audio_file=None):
        """Start the actual transcription stream"""
        # Create audio stream generator
        def audio_stream():
            while True:
                if audio_file:
                    data = audio_file.readframes(self.chunk_size)
                    if not data:
                        break
                else:
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                
                yield data
        
        # Start transcription
        response = self.streaming_client.start_stream_transcription(
            LanguageCode='en-US',
            MediaEncoding='pcm',
            MediaSampleRateHertz=self.sample_rate,
            AudioStream=audio_stream()
        )
        
        # Process results
        self._process_transcription_results(response)
    
    def _process_transcription_results(self, response):
        """Process and display transcription results"""
        print("\n📝 Transcription Results:")
        print("-" * 50)
        
        for event in response['TranscriptResultStream']:
            if 'TranscriptEvent' in event:
                transcript = event['TranscriptEvent']['Transcript']
                results = transcript['Results']
                
                for result in results:
                    if not result['IsPartial']:
                        transcript_text = result['Alternatives'][0]['Transcript']
                        confidence = result['Alternatives'][0].get('Confidence', 0)
                        
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] {transcript_text} (Confidence: {confidence:.2f})")
    
    def transcribe_file(self, file_path, output_format='json'):
        """
        Transcribe an audio file using batch processing
        
        Args:
            file_path (str): Path to audio file
            output_format (str): Output format ('json' or 'text')
        """
        if not os.path.exists(file_path):
            print(f"❌ Audio file not found: {file_path}")
            return
        
        # Generate unique job name
        job_name = f"transcribe-demo-{int(time.time())}"
        
        print(f"📁 Starting batch transcription for: {file_path}")
        print(f"🔄 Job name: {job_name}")
        
        try:
            # Start transcription job
            response = self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': f'file://{os.path.abspath(file_path)}'},
                MediaFormat='wav',  # Adjust based on your file format
                LanguageCode='en-US'
            )
            
            print("⏳ Transcription job started. Waiting for completion...")
            
            # Wait for job completion
            while True:
                response = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                
                status = response['TranscriptionJob']['TranscriptionJobStatus']
                
                if status == 'COMPLETED':
                    print("✅ Transcription completed!")
                    
                    # Get transcription results
                    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    print(f"📄 Results available at: {transcript_uri}")
                    
                    # You could download and parse the results here
                    break
                    
                elif status == 'FAILED':
                    print("❌ Transcription failed!")
                    print(f"Reason: {response['TranscriptionJob'].get('FailureReason', 'Unknown')}")
                    break
                    
                else:
                    print(f"⏳ Status: {status}")
                    time.sleep(5)
                    
        except ClientError as e:
            print(f"❌ AWS Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        self.audio.terminate()

def main():
    """Main demo function"""
    print("🎤 AWS Transcribe Streaming Demo")
    print("=" * 40)
    
    # Check AWS credentials
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if not credentials:
            print("❌ AWS credentials not found!")
            print("Please configure your AWS credentials:")
            print("1. Install AWS CLI: pip install awscli")
            print("2. Configure: aws configure")
            print("3. Or set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            return
    except Exception as e:
        print(f"❌ Error checking AWS credentials: {e}")
        return
    
    # Initialize demo
    demo = TranscribeStreamingDemo()
    
    try:
        print("\nChoose an option:")
        print("1. Stream from microphone (real-time)")
        print("2. Transcribe audio file (batch)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            demo.start_streaming_transcription('microphone')
        elif choice == '2':
            file_path = input("Enter path to audio file: ").strip()
            demo.transcribe_file(file_path)
        elif choice == '3':
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice!")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        demo.cleanup()

if __name__ == "__main__":
    main()
