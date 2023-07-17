from dataclasses import dataclass
from typing import Literal
import streamlit as st

from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components


from pydantic.error_wrappers import ValidationError


# for prompt
from langchain.prompts.prompt import PromptTemplate

def get_ai_prompt_chat_bot():
    template = """
    The following is a friendly conversation between a human and an AI.\n
    The AI is in the form of chatbot in an application called Talk With Your Files. \n
    AI is talkative & fun, already introduced itself with a default message. And does not greet anymore. \n
    AI is aware of this app's capabilities, and will not make assumptions around this app. \n 
    If the AI does not know the answer to a question, it truthfully says it does not know. \n
    And suggest people to check out the sources like github etc.
    
    The apps's capabilities:
    Talk with AI chat bot, run a question answer chain over documents to question user's documents with dynamic parameters integrated into the GUI.

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
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
        # Append a welcoming message to the history.
        st.session_state.history = [Message("ai", "Hi there! I'm here to guide & help you while using TalkWithYourFiles!")]
    if 'queued_messages' not in st.session_state:
        st.session_state.queued_messages = []        
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "conversation" not in st.session_state:
        if st.session_state.api_key_valid:
            llm = OpenAI(
                temperature=0,
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
    # try:
    initialize_session_state()
    # except ValidationError as ve:
    #     st.write("Invalid or missing API key.")
    #     return "Invalid or missing API key. Please ensure you have entered a valid OpenAI API key."
      

    ########### start gui

    st.title("Hello Custom CSS Chatbot 🤖")

    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")
    credit_card_placeholder = st.empty()

    with chat_placeholder:
        for chat in st.session_state.history:
            div = f"""
    <div class="chat-row 
        {'' if chat.origin == 'ai' else 'row-reverse'}">
        <img class="chat-icon" src="app/static/{
            'ai_icon.png' if chat.origin == 'ai' 
                        else 'user_icon.png'}"
            width=32 height=32>
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
        st.markdown("**Chat**")
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
        Debug Langchain conversation: 
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

    streamlitDoc.addEventListener('keydown', function(e) {
        switch (e.key) {
            case 'Enter':
                submitButton.click();
                break;
        }
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
        ai_message = f"Here're the result of your QA Chain usage, let's look at it together:\n\nquestion: {queued_message['question']}\nanswer: {queued_message['answer']}"

        # Save context to the conversation memory
        st.session_state.conversation.memory.save_context(
            {"input": queued_message['question']}, 
            {"output": queued_message['answer']}
        )

        # Display AI's message
        st.session_state.history.append(Message("ai", ai_message))

        # Use this to force rerun 
        st.experimental_rerun()



# #### make sure the enter only triggers when focused on the input box
# def chat_input_on_change(chat_input):
#     if chat_input:
#         st.session_state.chat_focused = True
#     else:
#         st.session_state.chat_focused = False