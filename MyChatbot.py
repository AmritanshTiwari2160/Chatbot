import json
import streamlit as st
from difflib import get_close_matches
import webbrowser

class ChatBotUI:
    
    def __init__(self, knowledge_base_file="knowledge_base.json"):
        self.knowledge_base_file = knowledge_base_file
        self.knowledge_base = self.load_knowledge_base()

    # Loading The Json File
    def load_knowledge_base(self) -> dict:
        try:
            with open(self.knowledge_base_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"intents": []}

    # Saving The Response from the user Into the knowledge_base
    def save_knowledge_base(self):
        with open(self.knowledge_base_file, 'w') as file:
            json.dump(self.knowledge_base, file, indent=2)

    # Finding the best match for the question
    def find_best_match(self, user_question: str) -> str | None:
        for intent in self.knowledge_base["intents"]:
            matches = get_close_matches(user_question, intent["patterns"], n=1, cutoff=0.6)
            if matches:
                return intent["responses"]

    # Main logic for processing user input
    def process_input(self, user_input: str):
        if user_input.lower() == 'quit':
            return "Goodbye!"

        responses = self.find_best_match(user_input)

        if responses:
            return f'Andro: {responses[0]}'

        if 'teach_mode' in st.session_state and st.session_state.teach_mode:
            new_answer = st.session_state.new_answer
            if new_answer and new_answer.lower() != 'skip':
                new_intent = {
                    "tag": "new_intent",
                    "patterns": [user_input],
                    "responses": [new_answer],
                    "context_set": ""
                }
                self.knowledge_base["intents"].append(new_intent)
                self.save_knowledge_base()
                st.session_state.teach_mode = False  # End teaching mode
                st.session_state.new_answer = ""  # Clear the input field
                return 'Andro: Thank you, I learned a new response.'

            return 'Andro: I don\'t know the answer. Can you teach me?'

        # Enable teaching mode
        st.session_state.teach_mode = True
        st.session_state.new_answer = ""  # Reset the answer field
        return 'Andro: I don\'t know the answer. Can you teach me?'

    def run(self):
        st.title("ANDRO THE CHATBOT")
        
        menu = st.sidebar.radio("Menu", ["Home", "About", "Developer"])

        if menu == "Home":
            user_input = st.text_input("You:", "")
            if st.button("Send"):
                response = self.process_input(user_input)
                st.text_area("Chat", value=f"You: {user_input}\n{response}", height=300)

            if 'teach_mode' in st.session_state and st.session_state.teach_mode:
                new_answer = st.text_input("Teach Me", "Type the answer or leave blank to skip:")
                st.session_state.new_answer = new_answer
        
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
