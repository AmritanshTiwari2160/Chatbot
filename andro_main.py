import json
import streamlit as st
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
        return "Immerse yourself in a dynamic interaction with 'ANDRO', an advanced chatbot designed to engage and evolve with your queries. ANDRO's modern and intuitive Streamlit interface ensures a seamless and sophisticated chatting experience, making every conversation effortless and enjoyable. As you interact with ANDRO, it learns from your input, continuously refining its responses and becoming a more knowledgeable assistant. Each exchange not only delivers immediate answers but also contributes to ANDRO's growth, enhancing its ability to assist you over time. Explore essential links and navigate the app's features with ease, as ANDRO provides you with valuable developer resources and insights. Whether you're seeking technical support or simply exploring new ideas, ANDRO is here to provide refined, effective assistance at every step."

    def show_about_developer(self):
        return "Developed by Amritansh Tiwari"

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
            st.write("Visit our GitHub: [https://github.com/AmritanshTiwari2160](https://github.com/AmritanshTiwari2160)")
            st.write("Visit LeetCode: [https://leetcode.com/AmritanshTiwari_108](https://leetcode.com/AmritanshTiwari_108)")
            st.write("Visit Student Portal: [https://student.gehu.ac.in/](https://student.gehu.ac.in/)")

if __name__ == '__main__':
    chat_bot_ui = ChatBotUI()
    chat_bot_ui.run()
