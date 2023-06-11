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

    ##### PAGE CONFIGURATIONS
    st.set_page_config(
                    page_title="Talk With Your Files",
                    page_icon="random",
                    layout="centered", # centered or wide
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
    ##If used values here will be used as parameters. 
    ##If not default values were already registered in the flow_coordinator.py

    if show_advanced:
        ## Instantiating a ParameterController instance to be used in the flow_coordinator at the end.
        param_controller = ParameterController()
        
        ## Registering default parameters.
        param_controller.setup_default_parameters()        


        ## Get Parameters (default)
        # chunk size
        chunk_size_param_dict = param_controller.get_parameter('chunk_size')
        # chunk overlap
        chunk_overlap_param_dict = param_controller.get_parameter('chunk_overlap')
        # top related chunks / chunks to retrieve
        top_related_chunks_param_dict = param_controller.get_parameter('top_related_chunks')

        # model name from OpenAI
        model_name_param_dict = param_controller.get_parameter('model_name') 




        ### GUI
        ## columns to configure parameters in the GUI
        col1, col2, col3 = st.columns(3)
        
        ## Text processing parameters
        with col1:
            chunk_size_GUI = st.slider("Chunk Size", 
                                       min_value=chunk_size_param_dict['min'], 
                                       max_value=chunk_size_param_dict['max'], 
                                       value=chunk_size_param_dict['value']
                                       )

        with col2:
            chunk_overlap_GUI = st.slider("Chunk Overlap",
                                       min_value=chunk_overlap_param_dict['min'], 
                                       max_value=chunk_overlap_param_dict['max'], 
                                       value=chunk_overlap_param_dict['value']
                                       )
            
        with col3:
            top_related_chunks_GUI = st.slider("Top Related Chunks",
                                        min_value=top_related_chunks_param_dict['min'],
                                        max_value=top_related_chunks_param_dict['max'],
                                        value=top_related_chunks_param_dict['value']                                   
                                        )


        model_name_GUI = st.selectbox('Select a Model:', model_name_param_dict['model_list'])


        # Update the parameters in the parameter controller after the interactions with the slider.
        param_controller.set_parameter('chunk_size', chunk_size_GUI)
        param_controller.set_parameter('chunk_overlap', chunk_overlap_GUI)
        param_controller.set_parameter('top_related_chunks', top_related_chunks_GUI)
        param_controller.set_parameter('model_name', model_name_GUI)
        

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
