from dotenv import load_dotenv
import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key is None:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set.")

# api_key = os.getenv("OPEN_AI_KEY")
# if api_key is None:
#     raise ValueError("OPEN_AI_KEY environment variable is not set.")

# model_client = OpenAIChatCompletionClient(
#     base_url= 'https://openrouter.ai/api/v1',
#     model = 'deepseek/deepseek-chat-v3-0324:free',
#     api_key=  api_key,
#     model_info={
#         "family": 'deepseek',
#         "vision" : True,
#         "function_calling": True,
#         "json_output": False
#     }
#     )
def model_client():
    model_client = OpenAIChatCompletionClient(
        base_url='https://openrouter.ai/api/v1',
        api_key=api_key,  # Replace with your real key
        model='deepseek/deepseek-chat',  # ✅ This works with OpenRouter
        model_info={
            "family": "deepseek",
            "vision": False,
            "function_calling": True,
            "json_output": False,
        }
    )
    return model_client

# model_client= OpenAIChatCompletionClient(
#     api_key= api_key,
#     model='gpt-4o'
