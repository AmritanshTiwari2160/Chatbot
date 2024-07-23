import json
from difflib import get_close_matches

import tkinter as tk
from tkinter import scrolledtext, simpledialog, Menu
import webbrowser

class ChatBotUI:
    
    def __init__(self, knowledge_base_file="knowledge_base.json"):
        self.window = tk.Tk()
        self.window.title("ANDRO THE CHATBOT")
        self.window.geometry("1920x1080")
        self.window.configure(bg="black")

        # Title Label
        title_label = tk.Label(self.window, text="ANDRO THE CHATBOT", font=("Helvetica", 18, "bold"), fg="red", bg="yellow")
        title_label.pack(side=tk.TOP, fill=tk.BOTH)

        # Menu Bar
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        # Developer Menu
        developer_menu = Menu(menu_bar, tearoff=0)
        developer_menu.add_command(label="Github", command=lambda: self.open_website("https://github.com/Risingamer"))
        developer_menu.add_command(label="LeetCode", command=lambda: self.open_website("https://leetcode.com/Shailesh_Singh_Bisht/"))
        developer_menu.add_command(label="Student Portal", command=lambda: self.open_website("https://student.gehu.ac.in/"))
        menu_bar.add_cascade(label="Developer", menu=developer_menu)

        # About Menu
        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About The App", command=self.show_about_app)
        about_menu.add_command(label="About The Developer", command=self.show_about_developer)
        menu_bar.add_cascade(label="About", menu=about_menu)

        # Scrolled Text Area
        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=46, height=34, bg="black", fg="white", font=("Helvetica", 12))
        self.text_area.pack(padx=10, pady=10, expand=False, fill=tk.BOTH)

        # Entry Field
        self.input_entry = tk.Entry(self.window, width=60, font=("Helvetica", 12))
        self.input_entry.pack(side=tk.TOP, pady=10, padx=10)

        # Send Button
        self.send_button = tk.Button(self.window, text="Send", command=self.process_input, font=("Helvetica", 12))
        self.send_button.pack(pady=10, side=tk.BOTTOM)


        self.text_area.tag_configure("user_tag", justify='left', foreground='green') 
        self.text_area.tag_configure("bot_tag", justify='right', foreground='white')  

        self.knowledge_base_file = knowledge_base_file
        self.knowledge_base = self.load_knowledge_base()



    #Loading The Json File
    def load_knowledge_base(self) -> dict:
        try:
            with open(self.knowledge_base_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"questions": []}


    #Saving The Response from the user Into the knowledge_base
    def save_knowledge_base(self):
        with open(self.knowledge_base_file, 'w') as file:
            json.dump(self.knowledge_base, file, indent=2)


    #Finding the best match for the question
    def find_best_match(self, user_question: str) -> str | None:
        questions = [q["question"] for q in self.knowledge_base["questions"]]
        matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None


    #Getting the answer from the knowledge_base
    def get_answer_for_question(self, question: str) -> str | None:
        for q in self.knowledge_base["questions"]:
            if q["question"] == question:
                return q["answer"]

            
    #Opening the websites
    def open_website(self, url: str):
        self.text_area.insert(tk.END, f"Opening Website: {url}\n")
        webbrowser.open(url)


    #Show About the App and The Developer
    def show_about_app(self):
        about_app_text = "This is a simple chatbot application."
        self.text_area.insert(tk.END, f"About The App: {about_app_text}\n")

    def show_about_developer(self):
        about_developer_text = "Developed by [Shailesh Singh Bisht]"
        self.text_area.insert(tk.END, f"About The Developer: {about_developer_text}\n")


    #Input Process from the user
    def process_input(self):
        user_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if user_input.lower() == 'quit':
            self.window.destroy()
            return

        self.text_area.insert(tk.END, f'You: {user_input}\n', 'user_tag')
        best_match = self.find_best_match(user_input)

        if best_match:
            answer = self.get_answer_for_question(best_match)
            response = f'Andro: {answer}\n'
            self.text_area.insert(tk.END, response, 'bot_tag')

        else:
            response = 'Andro: I don\'t know the answer. Can you teach me?\n'
            self.text_area.insert(tk.END, response, 'bot_tag')
            new_answer = simpledialog.askstring("Teach Me", "Type the answer or click OK to skip:")

            if new_answer is not None and new_answer.lower() != 'skip':
                self.knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                self.save_knowledge_base()
                response = 'Andro: Thank you, I learned a new response.\n'
                self.text_area.insert(tk.END, response, 'bot_tag')


    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    chat_bot_ui = ChatBotUI()  #Object of the ChatBotUI class 
    chat_bot_ui.run()  #Calling the main of the ChatBotUI Class
