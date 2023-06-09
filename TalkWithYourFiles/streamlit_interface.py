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
    ##### FLOW COORDINATOR
    # load environment variables, 
    # prepare parameters, 
    # initialize file handler factory, text processor, qa chain runner
    # import the definition of the run function
    flow_coordinator = FlowCoordinator()


    st.set_page_config(page_title="Talk With Your Files")  # can add parameters to style the page
    st.header("Talk With Your Files")

    files = st.file_uploader("Upload files", type=["pdf", "docx", "txt","csv"], accept_multiple_files=True)

    ### TEST AREA START ###
    ## a toggle switch for verbose logging, not in use right now.

    st.sidebar.header("Advanced Settings")
    show_advanced = st.sidebar.checkbox("Show Advanced Settings")
    if show_advanced:
        ## implement parameter controller logic
        param_controller = ParameterController.get_instance()
        chunk_size_param = param_controller.get_parameter('chunk_size')

        ## remove later or integrate
        # st.sidebar.subheader("Text Processing")
        #verbose_logging = st.checkbox('Verbose Logging')

        # Set up the chunk size slider & dynamically adjust the parameter in the param_controller
        chunk_size_GUI = st.slider("Set Chunk Size", min_value=chunk_size_param['min'], max_value=chunk_size_param['max'], value=chunk_size_param['value'])
        param_controller.set_parameter('chunk_size', chunk_size_GUI)  # Update the parameter after interaction with the slider
        

    ### TEST AREA END ###



    user_question = st.text_input("Please ask me about your uploaded files and I shall help you: ")




    if user_question and files:
        response = flow_coordinator.run(files, user_question)
        st.write(response)


if __name__ == '__main__':
    main()
