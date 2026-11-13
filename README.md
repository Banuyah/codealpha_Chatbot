# CodeAlpha Internship - Task 4: AI Chatbot

## Project overview
A desktop AI chatbot built with Python, Tkinter, and the OpenAI API. Unlike a fixed rule-based chatbot, it sends user questions to an AI model and displays the generated answers. It also keeps the current conversation context so follow-up questions make sense.

## Features
- Ask open-ended questions on different topics.
- AI-generated answers rather than only fixed replies.
- Conversation context within the current chat.
- Tkinter desktop popup interface.
- Enter key and Send button.
- New Chat button to clear conversation context.
- Exit button.
- API requests run in a background thread so the GUI remains responsive.
- API key is entered at startup and kept in memory; it is not written into the project files.

## Files
- `ai_chatbot.py` - application source code.
- `requirements.txt` - Python package dependency.
- `.gitignore` - common files to exclude from Git.

## Requirements
- Python 3.10 or later.
- Internet connection.
- OpenAI API key with access to the selected model.
- API billing/credits configured on the OpenAI API Platform.

## Installation
Open a terminal in this project folder and run:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python ai_chatbot.py
```

A small dialog asks for your OpenAI API key. Paste your key there. The key is not saved by this application.

## Important API billing note
ChatGPT subscriptions and API Platform billing are separate. API usage may incur charges based on model and token usage. Check your API billing and usage limits before using the chatbot.

## Model setting
The starter code uses `gpt-5.5`. If your API project does not have access to this model, change the `MODEL` value near the top of `ai_chatbot.py` to a model available in your API account.

## GitHub safety
Never upload your API key to GitHub. This project does not store it in the source code. Do not paste your key into public issues, screenshots, or chat messages.

## Concepts covered
- Functions and classes
- Tkinter GUI and event handling
- Input and output
- Lists and dictionaries for conversation history
- Exception handling
- Threading for background API requests
- Calling an external API using the OpenAI Python SDK
