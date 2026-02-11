# Voice_agent (Azure OpenAI + SpeechRecognition + pyttsx3 + MongoDB + Tavily)

A real-time conversational voice assistant built using Azure OpenAI for language generation, SpeechRecognition for speech-to-text, pyttsx3 for offline text-to-speech, MongoDB for persistent conversation storage, and Tavily for real-time web search.

This project demonstrates how to build a continuous, multi-turn, memory-enabled AI voice assistant with external search capabilities.

---

## Features

- Real-time voice input using microphone  
- Multi-turn conversation memory  
- Persistent chat history stored in MongoDB  
- Azure OpenAI integration for intelligent responses  
- Tavily API integration for real-time web search  
- Offline text-to-speech using pyttsx3  
- Automatic silence detection and restart listening  
- Voice commands: `stop` or `exit` to terminate  
- Environment variable configuration using dotenv  

---

## Tech Stack

- Python  
- Azure OpenAI  
- SpeechRecognition  
- pyttsx3 (offline TTS)  
- MongoDB  
- Tavily Search API  
- python-dotenv  

---


## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Harsh-1302-ust/Voice_agent.git
cd Voice_agent
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If installing manually:

```bash
pip install openai speechrecognition pyttsx3 python-dotenv pyaudio pymongo tavily-python
```

For Windows (if PyAudio fails):

```bash
pip install pipwin
pipwin install pyaudio
```

---

## Environment Variables

Create a `.env` file in the root directory:

```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=your_api_version
AZURE_DEPLOYMENT=your_deployment_name

MONGO_URI=your_mongodb_connection_string

TAVILY_API_KEY=your_tavily_api_key
```

---

## Running the Application

```bash
python main.py
```

The assistant will begin listening through your microphone.

---

## How It Works

1. The microphone captures audio input.  
2. SpeechRecognition converts speech to text.  
3. User queries can optionally trigger Tavily web search.  
4. Conversation history is stored in MongoDB.  
5. The assistant sends context + search results to Azure OpenAI.  
6. The assistant generates a response.  
7. pyttsx3 converts the response into speech offline.  
8. If silence is detected for 5 seconds, the assistant automatically resumes listening.  

---

## Conversation Memory (MongoDB)

Chat history is stored persistently in MongoDB using documents structured like:

```
{
  "role": "user",
  "content": "What is the capital of France?",
  "timestamp": "2026-02-11T12:30:00"
}
```

This enables:

- Persistent memory across sessions  
- Context-aware responses  
- Scalable storage  

---

## Tavily Search Integration

Tavily is used for real-time web search when the assistant needs up-to-date information.

Use cases:
- Current events  
- Latest technology updates  
- Real-time data queries  

Search results are injected into the LLM context before generating the final response.

---

## Limitations

- Google Speech Recognition requires internet connectivity.  
- pyttsx3 voice quality depends on installed system voices.  
- Performance depends on internet speed and API limits.  

---

## Future Improvements

- Wake word detection  
- Streaming responses  
- Async processing  
- GUI-based interface  
- Role-based memory filtering  
- Background listening mode  
- Deployment using Docker  

---

## Author

Harsh Jaiswal
