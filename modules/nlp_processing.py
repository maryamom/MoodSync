import openai

class NLPProcessor:
    """
    Class to process natural language data for summarization and emotion analysis.
    """

    def __init__(self, api_key="YOUR_OPENAI_API_KEY"):
        openai.api_key = api_key

    def summarize_conversation(self, conversation_text):
        """
        Summarizes the transcribed conversation into bullet points.
        """
        print("Generating bullet points...")

        prompt = (
            "Summarize the following conversation into key bullet points:\n\n"
            f"{conversation_text}\n\nBullet Points:"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        summary = response["choices"][0]["message"]["content"]
        return summary.split("\n")  # Return as a list of bullet points

    def analyze_emotion(self, conversation_text):
        """
        Analyzes the emotional tone of the conversation text.
        """
        print("Analyzing emotion...")

        prompt = (
            "Analyze the emotional tone of the following conversation and return the dominant emotion:\n\n"
            f"{conversation_text}\n\nEmotion:"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )

        emotion = response["choices"][0]["message"]["content"]
        return emotion.strip()
