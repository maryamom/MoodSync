import openai
import json
import pyaudio
import wave
import datetime
import os
from dotenv import load_dotenv

class AudioAgent:
    def __init__(self, openai_api_key, patient_data, target_language="en"):
        """
        Initialize the AudioAgent with OpenAI API credentials and patient data.

        Args:
            openai_api_key (str): OpenAI API key.
            patient_data (dict): Patient-specific information for contextual summaries.
            target_language (str): Language to translate the transcription into (default is 'en' for English).
        """
        self.openai_api_key = openai_api_key
        self.patient_data = patient_data
        self.target_language = target_language
        openai.api_key = self.openai_api_key

    def capture_audio(self, chunk_size=1024, rate=44100, duration=60, output_folder="./recordings", file_name="recorded_audio.wav"):
        """
        Captures real-time audio from the microphone and saves it to a file.

        Returns:
            str: Path to the saved audio file.
        """
        audio_format = pyaudio.paInt16
        channels = 1

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_path = os.path.join(output_folder, file_name)

        audio = pyaudio.PyAudio()
        stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)

        print("Recording...")
        frames = []
        for _ in range(0, int(rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames.append(data)
        print("Recording complete.")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved at: {output_path}")
        return output_path

    def transcribe_audio(self, audio_file):
        """
        Transcribes audio to text using OpenAI's Whisper API.

        Returns:
            str: Transcribed text.
        """
        try:
            print("Transcribing audio...")
            with open(audio_file, "rb") as file:
                response = openai.Audio.transcribe(model="whisper-1", file=file)
            return response.get("text", "")
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

    def translate_text(self, text):
        """
        Translates the transcribed text to the target language.

        Args:
            text (str): The text to be translated.

        Returns:
            str: Translated text.
        """
        try:
            print("Translating text...")
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Translate the following text to {self.target_language}: {text}",
                max_tokens=500
            )
            translated_text = response.choices[0].text.strip()
            return translated_text
        except Exception as e:
            print(f"Error during translation: {e}")
            return None

    def summarize_transcript(self, transcript):
        """
        Summarizes the transcribed speech using OpenAI's GPT API, incorporating patient data.

        Args:
            transcript (str): Transcribed speech text.

        Returns:
            dict: A summary of the session in structured JSON format.
        """
        patient_context = f"Patient Name: {self.patient_data.get('name', 'Unknown')}, " \
                          f"Age: {self.patient_data.get('age', 'Unknown')}, " \
                          f"History: {self.patient_data.get('history', 'No history provided')}."
        
        prompt = (
            f"Context: {patient_context}\n\n"
            f"Instructions:\n"
            f"Summarize the session with these sections:\n"
            f"- Overview: A concise description of the discussion.\n"
            f"- Key Insights: Specific observations or patterns.\n"
            f"- Emotions: Any noticeable emotional states.\n"
            f"- Goals: Actionable therapeutic goals.\n"
            f"Provide the summary in JSON format."
            f"\nTranscript:\n{transcript}\n\n"
        )

        try:
            print("Generating summary...")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant helping a therapist interpret patient speech."},
                    {"role": "user", "content": prompt}
                ]
            )
            summary_json = json.loads(response.choices[0].message['content'])
            return summary_json
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

    def save_summary_to_json(self, summary, output_folder="./summaries", file_name="session_summary.json"):
        """
        Save the session summary to a JSON file in the specified folder.
        """
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            file_path = os.path.join(output_folder, file_name)
            with open(file_path, "w") as json_file:
                json.dump(summary, json_file, indent=4)
            print(f"Summary saved to {file_path}")
        except Exception as e:
            print(f"Error saving summary to JSON: {e}")

if __name__ == "__main__":
    # Load OpenAI API Key from environment variables
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Define patient-specific data
    patient_data = {
        "name": "John Doe",
        "age": 32,
        "history": "Anxiety and mild depression."
    }

    # Initialize the AudioAgent
    audio_agent = AudioAgent(openai_api_key=openai_api_key, patient_data=patient_data, target_language="en")

    # Step 1: Capture audio
    audio_file = audio_agent.capture_audio(duration=60)

    # Step 2: Transcribe and translate the audio
    transcription_result = audio_agent.transcribe_audio(audio_file)
    print(f"Transcription: {transcription_result}")

    # Step 3: Summarize the transcript with patient-specific context
    if transcription_result:
        summary = audio_agent.summarize_transcript(transcription_result)
        if summary:
            print(f"Summary: {summary}")
            # Save the summary to a JSON file
            audio_agent.save_summary_to_json(
                summary, file_name=f"{patient_data['name']}_session_summary.json"
            )
        else:
            print("Summary generation failed.")
    else:
        print("No transcription available.")
