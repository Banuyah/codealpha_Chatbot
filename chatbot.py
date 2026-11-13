import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import random


# 1. Generate a response based on the user's message
def chatbot_response(user_message):

    message = user_message.lower().strip()

    # Greetings
    if message in ["hello", "hi", "hey", "hello bot", "hi bot"]:
        return random.choice([
            "Hello! How can I help you?",
            "Hi! Nice to meet you.",
            "Hey! What can I do for you?"
        ])

    elif "good morning" in message:
        return "Good morning! Have a wonderful day!"

    elif "good afternoon" in message:
        return "Good afternoon! How is your day going?"

    elif "good evening" in message:
        return "Good evening! How can I help you?"

    # Well-being
    elif "how are you" in message:
        return random.choice([
            "I'm fine, thanks! How about you?",
            "I'm doing great. Thank you for asking!",
            "I'm good! Hope you are doing well too."
        ])

    # Identity
    elif "your name" in message or "who are you" in message:
        return "I'm Python Bot, a simple rule-based chatbot."

    elif "how old are you" in message:
        return "I'm a chatbot program. I don't have a human age!"

    # Capabilities and help
    elif "what can you do" in message or "your features" in message:
        return (
            "I can respond to greetings, answer simple questions, "
            "tell jokes, show date and time, and more."
        )

    elif message in ["help", "help me"]:
        return (
            "You can ask me:\n"
            "1. Hello\n"
            "2. How are you?\n"
            "3. What is your name?\n"
            "4. What time is it?\n"
            "5. What is today's date?\n"
            "6. Tell me a joke\n"
            "7. What is Python?\n"
            "8. Bye"
        )

    # Common conversation
    elif "thank you" in message or message == "thanks":
        return random.choice([
            "You're welcome!",
            "Happy to help!",
            "No problem!"
        ])

    elif message == "sorry" or "i am sorry" in message:
        return "That's okay! No problem."

    # Date and time
    elif "time" in message:
        current_time = datetime.now().strftime("%I:%M %p")
        return "The current time is " + current_time

    elif "date" in message or "today" in message:
        current_date = datetime.now().strftime("%d-%m-%Y")
        return "Today's date is " + current_date

    # Programming and study
    elif "what is python" in message:
        return (
            "Python is a popular programming language. "
            "It is used in web development, automation, "
            "data science, and artificial intelligence."
        )

    elif "programming" in message or "coding" in message:
        return "Programming means giving instructions to a computer."

    elif "study" in message or "studying" in message:
        return (
            "Make a study timetable, understand the concepts, "
            "and practise questions every day!"
        )

    # Motivation and jokes
    elif "motivate me" in message or "motivation" in message:
        return random.choice([
            "Believe in yourself. You can do it!",
            "Every small step takes you closer to success.",
            "Don't give up. Keep learning and improving!"
        ])

    elif "joke" in message:
        return random.choice([
            "Why did the computer go to the doctor? Because it had a virus!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why was the computer cold? Because it left its Windows open!"
        ])

    # Mood
    elif message in ["good", "great", "fine", "i am fine"]:
        return "That's wonderful! What would you like to talk about?"

    elif "not good" in message or "i am sad" in message:
        return "I'm sorry to hear that. I hope things get better!"

    # Farewell
    elif message in ["bye", "goodbye", "see you", "exit", "quit"]:
        return "Goodbye! Have a great day!"

    # Unknown input
    else:
        return (
            "Sorry, I don't understand that question.\n"
            "Type 'help' to see what I can answer."
        )


# 2. Send the user's message and display the reply
def send_message(event=None):

    user_message = message_entry.get().strip()

    if user_message == "":
        return

    chat_area.config(state="normal")
    chat_area.insert(tk.END, "You: " + user_message + "\n\n")

    response = chatbot_response(user_message)
    chat_area.insert(tk.END, "Bot: " + response + "\n\n")

    chat_area.config(state="disabled")
    message_entry.delete(0, tk.END)
    chat_area.see(tk.END)

    # Disable input after a farewell message
    if user_message.lower().strip() in [
        "bye", "goodbye", "see you", "exit", "quit"
    ]:
        message_entry.config(state="disabled")
        send_button.config(state="disabled")
        status_label.config(text="Conversation ended")


# 3. Clear the conversation and start again
def clear_chat():

    chat_area.config(state="normal")
    chat_area.delete("1.0", tk.END)

    chat_area.insert(
        tk.END,
        "Bot: Hello! Welcome to Python Chatbot.\n"
        "Bot: Type 'help' to see available commands.\n\n"
    )

    chat_area.config(state="disabled")
    message_entry.config(state="normal")
    send_button.config(state="normal")
    status_label.config(text="Chat started")
    message_entry.focus()


# 4. Close the application
def exit_chatbot():

    answer = messagebox.askyesno(
        "Exit Chatbot",
        "Do you want to close the chatbot?"
    )

    if answer:
        root.destroy()


# 5. Create the main application window
root = tk.Tk()
root.title("Python Basic Chatbot")
root.geometry("700x650")
root.configure(bg="#f0f4f8")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="My Python Chatbot",
    font=("Arial", 24, "bold"),
    bg="#f0f4f8",
    fg="#1e3a8a"
)
title_label.pack(pady=15)

status_label = tk.Label(
    root,
    text="Chat started",
    font=("Arial", 10),
    bg="#f0f4f8",
    fg="green"
)
status_label.pack()

# Chat history display
chat_area = scrolledtext.ScrolledText(
    root,
    width=75,
    height=25,
    font=("Arial", 11),
    wrap=tk.WORD,
    state="disabled"
)
chat_area.pack(padx=20, pady=15)

chat_area.config(state="normal")
chat_area.insert(
    tk.END,
    "Bot: Hello! Welcome to Python Chatbot.\n"
    "Bot: How can I help you today?\n"
    "Bot: Type 'help' to see available commands.\n\n"
)
chat_area.config(state="disabled")

# User input area
input_frame = tk.Frame(root, bg="#f0f4f8")
input_frame.pack(pady=10)

message_entry = tk.Entry(
    input_frame,
    width=45,
    font=("Arial", 12)
)
message_entry.grid(row=0, column=0, padx=5)

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    bg="#2563eb",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12
)
send_button.grid(row=0, column=1, padx=5)

# Press Enter to send
message_entry.bind("<Return>", send_message)

# Clear and Exit buttons
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=10)

clear_button = tk.Button(
    button_frame,
    text="Clear Chat",
    command=clear_chat,
    width=15
)
clear_button.grid(row=0, column=0, padx=10)

exit_button = tk.Button(
    button_frame,
    text="Exit",
    command=exit_chatbot,
    width=15,
    bg="#dc2626",
    fg="white"
)
exit_button.grid(row=0, column=1, padx=10)

message_entry.focus()

# Keep the GUI running
root.mainloop()
