import tkinter as tk
from tkinter import scrolledtext
from chatbot_logic import get_response

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBot Chatbot")
        self.root.configure(bg="#333333")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled',
                                                   bg="#222222", fg="white", font=("Helvetica", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        entry_frame = tk.Frame(root, bg="#333333")
        entry_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(entry_frame, font=("Helvetica", 12), bg="#444444", fg="white",
                              insertbackground="white")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.on_enter_pressed)

        send_btn = tk.Button(entry_frame, text="Send", command=self.on_enter_pressed,
                             bg="#555555", fg="white", activebackground="#777777", activeforeground="white")
        send_btn.pack(side=tk.RIGHT)

        self.display_message("SmartBot", "Hello! Type your message and press Send or Enter.")

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def on_enter_pressed(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.display_message("You", user_text)
        self.entry.delete(0, tk.END)

        if user_text.lower() in ['exit', 'quit', 'bye']:
            self.display_message("SmartBot", "Goodbye! Have a great day!")
            self.root.after(500, self.root.quit)
            return

        self.display_message("SmartBot", "Thinking...")
        self.root.update()

        try:
            answer = get_response(user_text)
        except Exception as e:
            answer = f"Sorry, an error occurred: {e}"

        # Remove "Thinking..." message before displaying answer
        self.chat_area.config(state='normal')
        self.chat_area.delete("end-3l", "end-1l")
        self.chat_area.config(state='disabled')

        self.display_message("SmartBot", answer)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")
    app = ChatbotGUI(root)
    root.mainloop()
