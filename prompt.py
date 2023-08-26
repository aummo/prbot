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


llm3 = ChatOpenAI(model_name="gpt-3.5-turbo", 
                  temperature=0.7, 
                  request_timeout=240,
                  max_retries=4,
                  max_tokens=1000,
                  streaming=True
    )

llma = ChatAnthropic() 


# using an access token
auth = Auth.Token(config["GITHUB_ACCESS_TOKEN"])
# Public Web Github
g = Github(auth=auth)

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)

def get_pr_diff(repository_name, pr_number, github_token):
    # Initialize GitHub API client
    auth = Auth.Token(github_token)

    # Public Web Github
    g = Github(auth=auth)
    # g = Github(github_token)
    
    # Get the repository
    repo = g.get_repo(repository_name)
    
    # Get the pull request by number
    pr = repo.get_pull(pr_number)
    
    # Get the diff for the pull request
    diff_content = pr.get_files()[0].patch
    return diff_content

pr_diff_example = get_pr_diff("aummo/pierre-review", 1, config["GITHUB_ACCESS_TOKEN"])


def generate_prompt(code_diff, summary_prompt=SUMMARY_PROMPT, llm=llm3) -> str:
    """Load the summary yaml"""

    # system_prompt = SystemMessagePromptTemplate.from_template(
    #     SUMMARY_PROMPT)

    human_prompt = HumanMessagePromptTemplate.from_template(
        summary_prompt)

    prompt_template = ChatPromptTemplate.from_messages(
        [human_prompt])
        
    chain = LLMChain(llm=llm,
                     prompt=prompt_template)

    output = chain.run({"diff": code_diff})
    
    return output 

generate_prompt(pr_diff_example)



# def generate_comment():
#     """Run the prompt to get PR comment"""
#     pass


# def get_pull_request_info():
#     # Fetch the pull request info from GitHub API
#     # (Replace with actual API calls)
#     return {
#         'id': 1,
#         'diff_url': 'https://api.github.com/repos/owner/repo/pulls/1.diff'
#     }

# def post_comment_to_pr(pr_id, comment):
#     # Post a comment to the pull request using GitHub API
#     # (Replace with actual API calls)
#     api_url = f"https://api.github.com/repos/owner/repo/pulls/{pr_id}/comments"
#     headers = {
#         'Authorization': f"token {os.getenv('GITHUB_TOKEN')}",
#         'Accept': 'application/vnd.github.v3+json'
#     }
#     payload = {
#         'body': comment
#     }
#     response = requests.post(api_url, headers=headers, data=json.dumps(payload))
#     if response.status_code == 201:
#         print(f"Successfully posted comment to PR {pr_id}")

# def main():
#     # Fetch pull request info
#     pr_info = get_pull_request_info()
#     pr_id = pr_info['id']
#     diff_url = pr_info['diff_url']

#     # Get code difference
#     prompt = generate_prompt(diff_url)

#     # Generate comments based on code difference
#     comment = generate_comment(prompt)

#     # Post each comment to the pull request
#     post_comment_to_pr(pr_id, comment)