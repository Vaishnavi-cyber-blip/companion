import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

# Create the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Set the system prompt
def get_system_prompt(city_name):
    return {
        "role": "system",
        "content": f"You are the expert local tour guide of {city_name}. Be friendly and act as travel comapninon by guiding the user."
    }

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    cityName = data.get("cityName")

    # Initialize the chat history if not provided
    chat_history = data.get("history", [get_system_prompt(cityName)])

    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )

    # Append the assistant's response to the chat history
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })

    return jsonify({
        "response": response.choices[0].message.content,
        "history": chat_history
    })


if __name__ == '__main__':
    app.run(debug=True)
