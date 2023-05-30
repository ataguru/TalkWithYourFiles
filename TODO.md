

2) Integrate changing the model in use functionality to the GUI. Find a model that can handle a lot bigger tokens, probably the quality of the model will be poorer than OpenAIs but user should be able to do it. Make sure to mention all the limitations and related properties of the model in the GUI. 

3) Implement error handling for cases where the prompt (chunks from docs + question) is bigger than the maximum token limit. Keep in mind that it'll be possible to use other models. So a LLM class that is flexible to use with any other model might be good to have.
 

4) do something to further balance prompt & completion length
