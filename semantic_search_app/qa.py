import openai
openai.api_key="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"

def create_prompt(context,query):
    header = "Answer the question if you are 100 percent sure using the provided context only, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"

def generate_answer(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END']
    )
    return (response.choices[0].text).strip()