from flow_coordinator import FlowCoordinator
from parameter_controller import ParameterController

import streamlit as st
from streamlit_modules.streamlit_components import *
from streamlit_modules.streamlit_chat import main_chat


def main():
    ## Instantiating a ParameterController instance to be used in the flow_coordinator.
    param_controller = ParameterController()
    
    ## Registering default parameters.
    param_controller.setup_default_parameters()

    ## Instantiating the Flow Coordinator
    flow_coordinator = FlowCoordinator(param_controller) 


    ### Streamlit Interface

    # Page configurations
    setup_page_configurations()

    # Header
    setup_header_area()

    # Sidebar
    setup_sidebar(flow_coordinator)

    # Setting up each tab for the GUI
    tab0, tab1, tab2 = st.tabs(["Chat Bot", "QA Chain", "Active Params"])


    with tab0:
        main_chat()
    with tab1:
        # Tab 1 QA Chain Over Files
        tab1_qa_chain_files(param_controller, flow_coordinator)
    with tab2:
        tab2_active_params(param_controller)















#### TEST AREA START

## test if everything gets updated.
## customise the tab2
## integrate chat
## deploy demo

#### TEST AREA END





if __name__ == '__main__':
    main()
