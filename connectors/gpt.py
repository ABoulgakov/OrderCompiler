from openai import OpenAI
import ast
import pandas as pd

def call_gpt(key: str, query: str, df_output: bool = False):
    """
    Calls Chat GPT and outputs a pandas df
    """

    client = OpenAI(
    api_key=key
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": query}
    ]
    )

    gpt_answer_str = completion.choices[0].message.content
    orders_list = ast.literal_eval(gpt_answer_str)

    if df_output:
        try:
            df = pd.DataFrame(orders_list)
            df.index += 1
            return df
        except:
            return orders_list
    
    else:
        return orders_list