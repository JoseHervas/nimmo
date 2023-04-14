import openai, tiktoken, sys, os
sys.path.append('../')
from messages import MessageStore

class ChatEngine:
    api_key = None

    def __init__(self):
        self.api_key = os.getenv('OPENAI_TOKEN')

    def count_tokens_from_string(self, string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def suggest_journals(self, discipline):
        openai.api_key = self.api_key
        model_engine = "text-davinci-002"

        query = f"{discipline}\n- List the top 10 scientific journals in the provided discipline, along with the publication frequency of each journal and its Impact Factor (IF)."
        response = openai.Completion.create(
            engine=model_engine,
            prompt=query,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        if response.choices[0].text:
            return(response.choices[0].text)
        else:
            return("No response was returned from OpenAI.")

    def create_summary(self, papers):
        print("[+] Creating summary with ChatGPT")
        chatgpt_engine = "gpt-3.5-turbo"
        openai.api_key = self.api_key
        store = MessageStore()
        messages = store.get_messages()
        for paper in papers:
                print("\t[+] Running query number", papers.index(paper)+1, "of", len(papers))
                text = f"Resume este artículo científico en 1 línea. Recuerda mencionar el título, el numero de citas y la venue donde se ha publicado : {paper}"
                store.add_message({"role": "user", "content": text})
                response = openai.ChatCompletion.create(
                        model=chatgpt_engine, messages=[messages[0], {"role": "user", "content": text}])
                response_content = response.choices[0].message.content
                store.add_message({"role": "assistant", "content": response_content})
            
        print("\t[!] Writing general summary of everything")
        query = "Resume las noticias científicas del dia: "
        for message in messages:
            if (message["role"] == "assistant"):
                query += message["content"]
        store.add_message({"role": "user", "content": query})
        response = openai.ChatCompletion.create(model=chatgpt_engine, messages=[messages[0], {"role": "user", "content": query}])
        response_content = response.choices[0].message.content
        store.add_message({"role": "assistant", "content": response_content})  
            
        return(response_content)

    def answer_question(self, text):
        store = MessageStore()
        store.add_message({"role": "user", "content": text})
        chatgpt_engine = "gpt-3.5-turbo"
        openai.api_key = self.api_key
        full_messages_history = store.get_messages()
        tokens_count = 0
        messages = []
        for message in reversed(full_messages_history):
            tokens_count += self.count_tokens_from_string(message["content"], "gpt2")
            messages.insert(0, message)
            if tokens_count >= 4096:
                break
        response = openai.ChatCompletion.create(model=chatgpt_engine, messages=messages)
        response_content = response.choices[0].message.content
        store.add_message({"role": "assistant", "content": response_content})
        return(response_content)