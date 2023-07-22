
#### Token Balancer implementation will be integrated into the application in the next release.
#### It's not tested yet.

## total chunks to send to the model:
## context_tokens: chunks + user question 
## Requested completion tokens: model's response
## selected max tokens:model's maximum token size

### limits
### context tokens + requested completion tokens < max tokens


class TokenBalancer:
    def __init__(self, parameter_controller):
        self.parameter_controller = parameter_controller

    def get_parameter(self, parameter_name):
        parameter_info = self.parameter_controller.get_parameter(parameter_name)
        if 'value' not in parameter_info:
            raise Exception(f"Parameter {parameter_name} is not registered or doesn't have a value.")
        return parameter_info['value']

    def token_calculator_context_tokens(self):
        chunk_size = self.get_parameter('chunk_size')
        top_related_chunks_count = self.get_parameter('top_related_chunks')
        max_tokens = self.get_parameter('requested_max_model_tokens')

        context_tokens = chunk_size * top_related_chunks_count 
        percentage = context_tokens / max_tokens
        return context_tokens, percentage

    def token_calculator_completion_tokens(self):
        requested_max_model = self.get_parameter('requested_max_model_tokens')
        max_tokens = self.get_parameter('requested_max_model_tokens')

        completion_tokens = requested_max_model
        completion_tokens_percentage = requested_max_model / max_tokens
        return completion_tokens, completion_tokens_percentage

    def token_calculator_question_tokens(self):
        context_tokens, _ = self.token_calculator_context_tokens()
        completion_tokens, _ = self.token_calculator_completion_tokens()
        max_tokens = self.get_parameter('requested_max_model_tokens')

        total_tokens_used = completion_tokens + context_tokens
        question_tokens = max_tokens - total_tokens_used
        question_tokens_percentage = question_tokens / max_tokens
        return question_tokens, question_tokens_percentage

    def balance_tokens(self, chunks, user_question, model_response):
        # Implement the logic to balance tokens here.
        pass
