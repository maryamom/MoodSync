# main.py
# Entry point for the psychology AI tool.

from modules.speech_to_text import SpeechToText
from modules.nlp_processing import NLPProcessor
from modules.mood_music import MoodMusic
from modules.image_generation import ImageGenerator
from modules.ui import UI
from modules.data_manager import DataManager
from audio_transcriber import AudioTranscriber  # Importing the new class for audio transcription


def main():
    """Main function to run the psychology AI tool."""
    print("Initializing Psychology AI Tool...")

    # Initialize components
    speech_to_text = SpeechToText()
    nlp_processor = NLPProcessor()
    mood_music = MoodMusic()
    image_generator = ImageGenerator()
    data_manager = DataManager()
    ui = UI()

    # Initialize the AudioTranscriber class
    api_key = "YOUR_OPENAI_API_KEY"  # Make sure to replace with your actual API key
    audio_transcriber = AudioTranscriber(api_key)

    # Step 1: Real-time Speech-to-Text using the AudioTranscriber class
    print("Starting real-time transcription...")
    audio_transcriber.record_audio()  # Recording the audio
    live_transcription = audio_transcriber.transcribe_audio()  # Transcribing the recorded audio

    # Step 2: NLP Processing
    print("Processing transcription for bullet points and emotion analysis...")
    bullet_points = nlp_processor.summarize_conversation(live_transcription)
    detected_emotion = nlp_processor.analyze_emotion(live_transcription)

    # Step 3: Music Recommendation
    print("Recommending music based on detected emotion...")
    mood_music.recommend_and_play_music(detected_emotion)

    # Step 4: Image Generation
    print("Generating therapeutic image...")
    therapeutic_image = image_generator.generate_image(live_transcription, detected_emotion)

    # Step 5: Save Session Data
    print("Saving session data...")
    data_manager.save_session_data(live_transcription, bullet_points, detected_emotion, therapeutic_image)

    # Step 6: Start User Interface
    print("Launching User Interface...")
    ui.start(live_transcription, bullet_points, detected_emotion, therapeutic_image)


if __name__ == "__main__":
    main()
