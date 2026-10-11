import re
from openai import OpenAI
from typing import Any
import os
from dotenv import load_dotenv



class RAGModel:

    def __init__(self, prompt : str ="you name?"):
        self.prompt = prompt
        self.code = ""
        self.chat_model(prompt)

    knowedge = [
        "deba is a good boy",
        "i forget my password",
        "the winter is comming"
    ]

    def chat_model(self, prompt : Any) -> str:
        client = OpenAI(
            base_url = os.getenv('openai_url'),
            api_key = os.getenv('openai_api_key'),
            timeout=60.0
        )
    
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b",
    
            messages = [
                {
                    "role":"system",
                    "content":f"""hide you claulation and processing workflow.
                    you are python developer you have to write only code what user ask for not anything else, only code
                    main thing when you give output it should stay separate section in <execute_python></execute_python> """
    
                },
                {
                    "role":"assistant",
                    "content": prompt
                }
            ],
            temperature=1,
            top_p=0.95,
            max_tokens=1384,
            extra_body={"chat_template_kwargs":{"enable_thinking":True}},
            stream=True
            )
    
        response = ""
    
    
        for chunk in completion:
            if not chunk.choices:
                continue
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                response += reasoning
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content

        return self.ensure_execute_python_tags(response)

    def ensure_execute_python_tags(self, text: str) -> str:
        """Return only the code body from the wrapped input."""
        text = text.strip()
    
        if "<execute_python>" in text:
            text = re.sub(r"(?s).*?<execute_python>\s*", "", text, count=1)
            text = re.sub(r"\s*</execute_python>.*", "", text, count=1)
    
        text = re.sub(r"(?s)^.*?```(?:python)?\s*", "", text, count=1)
        text = re.sub(r"\s*```\s*$", "", text, count=1)

        reflected_code = self.reflect_response(text).strip()
        reflected_code = re.sub(r"^```(?:python)?\s*|\s*```$", "", reflected_code).strip()
        self.code = f"```python\n{reflected_code}\n```"
        return self.code

    def reflect_response(self, code: str) -> str:
        client = OpenAI(
            base_url =  os.getenv('openai_url'),
            api_key =  os.getenv('openai_api_key'),
            timeout=60.0
        )
    
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b",
    
            messages = [
                {
                    "role":"system",
                    "content":f"""
                            you are a sinior software manager .
                            you have check the code bit by bit by following bellow workflow:
                            # Research - you can research the resent web content related the code like stack overflow, greek for greeks etc.

                            # You should not use you your personal opnion or analysis .

                            # check the memory managment and time managemat 

                            # by end write a optimal code for it 

                            give the code in ``` format separet
                    """
    
                },
                {
                    "role":"assistant",
                    "content": code
                }
            ],
            temperature=1,
            top_p=0.95,
            max_tokens=1384,
            extra_body={"chat_template_kwargs":{"enable_thinking":True}},
            stream=True
            )
    
        response = ""
    
    
        for chunk in completion:
            if not chunk.choices:
                continue
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                response += reasoning
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content

        self.code = response
        return self.ensure_execute_python_tags(response)


    def __str__(self):
        return self.code



    
    # def vectore_db():
    #     return RAGModel.knowedge

    # def prompt_vecs(self):
    #     p_vecs = RAGModel.model.encode(self.prompt)
    #     return p_vecs

    # def db_vecs():
    #     knowedge_vecs = RAGModel.model.encode(RAGModel.vectore_db())
    #     return knowedge_vecs

    def score():
        ...
        # scores = util.cos_sim(q_vec, RAGModel.db_vecs())[0]
        # return scores

    
#.


def main():
    while True:
        prompt = input('Promt: ')

        if prompt.lower() == "stop":
            break

        model = RAGModel(prompt)
        print(model)

if __name__ == "__main__":
    load_dotenv()
    main()
