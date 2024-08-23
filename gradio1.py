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


custom_css = """
body, html {
    height: 100%;
    margin: 0;
    padding: 0;
}

#chat-container {
    display: flex;
    flex-direction: column;
    height: 100%; /* Adjusted to fit the height of the page */
    color: #fff;
    width: 85%; /* Remaining width for chat container */
}

#chatbox {
    flex-grow: 1;
    overflow-y: auto;
    border: 1px solid #444;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    color: #fff; /* White text */
}

#input-container {
    display: flex;
    margin-top: 10px;
}

#input-box {
    flex-grow: 1;
    padding: 10px;
    border-radius: 5px;
    border: none;
    margin-right: 10px;
    background-color: #444; /* Dark input box */
    color: #fff; /* White text */
}

#clear-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #007BFF; /* Blue button */
    color: white;
    cursor: pointer;
}

#clear-btn:hover {
    background-color: #0056b3; /* Darker blue on hover */
}

.sidebar {
    width: 10%; /* Adjusted to make sidebar narrower */
    background-color: #1f1f1f; /* Sidebar background */
    padding: 20px;
    border-right: 1px solid #444; /* Border color */
    height: 100%; /* Adjusted to fit the height of the page */
    overflow-y: auto;
}

.sidebar h2 {
    margin-bottom: 20px;
    color: #fff; /* White text */
}

.sidebar p {
    color: #aaa; /* Lighter grey text */
}
"""

with gr.Blocks(css=custom_css) as demo:
    with gr.Row():
        with gr.Column(elem_id="sidebar"):
            gr.Markdown("<h2>Chat History</h2>")
            gr.Markdown(value="No chat history yet.")
        
        with gr.Column(elem_id="chat-container", scale=3):
            gr.Markdown("<h1 style='text-align: center; color: #fff;'>Chat with GPT-4</h1>")
            chatbot = gr.Chatbot(elem_id="chatbox")
            with gr.Row(elem_id="input-container"):
                msg = gr.Textbox(placeholder="Type your message here...", elem_id="input-box")
                clear = gr.Button("Clear", elem_id="clear-btn")
                msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                    bot, chatbot, chatbot
                )
                clear.click(lambda: None, None, chatbot, queue=False)


demo.launch(share=True)
