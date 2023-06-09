class ParameterController:
    _instance = None

    def __init__(self):
        if ParameterController._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ParameterController._instance = self

        self.parameters = {}

    @staticmethod
    def get_instance():
        if ParameterController._instance is None:
            ParameterController()
        return ParameterController._instance

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
