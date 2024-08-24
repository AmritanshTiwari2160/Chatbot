import json
import streamlit as st
from PIL import Image
from difflib import get_close_matches
import webbrowser

class ChatBotUI:
    
    def __init__(self, knowledge_base_file="knowledge_base.json"):
        self.knowledge_base_file = knowledge_base_file
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self) -> dict:
        try:
            with open(self.knowledge_base_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"intents": []}

    def save_knowledge_base(self):
        with open(self.knowledge_base_file, 'w') as file:
            json.dump(self.knowledge_base, file, indent=2)

    def find_best_match(self, user_question: str) -> str | None:
        questions = [pattern for intent in self.knowledge_base["intents"] for pattern in intent["patterns"]]
        matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_answer_for_question(self, question: str) -> str | None:
        for intent in self.knowledge_base["intents"]:
            if question in intent["patterns"]:
                return intent["responses"][0]

    def open_website(self, url: str):
        webbrowser.open(url)

    def show_about_app(self):
        gif_path = "Colour.gif" 
        st.image(gif_path, caption="Welcome to ANDRO: The Chatbot!",width=410)
        st.write("""
#### 🚀Immerse yourself in a dynamic interaction with 'ANDRO':
  - An advanced chatbot designed to engage and evolve with your queries. 🌟

#### 🚀Modern and Intuitive Interface:
  - Streamlit interface ensures a seamless and sophisticated chatting experience.
  - Makes every conversation effortless and enjoyable.

#### 🚀Continuous Learning and Improvement:
  - ANDRO learns from your input, continuously refining its responses.
  - Becomes a more knowledgeable assistant over time. ✨

#### 🚀Growth and Enhancement:
  - Each exchange delivers immediate answers and contributes to ANDRO’s growth.
  - Enhances its ability to assist you over time. 🌱🔍

#### 🚀Explore and Navigate Easily:
  - Provides essential links and valuable developer resources and insights. 📚

#### 🚀Effective Assistance:
  - Whether seeking technical support or exploring new ideas, ANDRO offers refined and effective assistance at every step. 💡
""")
    def show_about_developer(self):
        return "*Developed by Amritansh Tiwari*"

    def process_input(self, user_input: str) -> str:
        if user_input.lower() == 'quit':
            return "Goodbye!"

        best_match = self.find_best_match(user_input)

        if best_match:
            answer = self.get_answer_for_question(best_match)
            return f'Andro: {answer}'
        else:
            return 'Andro: I don\'t know the answer. Can you teach me?'

    def add_new_response(self, user_input: str, new_answer: str):
        self.knowledge_base["intents"].append({
            "tag": "new",
            "patterns": [user_input],
            "responses": [new_answer],
            "context_set": ""
        })
        self.save_knowledge_base()

    def run(self):
        st.title("ANDRO THE CHATBOT")

        menu = st.sidebar.radio("Menu", ["Home", "About", "Developer", "Teach"])

        if menu == "Home":
            user_input = st.text_input("You:", "")
            if st.button("Send"):
                response = self.process_input(user_input)
                st.text_area("Chat", value=f"You: {user_input}\n{response}", height=300)

        elif menu == "Teach":
            user_input = st.text_input("Enter the new question:", "")
            new_answer = st.text_input("Enter the response:", "")
            if st.button("Submit"):
                if user_input and new_answer:
                    self.add_new_response(user_input, new_answer)
                    st.success("Thank you, I learned a new response.")
                else:
                    st.error("Please provide both a question and a response.")

        elif menu == "About":
            st.write(self.show_about_app())

        elif menu == "Developer":
            st.write(self.show_about_developer())
            st.write("#### GitHub: [https://github.com/AmritanshTiwari2160](https://github.com/AmritanshTiwari2160)")
            st.write("#### LeetCode: [https://leetcode.com/AmritanshTiwari_108](https://leetcode.com/AmritanshTiwari_108)")
            st.write("#### Student Portal: [https://student.gehu.ac.in/](https://student.gehu.ac.in/)")

if __name__ == '__main__':
    chat_bot_ui = ChatBotUI()
    chat_bot_ui.run()
