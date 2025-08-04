
from autogen_agentchat.agents import CodeExecutorAgent
from configs.docker_executor import get_docker_executor

docker = get_docker_executor()
def get_code_executor_agent():
    code_executor_agent = CodeExecutorAgent(
        name= 'CodeExecutorAgent',
        code_executor=docker,
        system_message='''
        You are a code executor agent that tests and verifies code solutions for DSA problems.
        
        When you receive code from the problem solver agent:
        1. Execute the code with the provided test cases
        2. Verify that the output matches the expected results
        3. If there are any errors or the output doesn't match, provide clear feedback
        4. If the code passes all tests, confirm success and report the results
        
        For LeetCode-style problems:
        - Focus on verifying the solution's correctness, not its formatting
        - Report time and space complexity if possible
        - Highlight any edge cases that might be problematic
        - If the solution is correct but could be optimized, suggest improvements
        
        After testing, return control to the problem solver agent so they can provide the final LeetCode submission.
        '''
    )

    return code_executor_agent, docker

