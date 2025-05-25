import openai
import pyaudio
import wave

class AudioTranscriber:
    def __init__(self, api_key, record_seconds=10, output_filename="output.wav"):
        """
        Initializes the AudioTranscriber with the OpenAI API key and recording settings.
        :param api_key: OpenAI API Key
        :param record_seconds: Duration to record in seconds
        :param output_filename: Filename to save the recorded audio
        """
        openai.api_key = api_key
        self.record_seconds = record_seconds
        self.output_filename = output_filename

    def record_audio(self):
        """
        Captures real-time audio from the microphone and saves it to a .wav file.
        """
        print("Recording audio...")

        # Set up audio recording
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16-bit resolution
        channels = 1  # Mono
        rate = 44100  # 44.1kHz sample rate

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open a stream
        stream = p.open(format=sample_format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

        frames = []

        # Record the audio
        for _ in range(0, int(rate / chunk * self.record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio as a .wav file
        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("Recording complete. Audio saved as:", self.output_filename)

    def transcribe_audio(self):
        """
        Transcribes the recorded audio file using OpenAI's Whisper model.
        :return: Transcribed text from the audio.
        """
        print("Transcription in progress...")

        # Use OpenAI Whisper for transcription
        with open(self.output_filename, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        
        return transcript["text"]

# Example usage
if __name__ == "__main__":
    # Replace with your actual OpenAI API key
    api_key = OPENAI_API_KEY
    
    transcriber = AudioTranscriber(api_key)
    transcriber.record_audio()
    transcript = transcriber.transcribe_audio()
    
    print("Transcription:", transcript)
