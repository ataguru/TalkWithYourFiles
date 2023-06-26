
## total chunks to send to the model:
## chunks from docs + user question + model's response < model's maximum token size


class TokenBalancer:
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens

    def balance_tokens(self, chunks, user_question, model_response):
        # Implement the logic to balance tokens here.
        # This could involve adjusting the chunks, user_question, and model_response
        # to ensure their total token count is less than self.max_tokens.
        pass
