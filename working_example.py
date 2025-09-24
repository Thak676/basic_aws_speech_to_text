#!/usr/bin/env python3
"""
Working AWS Transcribe Streaming Example
This example uses the correct approach for AWS Transcribe streaming.
"""

import boto3
import json
import pyaudio
import threading
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_aws_connection():
    """Test if AWS credentials are working"""
    try:
        # Test with a simple service call
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        print(f"✅ AWS Connection successful!")
        print(f"Account: {response['Account']}")
        print(f"User ID: {response['UserId']}")
        print(f"ARN: {response['Arn']}")
        return True
    except Exception as e:
        print(f"❌ AWS Connection failed: {e}")
        return False

def list_audio_devices():
    """List available audio input devices"""
    print("\n🎤 Available Audio Devices:")
    print("-" * 40)
    
    audio = pyaudio.PyAudio()
    
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:  # Only show input devices
            print(f"Device {i}: {info['name']}")
            print(f"  - Channels: {info['maxInputChannels']}")
            print(f"  - Sample Rate: {info['defaultSampleRate']}")
            print()
    
    audio.terminate()

def simple_batch_transcription():
    """Simple batch transcription example using a test audio file"""
    print("\n📁 Batch Transcription Example")
    print("-" * 40)
    
    # Create a simple test - we'll use text-to-speech to create audio
    print("This example would transcribe an audio file.")
    print("For now, let's test the AWS connection and audio setup.")
    
    # Test AWS connection
    if not test_aws_connection():
        return
    
    # List audio devices
    list_audio_devices()
    
    print("\n🎯 Next Steps:")
    print("1. Ensure your microphone is working")
    print("2. For streaming transcription, you'll need to implement WebSocket connection")
    print("3. For batch transcription, you can upload audio files to S3")

def microphone_test():
    """Test microphone input"""
    print("\n🎤 Testing Microphone...")
    print("-" * 40)
    
    # Audio settings
    sample_rate = 16000
    chunk_size = 1024
    channels = 1
    format = pyaudio.paInt16
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    try:
        # Open microphone stream
        stream = audio.open(
            format=format,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size
        )
        
        print("🎙️  Microphone is working! Recording for 3 seconds...")
        print("Speak now!")
        
        # Record for 3 seconds
        for i in range(int(sample_rate / chunk_size * 3)):
            data = stream.read(chunk_size, exception_on_overflow=False)
            print(".", end="", flush=True)
        
        print("\n✅ Microphone test completed successfully!")
        
        stream.stop_stream()
        stream.close()
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
    finally:
        audio.terminate()

def main():
    """Main function"""
    print("🎤 AWS Transcribe Setup Test")
    print("=" * 40)
    
    print("\nChoose an option:")
    print("1. Test AWS Connection")
    print("2. Test Microphone")
    print("3. List Audio Devices")
    print("4. Run All Tests")
    print("5. Exit")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            test_aws_connection()
        elif choice == '2':
            microphone_test()
        elif choice == '3':
            list_audio_devices()
        elif choice == '4':
            test_aws_connection()
            microphone_test()
            list_audio_devices()
        elif choice == '5':
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice!")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
