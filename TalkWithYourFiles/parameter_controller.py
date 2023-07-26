class ParameterController:
    def __init__(self):
        self.parameters = {}

    def register_parameter(self, name, type, default, description=None, **kwargs):
        parameter_info = {
            'type': type,
            'default': default,
            'value': default,
            'description': description
        }
        parameter_info.update(kwargs)
        self.parameters[name] = parameter_info

    def get_parameter(self, name):
        return self.parameters.get(name, {})

    def set_parameter(self, name, value):
        if name in self.parameters:
            self.parameters[name]['value'] = value
        else:
            raise Exception(f"Parameter {name} is not registered.")

    def get_all_parameters(self):
        return self.parameters

    def setup_default_parameters(self):
        self.register_parameter('chunk_size', int, 1000, 'Chunk size for text splitting', min=200, max=2000)
        self.register_parameter('chunk_overlap', int, 100,"Chunk overlap for wider context", min=0, max=800)
        self.register_parameter('top_related_chunks', int, 3, 'Amount of chunks to retrieve among the most related ones', min=1, max=30)
        self.register_parameter('requested_max_model_tokens', int, 256, 'Maximum tokens for the model', min=1, max=16000)
        self.register_parameter('displayed_max_response_tokens', int, 100, 'Maximum tokens for the chain response', min=1, max=16000)
        self.register_parameter('model_name', 
                                str,
                                "text-davinci-003", 
                                "Model to be used in the qa_chain", 
                                model_list=[
                                    {
                                        'name': 'text-davinci-003',
                                        'description': '	Can do any language task with better quality, longer output, and consistent instruction-following than the curie, babbage, or ada models. Also supports some additional features such as inserting text.',
                                        'max_tokens': 4097,
                                        'training_data': 'Up to Sep 2021' 
                                    },
                                    {
                                        'name': 'gpt-3.5-turbo',
                                        'description': 'Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration 2 weeks after it is released.',
                                        'max_tokens': 4096,
                                        'training_data': 'Up to Sep 2021'
                                    },
                                    {
                                        'name': 'gpt-3.5-turbo-16k',
                                        'description': 'Same capabilities as the standard gpt-3.5-turbo model but with 4 times the context.',
                                        'max_tokens': 16384,
                                        'training_data': 'Up to Sep 2021'
                                    },
                                    {
                                        'name': 'gpt-3.5-turbo-0613',
                                        'description': 'Snapshot of gpt-3.5-turbo from June 13th 2023 with function calling data. Unlike gpt-3.5-turbo, this model will not receive updates, and will be deprecated 3 months after a new version is released.',
                                        'max_tokens': 4096,
                                        'training_data': 'Up to Sep 2021'
                                    },
                                    {
                                        'name': 'gpt-3.5-turbo-16k-0613',
                                        'description': 'Snapshot of gpt-3.5-turbo-16k from June 13th 2023. Unlike gpt-3.5-turbo-16k, this model will not receive updates, and will be deprecated 3 months after a new version is released.',
                                        'max_tokens': 16384,
                                        'training_data': 'Up to Sep 2021'
                                    },
                                    {
                                        'name': 'gpt-4',
                                        'description': 'More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration 2 weeks after it is released.',
                                        'max_tokens': 8192,
                                        'training_data': 'Up to Sep 2021'
                                    },
                                    {
                                        'name': 'gpt-4-0613',
                                        'description': 'Snapshot of gpt-4 from June 13th 2023 with function calling data. Unlike gpt-4, this model will not receive updates, and will be deprecated 3 months after a new version is released.',
                                        'max_tokens': 8192,
                                        'training_data': 'Up to Sep 2021'
                                    },
                                    {
                                        'name': 'gpt-4-32k',
                                        'description': 'Same capabilities as the base gpt-4 mode but with 4x the context length. Will be updated with our latest model iteration.',
                                        'max_tokens': 32768,
                                        'training_data': 'Up to Sep 2021'
                                    },
                                    {
                                        'name': 'gpt-4-32k-0613',
                                        'description': 'Snapshot of gpt-4-32 from June 13th 2023. Unlike gpt-4-32k, this model will not receive updates, and will be deprecated 3 months after a new version is released.',
                                        'max_tokens': 32768,
                                        'training_data': 'Up to Sep 2021'
                                    }
                                    ]
                                )                  

        self.register_parameter('chatbot_llm', 
                                'llm', 
                                "text-davinci-003", 
                                'Wrapped version of the text-davinci-003 model from OpenAI API', 
                                temperature=0.4, 
                                prompt=
                                    """
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
                                    """,
                                prompt_input_variables=["history","input"]
                                )