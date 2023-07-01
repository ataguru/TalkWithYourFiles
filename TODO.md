
1) Adress the issue mentioned here: https://github.com/Safakan/TalkWithYourFiles-LLM-GUI/issues/1
We need to make sure the maximum chunk size limit rule is followed, so probably alternative or custom functions for chunking alone will fix it.

2) Integrate changing the model in use functionality to the GUI. Find a model that can handle a lot bigger tokens, probably the quality of the model will be poorer than OpenAIs but user should be able to do it. Make sure to mention all the limitations and related properties of the model in the GUI. 

3) Implement error handling for cases where the prompt (chunks from docs + question) is bigger than the maximum token limit. Keep in mind that it'll be possible to use other models. So a LLM class that is flexible to use with any other model might be good to have.
 

4) do something to further balance prompt & completion length



5) 
Each time an interaction occurs in the Streamlit app, Streamlit reruns the script that's powering the app. In your case, it would rerun the streamlit_interface.py script from top to bottom.

So if the user interacts with a widget, such as the slider or the text input, Streamlit will rerun the entire script and refresh the displayed page. This is why the return value of the widget functions (like st.slider()) will always be the current state of that widget on the page.

It's also important to note that any code you want to avoid running on each interaction should be inside a function and should be called using st.cache. For instance, if you have an expensive computation or a network call that doesn't need to happen every time a widget value changes, you can put this in a separate function and use @st.cache decorator above the function definition. This tells Streamlit to only rerun the function when the input arguments change.


6) are there ways to incorporate something like a debug mode to test & work on the new changes on my app? I can create a new branch in git, but still, what are some other options?


7) Integrate logging for some more details: chunk sizes? params? 

8) cost calculator?


9)  ** do something to further balance prompt & completion length

10) C:\Users\aCat\anaconda3\envs\aiplayground\lib\site-packages\langchain\llms\openai.py:696: UserWarning: You are trying to use a chat model. This way of initializing it is no longer supported. Instead, please use: `from langchain.chat_models import ChatOpenAI`
  warnings.warn(


11) GPT suggestions:
Bad: Currently, there's no type checking or validation for parameter values when set, which could potentially lead to issues if invalid values are used.
Improvements: I would suggest adding some validation in the set_parameter method to ensure that the value being set is valid for the specified type.


b) Out-of-the-box suggestions:

You could consider implementing a caching mechanism to reduce the computational cost of creating embeddings if the same documents need to be processed repeatedly.
For handling a large number of documents, a batch processing system might be beneficial.
In terms of error handling, consider introducing custom exception classes instead of throwing the generic Exception. This would make debugging easier and your code more robust.
It would be beneficial to add logging throughout your application. This would help in debugging and also in understanding how your application is behaving in production.
For long-running processes, consider implementing a progress monitoring system to give users feedback on the state of the operation.
Consider adding automated tests to ensure your code behaves as expected. This is particularly important when your application goes into production.


12) count the tokens in the process to be sure! chunking is not doing exact splits! check out here: https://www.youtube.com/watch?v=au2WVVGUvc8




NOTE: flow_coordinator only initilasied right before the chian is going to run.