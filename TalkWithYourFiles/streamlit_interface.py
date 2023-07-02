import streamlit as st
from flow_coordinator import FlowCoordinator
from parameter_controller import ParameterController


def advanced_parameters_section(param_controller):
    ## Get Parameters (default)
    # chunk size
    chunk_size_param_dict = param_controller.get_parameter('chunk_size')
    # chunk overlap
    chunk_overlap_param_dict = param_controller.get_parameter('chunk_overlap')
    # top related chunks / chunks to retrieve
    top_related_chunks_param_dict = param_controller.get_parameter('top_related_chunks')
    # model name from OpenAI
    model_name_param_dict = param_controller.get_parameter('model_name') 
    # max model tokens
    requested_max_model_tokens_param_dict = param_controller.get_parameter('requested_max_model_tokens')


    ### GUI
    ## columns to configure parameters in the GUI
    column_chunk_size, column_chunk_overlap, column_top_related_chunks, column_requested_max_model_tokens = st.columns(4)

    ## Text processing parameters
    with column_chunk_size:
        chunk_size_GUI = st.slider("Chunk Size", 
                                    min_value=chunk_size_param_dict['min'], 
                                    max_value=chunk_size_param_dict['max'], 
                                    value=chunk_size_param_dict['value']
                                    )

    with column_chunk_overlap:
        chunk_overlap_GUI = st.slider("Chunk Overlap",
                                    min_value=chunk_overlap_param_dict['min'], 
                                    max_value=chunk_overlap_param_dict['max'], 
                                    value=chunk_overlap_param_dict['value']
                                    )
        
    with column_top_related_chunks:
        top_related_chunks_GUI = st.slider("Top Chunks To Retrieve",
                                    min_value=top_related_chunks_param_dict['min'],
                                    max_value=top_related_chunks_param_dict['max'],
                                    value=top_related_chunks_param_dict['value']                                   
                                    )

    with column_requested_max_model_tokens:
        requested_max_model_tokens_GUI = st.slider("Max Tokens To Request", 
                                            min_value=requested_max_model_tokens_param_dict['min'], 
                                            max_value=requested_max_model_tokens_param_dict['max'], 
                                            value=requested_max_model_tokens_param_dict['value']
                                            )






    column_model_name, column_model_details, columns_token_limits = st.columns(3)

    model_names = [model['name'] for model in model_name_param_dict['model_list']]        
    
    with column_model_name:
        model_name_GUI = st.selectbox('Select a Model:', model_names)
        selected_model_info = next((model for model in model_name_param_dict['model_list'] if model['name'] == model_name_GUI), None)

        # Display the selected model's description
        st.write(f"Description: {selected_model_info['description']}")

         
    with column_model_details:
        # Display the selected model's max tokens
        st.write(f"Max Tokens: {selected_model_info['max_tokens']}")
        st.write("Beaware: Each model has its own maximum token limit. Make sure to leave room for the question.")
        st.write("Total tokens = Prompt tokens + Completion tokens")
        st.write("Prompt tokens = Context tokens + Question tokens")

 

    with columns_token_limits:        
        ## CONTEXT TOKENS    
        # calculate the context length
        context_tokens = chunk_size_GUI * top_related_chunks_GUI

        # calculate the percentage of the context tokens
        percentage = context_tokens / selected_model_info["max_tokens"]
        
        st.write(f"Context tokens: {context_tokens} tokens")
        st.progress(percentage)

        ## COMPLETION TOKENS
        # calculate the completion tokens
        completion_tokens = requested_max_model_tokens_GUI
        
        # calculate the percentage of the completion tokens
        completion_tokens_percentage = completion_tokens / selected_model_info["max_tokens"]

        st.write(f"Completion tokens: {completion_tokens} tokens")
        st.progress(completion_tokens_percentage)
    
        ## QUESTION TOKENS
        total_tokens_used = completion_tokens + context_tokens
        remaining_tokens = selected_model_info["max_tokens"] - total_tokens_used
        remaining_tokens_percentage = remaining_tokens / selected_model_info["max_tokens"]
        
        st.write(f"Question tokens: {remaining_tokens} tokens")
        st.progress(remaining_tokens_percentage)







    # Update the parameters in the parameter controller after the interactions with the slider.
    param_controller.set_parameter('chunk_size', chunk_size_GUI)
    param_controller.set_parameter('chunk_overlap', chunk_overlap_GUI)
    param_controller.set_parameter('top_related_chunks', top_related_chunks_GUI)
    param_controller.set_parameter('model_name', model_name_GUI)
    param_controller.set_parameter('requested_max_model_tokens', requested_max_model_tokens_GUI)
    




def main():
    """
    Main function to run the Streamlit interface and execute the run function from file_processor.
    This file follows the dependency inversion principle, and separates UI from backend functionalities:
    Streamlit framework is used to render the GUI and manage file uploads.
    To use other approaches or frameworks: 
    1) Make sure to set up a GUI that allows users to upload files & enter text input for their questions.
    2) Import the run method from the flow_coordinator.py
    3) Get the response by running the run(files, user_question) method with the appropriate arguments. 
    
    """

    ##### PAGE CONFIGURATIONS
    st.set_page_config(
                    page_title="Talk With Your Files",
                    page_icon="random",
                    layout="wide", # centered or wide
                    initial_sidebar_state="collapsed", #auto, expanded, collapsed
                    menu_items={
                        'Get Help': 'https://github.com/Safakan',
                        'Report a bug': "https://github.com/Safakan/TalkWithYourFiles-LLM-GUI",
                        'About': "# This is a header. This is an *extremely* cool app!"
                        }
                    )
    
    ##### HEADER
    st.header("Talk With Your Files")

    ##### SIDEBAR
    st.sidebar.header("Talk With Your Files")
    st.sidebar.write("Hello and welcome! I hope this helps you! <3")

    ##### FILE UPLOADS
    files = st.file_uploader("Upload files", type=["pdf", "docx", "txt","csv"], accept_multiple_files=True)



    ### TEST AREA START ###
    show_advanced = st.checkbox("Show advanced parameters?")


    ## Instantiating a ParameterController instance to be used in the flow_coordinator at the end.
    param_controller = ParameterController()
    
    ## Registering default parameters.
    param_controller.setup_default_parameters()     


    if show_advanced:
        advanced_parameters_section(param_controller)
    ### TEST AREA END ###



    ##### USER QUESTION INPUT
    user_question = st.text_input("Please ask me about your uploaded files and I shall help you: ")


    ##### QA CHAIN RUN BUTTON
    run_button_clicked = st.button("Run",
                                   use_container_width=True                                   
                                   )

    ##### START QA CHAIN
    if user_question and files and run_button_clicked:
        flow_coordinator = FlowCoordinator(param_controller)        
        response = flow_coordinator.run(files, user_question)
        st.write(response)


if __name__ == '__main__':
    main()
