import openai
import gradio as gr

openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def generate_response(history):

    messages = [{"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if bot_msg is not None:
            messages.append({"role": "assistant", "content": bot_msg})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",  
            messages=messages,
            max_tokens=150,
            temperature=0.7,
        )
        bot_response = completion['choices'][0]['message']['content'].strip()
    except openai.error.InvalidRequestError as e:
        print(f"Invalid request: {e}")
        bot_response = "There was an error processing your request."
    except openai.error.APIError as e:
        print(f"API error: {e}")
        bot_response = "There was an issue with the OpenAI API."
    except openai.error.AuthenticationError as e:
        print(f"Authentication error: {e}")
        bot_response = "Authentication failed. Please check your API key."
    except Exception as e:
        print(f"General error: {e}")
        bot_response = "Sorry, something went wrong."

    return bot_response

def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history):
    bot_response = generate_response(history)
    history[-1][1] = bot_response
    return history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(share=True)
