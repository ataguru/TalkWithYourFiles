import streamlit as st

##########################################################
##########################################################
### QA CHAIN
##########################################################
##########################################################

def advanced_parameters_section(param_controller):
    #### TOP ROW TO SHOW AND ALLOW DYNAMIC PARAMETERS

    ## 4 columns to configure text processing parameters in the GUI
    column_chunk_size, column_chunk_overlap, column_top_related_chunks, column_requested_max_model_tokens = st.columns(4)

    with column_chunk_size:
        create_slider_with_param_controller(param_controller, "chunk_size", "Chunk Size")

    with column_chunk_overlap:
        create_slider_with_param_controller(param_controller, "chunk_overlap", "Chunk Overlap")

    with column_top_related_chunks:
        create_slider_with_param_controller(param_controller, "top_related_chunks", "Top Related Chunks to Retrieve")

    with column_requested_max_model_tokens:
        create_slider_with_param_controller(param_controller, "requested_max_model_tokens", "Max Requested Tokens for Completion")



    ##### SECOND ROW TO CONFIGURE MODEL DETAILS AND SHOW TOKEN USAGE
    column_model_name, column_model_details, columns_token_limits = st.columns(3)

    
    ## Setting up the select box with the model names.
    with column_model_name:
        selected_model_info = create_drop_down_with_param_controller(param_controller, 
                                                                    "model_name", 
                                                                    'Select a Model:'
                                                                    )
        
        st.write(f"Description: {selected_model_info['description']}")


         
    with column_model_details:
        # Display the selected model's max tokens
        st.write(f"Max Tokens: {selected_model_info['max_tokens']}")
        st.write("Beaware: Each model has its own maximum token limit. Make sure to leave room for the question.")
        st.write("Total tokens = Prompt tokens + Completion tokens")
        st.write("Prompt tokens = Context tokens + Question tokens")

 
    ## PROGRESS BARS TO SHOW THE TOKEN USAGE WITH CURRENT FILTERS


    with columns_token_limits:        
        ## Context Tokens  
        context_tokens, context_tokens_percentage = token_calculator_context_tokens(
                                                    param_controller.get_parameter("chunk_size")["value"], 
                                                    param_controller.get_parameter("top_related_chunks")["value"], 
                                                    selected_model_info["max_tokens"]
                                                    )
        
        create_progress_bar(
                            "Context Tokens",
                            context_tokens,
                            context_tokens_percentage
                            )
        

        ## Completion Tokens
        completion_tokens, completion_tokens_percentage = token_calculator_completion_tokens(
                                                            param_controller.get_parameter("requested_max_model_tokens")["value"],
                                                            selected_model_info["max_tokens"]
                                                            )
        
        create_progress_bar(
                            "Completion Tokens",
                            completion_tokens,
                            completion_tokens_percentage
                            )

        ## Question Tokens
        question_tokens, question_tokens_percentage = token_calculator_question_tokens(
                                                                                    completion_tokens,
                                                                                    context_tokens,
                                                                                    selected_model_info["max_tokens"]
                                                                                    )
        create_progress_bar(
                            "Question Tokens",
                            question_tokens,
                            question_tokens_percentage,
                            reverse_limit_excess_behaviour=True
                            ) 




def create_authorization_box(flow_coordinator): 
    ##### Authorization & Setting up the environment variable
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = None
    
    input_api_key = st.sidebar.text_input(
        "Enter your OpenAI API key", 
        type="password",
    )

    if input_api_key:
        st.session_state.api_key = input_api_key
        st.session_state.api_key_valid = flow_coordinator.authorizer.validate_key(st.session_state.api_key)
        flow_coordinator.authorizer.set_api_key_environment_variable(st.session_state.api_key)    

    authorization_status_box(st.session_state.api_key_valid)

        


def authorization_status_box(isvalid):
    """Creates a green or red box depending on the value of the `isvalid` variable."""
    if isvalid:
        color = "green"
        text = "Validated"
    else:
        color = "darkred"
        text = "Not Validated"
    style = f"""
    .{color}-box {{
        background-color: {color};
        border: 1px solid black;
        padding: 10px;
    }}
    """
    st.sidebar.markdown(f"""
    <style>{style}</style>
    <div class="{color}-box">{text}</div>
    """, unsafe_allow_html=True)


def create_slider_with_param_controller(param_controller, param_name, slider_title):
    param_dict = param_controller.get_parameter(param_name)
    value = st.slider(
        slider_title, 
        min_value=param_dict['min'], 
        max_value=param_dict['max'], 
        value=param_dict['value']
    )
    param_controller.set_parameter(param_name, value)
    return value

def create_progress_bar(title, unit_tokens, unit_percentage, reverse_limit_excess_behaviour=False):
    st.write(f"{title}: {unit_tokens} tokens")
    # If user sets up unrealistic parameters.   
    try:
        st.progress(unit_percentage)
    except:
        ## the usual behaviour is the limit is exceeded and the bar is full.
        if reverse_limit_excess_behaviour:
            st.progress(0, ":red[Limit exceeded!]")
        else:
            st.progress(100, ":red[Limit exceeded!]")



def create_drop_down_with_param_controller(param_controller, param_name, drop_down_title):
    param_dict = param_controller.get_parameter(param_name)

    options = [model['name'] for model in param_dict['model_list']]

    selected_option = st.selectbox(drop_down_title, options)

    selected_model_info = next((model for model in param_dict['model_list'] if model['name'] == selected_option), None)
    
    param_controller.set_parameter(param_name, selected_option)

    return selected_model_info





##########################################################
##########################################################
### FOR TOKEN CALCULATIONS
##########################################################
##########################################################


##### these will be moved to the token balancer class
## Token Balancer Functions
def token_calculator_context_tokens(chunk_size, top_related_chunks_count, selected_model_max_tokens):
    ## CONTEXT TOKENS    
    # Context is spllitted into chunks & then top requested ones are used.
    context_tokens = chunk_size * top_related_chunks_count 

    # calculate the percentage of the context tokens
    percentage = context_tokens / selected_model_max_tokens

    return context_tokens, percentage

def token_calculator_completion_tokens(requested_max_model, selected_model_max_tokens):
    # the max limit we request from model for completion
    completion_tokens = requested_max_model
    completion_tokens_percentage = requested_max_model / selected_model_max_tokens

    return completion_tokens, completion_tokens_percentage

def token_calculator_question_tokens(completion_tokens, context_tokens, selected_model_max_tokens):
    # remaining tokens from total used after completion & context tokens are question tokens.
    total_tokens_used = completion_tokens + context_tokens
    question_tokens = selected_model_max_tokens - total_tokens_used
    question_tokens_percentage = question_tokens / selected_model_max_tokens

    return question_tokens, question_tokens_percentage



##########################################################
##########################################################
### Chatbot
##########################################################
##########################################################
