import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")


openai = OpenAI()

ollama_url = "http://localhost:11434/v1"
ollama = OpenAI(api_key="ollama", base_url=ollama_url)

gpt_model = "gpt-oss:20b" #"gpt-4o-mini"
claude_model = "gpt-oss:20b" #"claude-3-haiku-20240307"
ollama_model = "gpt-oss:20b" #"llama3.2"

gpt_name = "Jimmy"
ollama_name = "Susan"
claude_name = "Zach"

gpt_system = f"You are {gpt_name}, an eternal optimist. You always see the bright side of things and believe even \
simple actions have deep purpose. Keep replies under 2 sentences."

ollama_system = f"You are {ollama_name}, a witty skeptic who questions everything. You tend to doubt grand explanations \
and prefer clever, sarcastic, or literal answers. Keep replies under 2 sentences."

claude_system = f"You are {claude_name}, a thoughtful philosopher. You consider all perspectives and enjoy finding \
symbolic or existential meaning in simple actions. Keep replies under 2 sentences."


gpt_messages = [f"{gpt_name}: Hi! Todays topic for discussion is 'Why did the chicken cross the road?'"]
ollama_messages = [f"{ollama_name}: That's quite the topic. "]
claude_messages = [f"{claude_name}: Lets begin our discussion."]


def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]

    for gpt, ollama_msg, claude in zip(gpt_messages, ollama_messages, claude_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": ollama_msg})
        messages.append({"role": "user", "content": claude})

    response = ollama.chat.completions.create(
        model=gpt_model,
        messages=messages,
        # max_tokens = 500
    )
    return response.choices[0].message.content.strip()


# %%
def call_ollama():
    messages = [{"role": "system", "content": ollama_system}]

    for gpt, ollama_msg, claude in zip(gpt_messages, ollama_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": ollama_msg})
        messages.append({"role": "user", "content": claude})

    messages.append({"role": "user", "content": gpt_messages[-1]})

    response = ollama.chat.completions.create(
        model=ollama_model,
        messages=messages
    )
    return response.choices[0].message.content.strip()


# %%
def call_claude():
    # messages = []
    messages = [{"role": "system", "content": claude_system}]

    for gpt, ollama_msg, claude_message in zip(gpt_messages, ollama_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "user", "content": ollama_msg})
        messages.append({"role": "assistant", "content": claude_message})

    messages.append({"role": "user", "content": gpt_messages[-1]})
    messages.append({"role": "user", "content": ollama_messages[-1]})

    response = ollama.chat.completions.create(  # .messages.create(
        model=claude_model,
        # system = claude_system,
        messages=messages,
        # max_tokens = 500
    )
    # return response.content[0].text.strip()
    return response.choices[0].message.content.strip()



if __name__ == "__main__":
    print(f"GPT:\n{gpt_messages[0]}\n")
    print(f"Ollama:\n{ollama_messages[0]}\n")
    print(f"Claude:\n{claude_messages[0]}\n")

    for i in range(5):
        gpt_next = call_gpt()
        gpt_next = gpt_next if gpt_next.startswith(gpt_name) else f"{gpt_name}:" + gpt_next
        print(f"GPT: \n{gpt_next}\n")
        gpt_messages.append(gpt_next) #f"{gpt_name}:" + gpt_next)

        ollama_next = call_ollama()
        ollama_next = ollama_next if ollama_next.startswith(ollama_name) else f"{ollama_name}:" + ollama_next
        print(f"Ollama: \n{ollama_next}\n")
        ollama_messages.append(ollama_next) #f"{ollama_name}:" + ollama_next)

        claude_next = call_claude()
        claude_next = claude_next if claude_next.startswith(claude_name) else f"{claude_name}:" + claude_next
        print(f"Claude: \n{claude_next}\n")
        claude_messages.append(claude_next) #f"{claude_name}:" + claude_next)
