from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


def chat_openai():
    llm = ChatOpenAI()
    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content="hi!"),
    ]
    response = llm.invoke(messages)
    print(response)


#

def chat_invoke():
    llm = ChatOpenAI()
    text = "武汉今天天气怎么样?"
    print(llm.invoke(text))


if __name__ == '__main__':
    chat_invoke()
