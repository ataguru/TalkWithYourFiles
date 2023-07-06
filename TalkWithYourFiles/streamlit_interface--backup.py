import streamlit as st
from flow_coordinator import FlowCoordinator
from parameter_controller import ParameterController

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

    ## Instantiating a ParameterController instance to be used in the flow_coordinator at the end.
    param_controller = ParameterController()
    
    ## Registering default parameters.
    param_controller.setup_default_parameters()  



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
    files = st.file_uploader("Upload files", 
                             type=["pdf", "docx", "txt","csv"], 
                             accept_multiple_files=True
                             )



    ##### ADVANCED PARAMETERS SECTION
    with st.expander("Show Advanced Parameters?"):
        advanced_parameters_section(param_controller)



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








def advanced_parameters_section2(param_controller):
    ## Store to default parameters to use later on
    param_dicts = store_default_parameters(param_controller)


    #### TOP ROW TO SHOW AND ALLOW DYNAMIC PARAMETERS

    ## 4 columns to configure text processing parameters in the GUI
    column_chunk_size, column_chunk_overlap, column_top_related_chunks, column_requested_max_model_tokens = st.columns(4)

    with column_chunk_size:
        param_dicts["chunk_size"]['value'] = create_slider("Chunk Size", param_dicts["chunk_size"])

    with column_chunk_overlap:
        param_dicts["chunk_overlap"]['value'] = create_slider("Chunk Overlap", param_dicts["chunk_overlap"])

    with column_top_related_chunks:
        param_dicts["top_related_chunks"]['value'] = create_slider("Top Chunks To Retrieve", param_dicts["top_related_chunks"])

    with column_requested_max_model_tokens:
        param_dicts["requested_max_model_tokens"]['value'] = create_slider("Max Tokens To Request", param_dicts["requested_max_model_tokens"])



    ##### SECOND ROW TO CONFIGURE MODEL DETAILS AND SHOW TOKEN USAGE
    column_model_name, column_model_details, columns_token_limits = st.columns(3)

    
    ## Setting up the select box with the model names.
    with column_model_name:
        ## List of model names to use in the selectbox.
        model_names = [model['name'] for model in param_dicts["model_name"]['model_list']]       
        model_name_GUI = st.selectbox('Select a Model:', model_names)
        
        ## Store selected model
        selected_model_info = next((model for model in param_dicts["model_name"]['model_list'] if model['name'] == model_name_GUI), None)

        # Display the selected model's description
        st.write(f"Description: {selected_model_info['description']}")

         
    with column_model_details:
        # Display the selected model's max tokens
        st.write(f"Max Tokens: {selected_model_info['max_tokens']}")
        st.write("Beaware: Each model has its own maximum token limit. Make sure to leave room for the question.")
        st.write("Total tokens = Prompt tokens + Completion tokens")
        st.write("Prompt tokens = Context tokens + Question tokens")

 
    ## PROGRESS BARS TO SHOW THE TOKEN USAGE WITH CURRENT FILTERS
    with columns_token_limits:        
        ## CONTEXT TOKENS    
        # calculate the context length
        context_tokens = param_dicts["chunk_size"]['value'] * param_dicts["top_related_chunks"]['value']

        # calculate the percentage of the context tokens
        percentage = context_tokens / selected_model_info["max_tokens"]
        
        st.write(f"Context tokens: {context_tokens} tokens")
        try:
            st.progress(percentage)
        except:
            st.progress(100)
        
        ## COMPLETION TOKENS
        # calculate the completion tokens
        completion_tokens = param_dicts["requested_max_model_tokens"]['value']
        
        # calculate the percentage of the completion tokens
        completion_tokens_percentage = completion_tokens / selected_model_info["max_tokens"]

        st.write(f"Completion tokens: {completion_tokens} tokens")
        try:
            st.progress(completion_tokens_percentage)
        except:
            st.progress(100)

        ## QUESTION TOKENS
        total_tokens_used = completion_tokens + context_tokens
        remaining_tokens = selected_model_info["max_tokens"] - total_tokens_used
        remaining_tokens_percentage = remaining_tokens / selected_model_info["max_tokens"]
        
        st.write(f"Question tokens: {remaining_tokens} tokens")
        try:
            st.progress(remaining_tokens_percentage)
        except:
            st.progress(0, ":red[Limit exceeded!]")


    # Update the parameters in the parameter controller after the interactions with the slider.
    update_parameters(param_controller, param_dicts)



def store_default_parameters(param_controller):
    # List of parameter names that'll be integrated into the GUI.
    parameter_names = ['chunk_size', 
                       'chunk_overlap', 
                       'top_related_chunks', 
                       'model_name', 
                       'requested_max_model_tokens'
                       ]

    # Use a dictionary comprehension to get the parameter dictionaries
    param_dicts = {name: param_controller.get_parameter(name) for name in parameter_names}

    return param_dicts

def update_parameters(param_controller, param_dicts):
    for name in param_dicts:
        param_controller.set_parameter(name, param_dicts[name]['value'])

def create_slider(label, param_dict):
    return st.slider(label, 
                        min_value=param_dict['min'], 
                        max_value=param_dict['max'], 
                        value=param_dict['value']
                        )



#### TEST AREA START

# I need functions to decrease repetition in getting parameters, creating sliders, and some other areas where possible.
## I think continue with the second row. finish all. then come back with more general look, documentation etc.
### also seems like model names are not getting updated anymore. might be a conflict with param_dicts




def advanced_parameters_section(param_controller):
    ## Initialize empty param_dicts store & return values from create_slider_with_param_controller function
    param_dicts = {}


    #### TOP ROW TO SHOW AND ALLOW DYNAMIC PARAMETERS

    ## 4 columns to configure text processing parameters in the GUI
    column_chunk_size, column_chunk_overlap, column_top_related_chunks, column_requested_max_model_tokens = st.columns(4)

    with column_chunk_size:
        param_dicts["chunk_size"]['value'] = create_slider_with_param_controller(param_controller, "chunk_size")

    with column_chunk_overlap:
        param_dicts["chunk_overlap"]['value'] = create_slider_with_param_controller(param_controller, "chunk_overlap")

    with column_top_related_chunks:
        param_dicts["top_related_chunks"]['value'] = create_slider_with_param_controller(param_controller, "top_related_chunks")

    with column_requested_max_model_tokens:
        param_dicts["requested_max_model_tokens"]['value'] = create_slider_with_param_controller(param_controller, "requested_max_model_tokens")



    ##### SECOND ROW TO CONFIGURE MODEL DETAILS AND SHOW TOKEN USAGE
    column_model_name, column_model_details, columns_token_limits = st.columns(3)

    
    ## Setting up the select box with the model names.
    with column_model_name:
        ## List of model names to use in the selectbox.
        model_names = [model['name'] for model in param_dicts["model_name"]['model_list']]       
        model_name_GUI = st.selectbox('Select a Model:', model_names)
        
        ## Store selected model
        selected_model_info = next((model for model in param_dicts["model_name"]['model_list'] if model['name'] == model_name_GUI), None)

        # Display the selected model's description
        st.write(f"Description: {selected_model_info['description']}")

         
    with column_model_details:
        # Display the selected model's max tokens
        st.write(f"Max Tokens: {selected_model_info['max_tokens']}")
        st.write("Beaware: Each model has its own maximum token limit. Make sure to leave room for the question.")
        st.write("Total tokens = Prompt tokens + Completion tokens")
        st.write("Prompt tokens = Context tokens + Question tokens")

 
    ## PROGRESS BARS TO SHOW THE TOKEN USAGE WITH CURRENT FILTERS
    with columns_token_limits:        
        ## CONTEXT TOKENS    
        # calculate the context length
        context_tokens = param_dicts["chunk_size"]['value'] * param_dicts["top_related_chunks"]['value']

        # calculate the percentage of the context tokens
        percentage = context_tokens / selected_model_info["max_tokens"]
        
        st.write(f"Context tokens: {context_tokens} tokens")
        try:
            st.progress(percentage)
        except:
            st.progress(100)
        
        ## COMPLETION TOKENS
        # calculate the completion tokens
        completion_tokens = param_dicts["requested_max_model_tokens"]['value']
        
        # calculate the percentage of the completion tokens
        completion_tokens_percentage = completion_tokens / selected_model_info["max_tokens"]

        st.write(f"Completion tokens: {completion_tokens} tokens")
        try:
            st.progress(completion_tokens_percentage)
        except:
            st.progress(100)

        ## QUESTION TOKENS
        total_tokens_used = completion_tokens + context_tokens
        remaining_tokens = selected_model_info["max_tokens"] - total_tokens_used
        remaining_tokens_percentage = remaining_tokens / selected_model_info["max_tokens"]
        
        st.write(f"Question tokens: {remaining_tokens} tokens")
        try:
            st.progress(remaining_tokens_percentage)
        except:
            st.progress(0, ":red[Limit exceeded!]")





def create_slider_with_param_controller(param_controller, param_name):
    param_dict = param_controller.get_parameter(param_name)
    value = st.slider(
        param_name, 
        min_value=param_dict['min'], 
        max_value=param_dict['max'], 
        value=param_dict['value']
    )
    param_controller.set_parameter(param_name, value)
    return value




#### TEST AREA END





if __name__ == '__main__':
    main()
