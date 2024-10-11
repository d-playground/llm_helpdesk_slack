import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.middleware.ignoring_self_events import IgnoringSelfEvents
from llama_cpp import Llama

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initialize_slack_app():
    """Initialize the Slack app with environment tokens."""
    return App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )

def initialize_llama_model():
    """Initialize the Llama model based on configuration."""
    model_type = os.environ.get("MODEL_TYPE", "local")
    
    if model_type == "local":
        logger.info("Initializing local Llama model.")
        return Llama(
            model_path="llama-3.2-3b-instruct-q8_0.gguf",
            n_ctx=4096,
            n_threads=12
        )
    elif model_type == "api":
        logger.info("Connecting to API-based Llama model.")
        return ApiLlamaClient(api_key=os.environ.get("API_KEY"))
    else:
        raise ValueError(f"Unsupported MODEL_TYPE: {model_type}")

class ApiLlamaClient:
    """Client for interacting with a Llama API."""
    
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, prompt, max_tokens, stop, echo):
        response = {
            'choices': [{'text': 'API response text'}]
        }
        return response

def log_last_message(event):
    """Log the last message information."""
    global last_message_info
    message_text = event.get('text', '')
    timestamp = event.get('ts', '')
    channel = event.get('channel', '')
    
    last_message_info = {'text': message_text, 'timestamp': timestamp, 'channel': channel}
    logger.info(f"Last message logged: {message_text} at {timestamp} in channel {channel}")


def generate_response(event, thread_id):
    """Generate a response using the Llama model."""
    query = event.get('text', '')
    history = chat_history.get(thread_id, "")
    
    prompt_template = os.environ.get("PROMPT_TEMPLATE", "")
    
    full_prompt = f"""{history}
    Human: {query} {prompt_template}
    AI:"""
    
    output = model(full_prompt, max_tokens=256, stop=["Human:", "\n"], echo=True)
    response = output['choices'][0]['text'].split("AI:")[-1].strip()
    
    chat_history[thread_id] = f"{full_prompt}{response}"
    
    return response

@app.event("message")
def handle_message(event, say):
    """Handle incoming messages and generate responses."""
    log_last_message(event)
    
    logger.debug(f"Received event: {event}")
    
    if event['channel'] == os.environ.get('SLACK_CHANNEL_ID') and "IT" in event["text"]:
        query = event["text"]
        thread_ts = event.get("thread_ts", event["ts"])
        
        logger.info(f"Processing message related to IT support: {query}")
        
        response = generate_response(event, thread_ts)
        say(text=response, thread_ts=thread_ts)
        logger.info(f"Sent response: {response}")
    else:
        logger.info("Message ignored as it is not relevant or not from the target channel.")

@app.error
def global_error_handler(error, body, logger):
    """Handle errors globally."""
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")

def main():
    """Main entry point for running the Slack bot."""
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()

if __name__ == "__main__":
    app = initialize_slack_app()
    model = initialize_llama_model()
    
    # Add middleware to ignore self events
    app.middleware(IgnoringSelfEvents())
    
    # Chat history storage
    chat_history = {}
    
    # Variable to hold the last message info
    last_message_info = None
    
    main()