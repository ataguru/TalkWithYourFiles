from dataclasses import dataclass
from typing import Literal
import streamlit as st

from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components

from pydantic.error_wrappers import ValidationError

import os

from langchain.prompts.prompt import PromptTemplate


# REFACTORING AND CONNECTING TO FLOWCOORDINATOR is on the way.
# This is a somewhat dirty module in the application, and the refactoring is the first in the to-do list.
# By itself it's fine, but it requires refactoring towards integration into the app design.


# Integration with param controller & flow coordinator:
# # # chatbot_prompt
# # # chatbot model name
# # # chatbot temperature
# # # chatbot description

def get_ai_prompt_chat_bot():
    template = """
            The following is a friendly conversation between a human and an AI.\n
            The AI is in the form of llm chatbot in an application called Talk With Your Files. \n
            AI's main purpose is to help the user find answers to their personal questions. \n
            AI is not the help center of the application. \n
            User can ask standalone questions or questions about the file they have uploaded. \n
            
            AI is talkative, fun, helpful and harmless. \n

            AI does not make any assumptions around this app. \n 
            If the AI does not know the answer to a question, it truthfully says it does not know. \n
            If user asks questions about the app and AI has no clear answers, AI redirect user to check out the documentations. \n
            AI can be creative and use its own knowledge if the questions are not specific to this application. \n
            
            REMEMBER: AI is there to help with all appropriate questions of users, not just the files. Provide higher level guidance with abstraction. \n
            
            This application's capabilities: \n
            1) Talk with AI chat bot (this one), \n 
            2) Run a question answer chain over documents to answer users questions over uploaded files. \n
            2.1) Modify the qa chain behaviour with dynamic parameters visible on GUI  \n
            2.2) Choose to use qa chain standalone or by integrating the results into the chatbot conversation. \n
            3) Monitor active parameters that're in use.

            documentation: https://github.com/Safakan/TalkWithYourFiles \n

            AI uses conversation summary memory, and does not remember the exact words used in the chat, but it remembers the essential meanings. \n
            Current conversation: {history} \n    
            Human: {input} \n
            AI Assistant:  
    """
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    return prompt






@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

def load_css():
    ## uses absolute path. needs modifying if static folder or the current folder changes.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, "..", "static", "styles.css")
    with open(css_path, "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)



def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
        # Append a welcoming message to the history.
        st.session_state.history = [Message("ai", 
                                            "Hi there! I'm your AI assistant while using the app TalkWithYourFiles! \n  To start using the app, please authorize yourself using the sidebar on the left."
                                            )
                                    ]
    if 'queued_messages' not in st.session_state:
        st.session_state.queued_messages = []        
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "conversation" not in st.session_state:
        if st.session_state.api_key_valid:
            llm = OpenAI(
                temperature=0.4,
                model_name="text-davinci-003"
            )
            st.session_state.conversation = ConversationChain(
                llm=llm,
                memory=ConversationSummaryMemory(llm=llm),
                prompt=get_ai_prompt_chat_bot(),
                verbose=True
            )

def on_click_callback():
    if st.session_state.api_key_valid:
        with get_openai_callback() as cb:
            human_prompt = st.session_state.human_prompt
            llm_response = st.session_state.conversation.run(
                human_prompt
            )
            st.session_state.history.append(
                Message("human", human_prompt)
            )
            st.session_state.history.append(
                Message("ai", llm_response)
            )
            st.session_state.token_count += cb.total_tokens



def main_chat():
    load_css()
    initialize_session_state()

      

    ########### start gui

    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")
    credit_card_placeholder = st.empty()

    with chat_placeholder:
        for chat in st.session_state.history:
            div = f"""
    <div class="chat-row 
        {'' if chat.origin == 'ai' else 'row-reverse'}">
        <div class="chat-icon" style="font-size: 32px;">
            {'🧙‍♂️' if chat.origin == 'ai' else '👀'}
        </div>
        <div class="chat-bubble
        {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
            &#8203;{chat.message}
        </div>
    </div>
            """
            st.markdown(div, unsafe_allow_html=True)
        
        for _ in range(3):
            st.markdown("")

    with prompt_placeholder:
        st.markdown("Chat:")
        cols = st.columns((6, 1))
        cols[0].text_input(
            "Chat",
            value="Hello bot",
            label_visibility="collapsed",
            key="human_prompt",
        )
        cols[1].form_submit_button(
            "Submit", 
            type="primary", 
            on_click=on_click_callback,
        )

    if st.session_state.api_key_valid:
        credit_card_placeholder.caption(f"""
        Used {st.session_state.token_count} tokens \n
        Debug Conversation Summary Memory: 
        {st.session_state.conversation.memory.buffer}
        """)

    components.html("""
    <script>
    const streamlitDoc = window.parent.document;

    const buttons = Array.from(
        streamlitDoc.querySelectorAll('.stButton > button')
    );
    const submitButton = buttons.find(
        el => el.innerText === 'Submit'
    );

    //streamlitDoc.addEventListener('keydown', function(e) {
    //    switch (e.key) {
    //        case 'Enter':
    //            submitButton.click();
    //          break;
    //   }
    });
    </script>
    """, 
        height=0,
        width=0,
    )




############# Helper Functions
def integrate_chain_into_chat(user_question, response):
    if st.session_state.api_key_valid:
        # Add the QA chain result to the queue
        st.session_state.queued_messages.append({
            'question': user_question,
            'answer': response
        })

        # Get the first queued message
        queued_message = st.session_state.queued_messages.pop(0)

        # Create a special AI message for it
        ai_message = f"Here're the result of your QA Chain usage: \n\n Your question: {queued_message['question']} \n\n Answer: {queued_message['answer']} \n\n\n\n I hope this helps you! I'm here to further discuss the topic or for any questions."

        # Save context to the conversation memory
        st.session_state.conversation.memory.save_context(
            {"input": queued_message['question']}, 
            {"output": queued_message['answer']}
        )

        # Display AI's message
        st.session_state.history.append(Message("ai", ai_message))

        # Use this to force rerun 
        st.experimental_rerun()



