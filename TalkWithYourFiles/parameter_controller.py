class ParameterController:
    def __init__(self):
        self.parameters = {}

    def register_parameter(self, name, type, default, description=None, **kwargs):
        parameter_info = {
            'type': type,
            'default': default,
            'value': default,  # Added this line
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
        self.register_parameter('model_name', str, "text-davinci-003", "Model to be used in the qa_chain", model_list=['text-davinci-003', 'gpt-3.5-turbo'])   