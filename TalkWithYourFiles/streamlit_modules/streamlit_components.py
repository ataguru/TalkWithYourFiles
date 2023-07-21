import streamlit as st
from .streamlit_helper_functions import advanced_parameters_section, create_authorization_box, get_chat_bot_info_dict, get_qa_chain_info_dict
from .streamlit_chat import integrate_chain_into_chat



def setup_page_configurations():
    ##### PAGE CONFIGURATIONS
    st.set_page_config(
                    page_title="Talk With Your Files",
                    page_icon="🧙‍♂️",
                    layout="wide", # centered or wide
                    initial_sidebar_state="expanded", #auto, expanded, collapsed
                    menu_items={
                        'Get Help': 'https://github.com/Safakan',
                        'Report a bug': "https://github.com/Safakan/TalkWithYourFiles",
                        'About': "Open source LLM GUI app allowing interactions with files!"
                        }
                    )

    # ---- HIDE STREAMLIT STYLE ----
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def setup_header_area():
    ##### HEADER
    st.title("Talk With Your Files 🪄 ")

def setup_sidebar(flow_coordinator):
    ##### SIDEBAR
    st.sidebar.markdown("# Talk With Your Files 🪄")
    st.sidebar.write("Hello! Here's an open-source tool for you. Query your files, modify the QA chain behaviour, monitor active parameters, feed the results into the chatbot if you prefer and debug the chatbot conversation. Stay tuned for the updates. Hope you love it! ❤️")

    st.sidebar.markdown('Documentation & codebase: [github.com/Safakan/TalkWithYourFiles](https://www.github.com/Safakan/TalkWithYourFiles)')
    
    st.sidebar.markdown("#### Authorization")
    ##### Authorization box for OpenAI API KEY
    create_authorization_box(flow_coordinator)
    st.sidebar.write("API keys are not stored, and their use is limited to your present browser session.")


def tab1_qa_chain_files(param_controller, flow_coordinator):
    """
    Main function to run the Streamlit interface and execute the run function from file_processor.
    This file follows the dependency inversion principle, and separates UI from backend functionalities:
    Streamlit framework is used to render the GUI and manage file uploads.
    To use other approaches or frameworks: 
    1) Make sure to set up a GUI that allows users to upload files & enter text input for their questions.
    2) Import the run method from the flow_coordinator.py
    3) Get the response by running the run(files, user_question) method with the appropriate arguments. 
    
    """
 


    ##### FILE UPLOADS
    files = st.file_uploader("Upload files", 
                            type=["pdf", "docx", "txt","csv"], 
                            accept_multiple_files=True
                            )



    

    ##### ADVANCED PARAMETERS SECTION
    with st.expander("Show Advanced Parameters?"):
        advanced_parameters_section(param_controller)




    ##### USER QUESTION INPUT
    user_question = st.text_input("Please ask question(s) about the files you've uploaded: ")
    

    ###### To run the chain & shape the behaviour
    run_button_col, integration_button_col = st.columns([4,1])
    with run_button_col:
        ##### QA CHAIN RUN BUTTON
        run_button_clicked = st.button("Run",
                                    use_container_width=True,
                                    type="primary"                                   
                                    )
    
    with integration_button_col:
        ###### QA Chain Behaviour
        transfer_to_chat_bot = st.selectbox(
                                            label="Test",
                                            label_visibility="collapsed", 
                                            options=["Standalone","Integrated into the chatbot"]
                                            )


    ##### START QA CHAIN
    if user_question and files and run_button_clicked and st.session_state.api_key_valid:       
        response = flow_coordinator.run(files, user_question)
        st.write(response)

        if transfer_to_chat_bot != "Standalone":
            integrate_chain_into_chat(user_question, response)


def tab2_active_params(param_controller):
    ## for testing purposes - to see the params in the UI as I change them.

    # tab_chat_bot_params, tab_qa_chain_params = st.tabs(["Chat Bot", "QA Chain"])
    tab_chat_bot_params, tab_qa_chain_params = st.columns(2)

    with tab_chat_bot_params:
        st.write("""
                Chat Bot   
                """
                )
        st.write(get_chat_bot_info_dict(param_controller))
    with tab_qa_chain_params:
        st.write("""
                QA Chain
                """
                )
        st.write(get_qa_chain_info_dict(param_controller))






