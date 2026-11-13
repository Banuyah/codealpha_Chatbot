import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from openai import OpenAI
import threading

# Change this model only if your API account does not have access to it.
MODEL = "gpt-5.5"

SYSTEM_PROMPT = """
You are a helpful, friendly general-purpose chatbot.
Answer the user's questions clearly and accurately.
Use simple language when appropriate.
If you are unsure about something, say so instead of inventing facts.
"""


class AIChatbot:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.conversation = []
        self.is_waiting = False

        root.title("AI Chatbot")
        root.geometry("760x680")
        root.minsize(620, 520)
        root.configure(bg="#f0f4f8")

        title = tk.Label(
            root,
            text="AI Chatbot",
            font=("Arial", 23, "bold"),
            bg="#f0f4f8",
            fg="#1e3a8a"
        )
        title.pack(pady=(15, 4))

        subtitle = tk.Label(
            root,
            text="Ask questions and have a conversation",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#475569"
        )
        subtitle.pack(pady=(0, 10))

        self.chat_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Arial", 11),
            state="disabled",
            padx=10,
            pady=10
        )
        self.chat_area.pack(fill="both", expand=True, padx=18, pady=8)

        self.chat_area.tag_config("user", foreground="#1d4ed8")
        self.chat_area.tag_config("bot", foreground="#15803d")
        self.chat_area.tag_config("error", foreground="#dc2626")

        input_frame = tk.Frame(root, bg="#f0f4f8")
        input_frame.pack(fill="x", padx=18, pady=10)

        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12)
        )
        self.message_entry.pack(
            side="left", fill="x", expand=True, padx=(0, 8), ipady=8
        )
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        self.send_button.pack(side="right")

        bottom = tk.Frame(root, bg="#f0f4f8")
        bottom.pack(pady=(0, 12))

        tk.Button(
            bottom,
            text="New Chat",
            command=self.new_chat,
            width=14
        ).pack(side="left", padx=6)

        tk.Button(
            bottom,
            text="Exit",
            command=self.close_app,
            width=14,
            bg="#dc2626",
            fg="white"
        ).pack(side="left", padx=6)

        self.status = tk.Label(
            root,
            text="Ready",
            bg="#f0f4f8",
            fg="#475569",
            font=("Arial", 9)
        )
        self.status.pack(pady=(0, 8))

        self.add_message(
            "AI",
            "Hello! I'm your AI chatbot. Ask me anything to get started.",
            "bot"
        )
        self.message_entry.focus()

    def add_message(self, speaker, message, tag):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, f"{speaker}: ", tag)
        self.chat_area.insert(tk.END, message + "\n\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        if self.is_waiting:
            return

        user_text = self.message_entry.get().strip()
        if not user_text:
            return

        self.message_entry.delete(0, tk.END)
        self.add_message("You", user_text, "user")

        self.conversation.append({
            "role": "user",
            "content": user_text
        })

        self.is_waiting = True
        self.send_button.config(state="disabled")
        self.message_entry.config(state="disabled")
        self.status.config(text="AI is thinking...")

        # Run the API request in a background thread so the window stays responsive.
        thread = threading.Thread(
            target=self.get_ai_reply,
            daemon=True
        )
        thread.start()

    def get_ai_reply(self):
        try:
            response = self.client.responses.create(
                model=MODEL,
                instructions=SYSTEM_PROMPT,
                input=self.conversation
            )
            answer = response.output_text.strip()

            if not answer:
                answer = "I couldn't produce a text response. Please try again."

            self.conversation.append({
                "role": "assistant",
                "content": answer
            })

            self.root.after(0, self.finish_response, answer, None)

        except Exception as error:
            # Remove the unanswered user turn so the user can retry cleanly.
            if self.conversation and self.conversation[-1]["role"] == "user":
                self.conversation.pop()

            self.root.after(0, self.finish_response, None, str(error))

    def finish_response(self, answer, error):
        if error:
            self.add_message(
                "Error",
                "The request could not be completed.\n"
                "Check your internet connection, API key, API billing, and model access.\n\n"
                + error,
                "error"
            )
            self.status.config(text="Request failed")
        else:
            self.add_message("AI", answer, "bot")
            self.status.config(text="Ready")

        self.is_waiting = False
        self.send_button.config(state="normal")
        self.message_entry.config(state="normal")
        self.message_entry.focus()

    def new_chat(self):
        if self.is_waiting:
            messagebox.showinfo(
                "Please wait",
                "Wait for the current answer before starting a new chat."
            )
            return

        self.conversation.clear()
        self.chat_area.config(state="normal")
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state="disabled")
        self.add_message(
            "AI",
            "New conversation started. What would you like to ask?",
            "bot"
        )
        self.status.config(text="New chat")

    def close_app(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    root.withdraw()

    api_key = simpledialog.askstring(
        "OpenAI API Key",
        "Enter your OpenAI API key.\n"
        "It is used only while this application is open and is not saved.",
        show="*",
        parent=root
    )

    if not api_key or not api_key.strip():
        messagebox.showwarning(
            "API key required",
            "An OpenAI API key is required to use this AI chatbot.",
            parent=root
        )
        root.destroy()
        return

    try:
        client = OpenAI(api_key=api_key.strip())
    except Exception as error:
        messagebox.showerror(
            "Setup error",
            f"Could not initialize the OpenAI client:\n{error}",
            parent=root
        )
        root.destroy()
        return

    root.deiconify()
    AIChatbot(root, client)
    root.mainloop()


if __name__ == "__main__":
    main()
