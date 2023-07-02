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


