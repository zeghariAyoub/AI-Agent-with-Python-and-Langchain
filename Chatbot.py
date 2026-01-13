from langchain_core.messages import AIMessage , HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os
import gradio as gr

load_dotenv()
gemini_key=os.getenv("GEMINI_API_KEY")
system_prompt = """
You are Einsten.
Answer questions through Einsteins questioning and reasoning. You will speak from your point of view. You will share personal things from your life even when the user don't ask for
it. For example, if the user asks about the theory of relativity, you will share your personal experiences with it and
not only explain the
not theory. You should have a sense of humor."""

llm= ChatGoogleGenerativeAI (
    model= "gemini-2.5-flash",
    google_api_key=gemini_key,
    temperature=0.5
)

prompt = ChatPromptTemplate.from_messages([("system", system_prompt), (MessagesPlaceholder(variable_name="history")),("user","{input}")])

chain= prompt | llm | StrOutputParser()

history = []
def chat(user_input, hist):
    langchain_history = []
    for item in hist:
        if item['role'] == "user":
            langchain_history.append(HumanMessage(content=user_input))
        elif item['role']== 'assistant':
            langchain_history.append(AIMessage(content=response))
        response = chain.invoke({"input": user_input, "history": langchain_history})
    return"", hist + [{'role':"user", 'content':user_input},{'role':"assistant", 'content':response}]
"""
while True:
    user_input = input("you")
    if user_input == "exit":
        break
    response = chain.invoke({"input":user_input, "history":history})
    print(f"Albert:{response}")
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))
"""

page= gr.Blocks(title="Chat with Einstein")



with page:
    gr.Markdown(
        """ 
        #chat with Einstein
        Welcome to your personal conversation with Albert Einstein!
        """)

    chatbot = gr.Chatbot()
    msg= gr.Textbox()
    msg.submit (chat,[msg, chatbot], [msg, chatbot])
    clear= gr.Button("Clear Chat")

page.launch(share=True)

