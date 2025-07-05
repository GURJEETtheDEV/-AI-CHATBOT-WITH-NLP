import os
import openai
import nltk
import string
from nltk.tokenize import TreebankWordTokenizer

# Download necessary NLTK data files (run once)
nltk.download('punkt')

# Initialize the tokenizer
tokenizer = TreebankWordTokenizer()

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Define simple obvious questions & answers
FAQ_RESPONSES = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! How can I help you?",
    "how are you": "I'm an AI chatbot, always ready to help!",
    "what is your name": "I am SmartBot, your AI assistant.",
    "bye": "Goodbye! Have a great day!",
    "thank you": "You're welcome!",
}

def check_faq(user_input):
    # Normalize input
    text = user_input.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = tokenizer.tokenize(text)

    # Check if any FAQ keyword or phrase matches input closely
    for question, answer in FAQ_RESPONSES.items():
        question_tokens = tokenizer.tokenize(question)
        if all(token in tokens for token in question_tokens):
            return answer
    return None

def ask_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def chatbot():
    print("🤖 Hybrid Chatbot (NLTK + GPT) — type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("SmartBot: Goodbye! Have a great day!")
            break

        # Try FAQ first
        faq_answer = check_faq(user_input)
        if faq_answer:
            print("SmartBot:", faq_answer)
        else:
            # Fall back to GPT
            answer = ask_gpt(user_input)
            print("SmartBot:", answer)

if __name__ == "__main__":
    chatbot()

def get_response(user_input):
    faq_answer = check_faq(user_input)
    if faq_answer:
        return faq_answer
    else:
        return ask_gpt(user_input)
