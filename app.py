from flask import Flask, render_template, request, jsonify
from typing import Union
from langchain import ConversationChain
from langchain.llms import OpenAI
import os
import openai
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.agents import load_tools, initialize_agent, AgentType

os.environ["OPENAI_API_KEY"] = 'key'
OPENAI_API_KEY = 'key' 
openai.api_key = OPENAI_API_KEY
llm = OpenAI(model_name="pernance")

transactions =[ 
    {"date": "2021-01-01", "amount": 1000, "category": "income", "description": "salary" }, 
    { "date": "2021-01-02", "amount": -50, "category": "groceries", "description": "milk and eggs" },
    { "date": "2021-01-03", "amount": -100, "category": "entertainment", "description": "movie tickets" },
    { "date": "2021-01-04", "amount": -20, "category": "transportation", "description": "bus fare" },
    { "date": "2021-01-05", "amount": -200, "category": "bills", "description": "electricity bill" }, 
    { "date": "2021-01-06", "amount": -30, "category": "groceries", "description": "bread and cheese" }, 
    { "date": "2021-01-07", "amount": -150, "category": "clothing", "description": "new shoes" },
    { "date": "2021-01-08", "amount": -40, "category": "healthcare", "description": "prescription drugs" }, 
    { "date": "2021-01-09", "amount": -80, "category": "education", "description": "online course" }, 
    { "date": "2021-01-10", "amount": -60, "category": "entertainment", "description": "pizza delivery" },
    {"date": "2021-01-11", "amount": -25, "category": "transportation", "description": "taxi ride" },
    { "date": "2021-01-12", "amount": -300, "category":"bills", "description":"internet bill" },
    { "date":"2021-01-13", "amount":-50, "category":"groceries", "description":"fruits and vegetables" }
]

summary_template = "On {date}, you {action} {amount} for {category}: {description}."
summary = ""
for transaction in transactions:
    date = transaction["date"]
    amount = transaction["amount"]
    category = transaction["category"]
    description = transaction["description"]
    action = "received" if amount > 0 else "spent"
    amount_formatted = "${:.2f}".format(abs(amount))
    summary += summary_template.format(date=date, action=action, amount=amount_formatted, category=category, description=description)

summary = "Summary: Let's summarize your recent financial activities:\n\n" + summary# + "As financial advisor, Give this person additional advice to make sure they can become financially stable.  make sure that the responses are not generic and are extremely personalized with actual advice"

print(summary)

conversation = ConversationChain(llm=llm, verbose=True)

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        # response: dict = openai.Completion.create(
        #     model='pernance',
        #     prompt=prompt,
        #     temperature=0.9,
        #     max_tokens=150,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0.6,
        # )
        response: dict = conversation.get_output(prompt)
        choices: dict = response.get('choices')[0]
        text = choices.get('text')
    except Exception as e:
        print('There seems to be an issue. We will get back to you soon: ', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = message
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    prompt = summary + "Specific Advice: "+ prompt+ " .Make sure that the advice is extremely personal and specific."
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
    else:
        bot_response = 'Something went wrong :(... Please try again after some time'

    return bot_response


def get_Chat_response(input):
    prompt_list: list[str] = [summary]
    user_input: str = input
    response: str = conversation.get_bot_response(user_input, prompt_list)
    print(response)
    return response


app = Flask(__name__)
@app.route("/")

def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET","POST"])                
                             
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)



if __name__ == '__main__':
    print("Welcome to the Chatbot! Type 'exit' to quit.")

    app.run()
    conversation.run(summary)
