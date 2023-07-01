import openai

def get_initial_message():
    messages=[
            {"role": "system", "content": "You are a helpful Doctor. Who anwers brief questions about Medicine,deases,recommendations."},
            {"role": "user", "content": "I want to do consultation"},
            {"role": "assistant", "content": "Thats awesome, what do you want to know aboout ?"},
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    #print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
