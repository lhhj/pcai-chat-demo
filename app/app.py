import os
import gradio as gr
from openai import OpenAI

DEFAULT_ENDPOINT = os.environ.get("LLM_ENDPOINT", "")
DEFAULT_API_KEY = os.environ.get("LLM_API_KEY", "")
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "")
SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    "You are a helpful AI assistant running on HPE Private Cloud AI.",
)


def chat(message, history, endpoint, api_key, model):
    if not endpoint or not model:
        yield "Please configure the LLM Endpoint and Model Name above."
        return

    client = OpenAI(base_url=endpoint, api_key=api_key or "none")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    partial = ""
    for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        partial += delta
        yield partial


with gr.Blocks(title="PCAI Chat Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# PCAI Chat Demo\nA simple chat interface for any OpenAI-compatible LLM endpoint on HPE Private Cloud AI.")

    with gr.Accordion("LLM Configuration", open=not bool(DEFAULT_ENDPOINT)):
        endpoint_box = gr.Textbox(
            label="LLM Endpoint (base URL)",
            placeholder="https://mlis.<namespace>.ingress.<cluster>/v1",
            value=DEFAULT_ENDPOINT,
        )
        api_key_box = gr.Textbox(
            label="API Key",
            placeholder="(leave blank if not required)",
            value=DEFAULT_API_KEY,
            type="password",
        )
        model_box = gr.Textbox(
            label="Model Name",
            placeholder="meta-llama/Llama-3.1-8B-Instruct",
            value=DEFAULT_MODEL,
        )

    chatbot = gr.ChatInterface(
        fn=chat,
        additional_inputs=[endpoint_box, api_key_box, model_box],
        chatbot=gr.Chatbot(height=500),
        retry_btn=None,
        undo_btn=None,
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
