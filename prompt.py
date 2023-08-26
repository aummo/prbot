"""Interface for a GPT Prompts."""
import os
import sys
from dotenv import dotenv_values
from github import Github 
from github import Auth


from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI, ChatAnthropic
import openai 

from llamaapi import LlamaAPI
# Replace 'Your_API_Token' with your actual API token
llama = LlamaAPI('Your_API_Token')

from langchain_experimental.llms import ChatLlamaAPI

llm_llama = ChatLlamaAPI(client=llama)

config = dotenv_values(".env")

try:
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
    os.environ["ANTHROPIC_API_KEY"] = config["ANTHROPIC_API_KEY"]
except:
    pass


SUMMARY_PROMPT = """
Summarize the following files changed in a pull request denoted in backticks submitted by a developer on GitHub, focusing on major modifications, additions, deletions, and any significant updates within the files.
Do not include the file name in the summary and list the summary with bullet points.

```
{diff}
```
"""

def generate_prompt(code_diff, llm, summary_prompt=SUMMARY_PROMPT) -> str:
    """Load the summary yaml"""

    human_prompt = HumanMessagePromptTemplate.from_template(
        summary_prompt)

    prompt_template = ChatPromptTemplate.from_messages(
        [human_prompt])
        
    chain = LLMChain(llm=llm,
                     prompt=prompt_template)

    output = chain.run({"diff": code_diff})
    
    return output 



# pr_diff_example = get_pr_diff("aummo/pierre-review", 1, config["GITHUB_ACCESS_TOKEN"])

# generate_prompt(pr_diff_example)
