import openai

openai.api_key ="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"

system_prompt_template = """You are able to give the name of a cryptocurrency and its launch date given its symbol. Example output would be:
Sure this is the json:
{"name": "Bitcoin",
"date": "2009"}
"""

def eval(llm_output, tests):
    eval_prompt = """You are responsible for testing the output of a LLM against user-defined test requirements. You will output a list object with each value being 'True' or 'False' for whether the LLM output passes its corresponding test.

    EXAMPLE INPUT: "LLM Output: This is what the JSON would be: {\n    "type": "percent_price",\n    "currency": "DOGE",\n    "percent": "10",\n    "direction": "down",\n    "window": "30",\n    "channel": { "name": "webhook" },\n    "exchange": "Coinbase"\n}"
    Tests: ["Output should ONLY contain JSON with no extra words before or after"]
    EXAMPLE OUTPUT: [False]
    """
    test_prompt = f"LLM Output: {llm_output} \n Tests: {tests}"

    run = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0,
    messages=[
            {"role": "system", "content": eval_prompt},
            {"role": "user", "content": test_prompt},
        ]
    )

    response = run['choices'][0]['message']['content']
    return response

def test(system_prompt, user_prompt, tests, runs, model):
    store = {'params': [system_prompt, user_prompt, model]}

    for i in range(runs):
    
        run = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = 0,
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        response = run['choices'][0]['message']['content']

        evaluation = eval(response, tests)

        store[i] = [response, evaluation]
    
    return store

# print(test(system_prompt_template, "DOGE", ["Output should ONLY contain JSON with no extra words before or after"], 3, "gpt-3.5-turbo"))
# TODO: break up user given command into simpler cases
print(eval('Sure, here is the information for DOGE:\n\n{\n  "name": "Dogecoin",\n  "date": "2013"\n}', ["Output should contain JSON", "Output should not have any extraneous information before or after"]))