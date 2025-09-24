# AWS Transcribe Streaming Demo

A Python demo project showcasing Amazon AWS Transcribe for real-time speech-to-text conversion.

## Features

- 🎤 **Real-time streaming transcription** from microphone
- 📁 **Batch transcription** from audio files
- 🔄 **Live confidence scores** and timestamps
- 🛠️ **Easy setup** with clear instructions

## Prerequisites

1. **Python 3.7+**
2. **AWS Account** with Transcribe service access
3. **Audio device** (microphone) for real-time demo

## Installation

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install PyAudio** (if you encounter issues):
   - **Windows:**
     ```bash
     pip install pipwin
     pipwin install pyaudio
     ```
   - **macOS:**
     ```bash
     brew install portaudio
     pip install pyaudio
     ```
   - **Linux:**
     ```bash
     sudo apt-get install python3-pyaudio
     ```

## AWS Setup

### 1. Configure AWS Credentials

Choose one of these methods:

**Option A: AWS CLI (Recommended)**
```bash
pip install awscli
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (e.g., `json`)

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option C: IAM Role** (if running on EC2)

### 2. Required Permissions

Your AWS user/role needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "transcribe:StartStreamTranscription",
                "transcribe:StartTranscriptionJob",
                "transcribe:GetTranscriptionJob"
            ],
            "Resource": "*"
        }
    ]
}
```

## Usage

### Run the Demo

```bash
python transcribe_demo.py
```

### Options

1. **Real-time Microphone Transcription**
   - Speaks into your microphone
   - See live transcription results
   - Press Ctrl+C to stop

2. **Batch File Transcription**
   - Transcribe pre-recorded audio files
   - Supports WAV format (16kHz recommended)
   - Get results via AWS console

## Example Output

```
🎤 AWS Transcribe Streaming Demo
========================================

Choose an option:
1. Stream from microphone (real-time)
2. Transcribe audio file (batch)
3. Exit

Enter your choice (1-3): 1

🎤 Starting streaming transcription from microphone...
🎙️  Listening... Speak now!

📝 Transcription Results:
--------------------------------------------------
[14:30:15] Hello, this is a test of the transcription system (Confidence: 0.95)
[14:30:18] It seems to be working quite well (Confidence: 0.92)
```

## Supported Audio Formats

- **Streaming:** PCM, 16kHz sample rate, mono
- **Batch:** WAV, MP3, MP4, FLAC, OGG, AMR, WebM

## Troubleshooting

### Common Issues

1. **"AWS credentials not found"**
   - Run `aws configure` or set environment variables
   - Check your AWS account has Transcribe access

2. **"No module named 'pyaudio'"**
   - Install PyAudio using the platform-specific instructions above

3. **"Permission denied" for microphone**
   - Grant microphone permissions to your terminal/Python
   - On Windows: Check Privacy settings
   - On macOS: System Preferences > Security & Privacy > Microphone

4. **"Audio device not found"**
   - Check your microphone is connected and working
   - Test with other applications first

### Performance Tips

- Use a **quiet environment** for better accuracy
- Speak **clearly and at normal pace**
- **16kHz sample rate** works best for most use cases
- **Mono audio** is sufficient and more efficient

## Cost Considerations

- **Streaming:** Pay per second of audio processed
- **Batch:** Pay per minute of audio processed
- Check [AWS Transcribe Pricing](https://aws.amazon.com/transcribe/pricing/) for current rates

## Next Steps

- Integrate with your applications
- Add custom vocabulary for domain-specific terms
- Implement speaker identification
- Add language detection
- Create web interface with Flask/Django

## License

This demo is provided as-is for educational purposes. Feel free to modify and use in your projects!
