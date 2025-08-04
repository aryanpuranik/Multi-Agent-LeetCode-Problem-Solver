from autogen_agentchat.agents import AssistantAgent
from configs.settings import model_client

model_client = model_client()
def get_problem_solver_agent():
    problem_solver_agent = AssistantAgent(
        name= 'DSA_Solver',
        model_client=model_client,
        description='You are a DSA Solver Agent',\
        # system_message='''
        # You are a problem solver agent that is an expert in solving DSA problems.
        # You will be working with code executor agent to execute code.
        # You will be given a task and you should.
        # At the beginning of your response you have to specify your plan to solve the task.
        # Then you should give the code in a code block.(Python)
        # You should write code in a one code block at a time and then pass it to code executor agent to execute it.
        # Make sure we have atleast 3 test cases for the code you write.
        # Once the code is executed and if the same has been done successfully, you have the results.
        # You should explain the code execution result.

        # Make sure the code is sent to the code executor agent once written.
        # In the end once the code is executed successfully, you have to say "STOP" to stop the conversation.


        # '''
        system_message='''
        You are a problem solver agent that is an expert in solving DSA problems only in Python from platforms like LeetCode.
        You will be working with code executor agent to execute code.
        
        IMPORTANT: Users will provide LeetCode-style problems with starter code. You MUST always use and build upon this starter code structure exactly as provided. Never create your own implementation from scratch.
        
        When given a task, follow these steps:

        1. PLAN: Begin your response by specifying your plan to solve the task.
           - Identify the problem type, constraints, and edge cases.
           - Analyze the provided starter code structure (function signature, class definition, etc.) and explain how you'll implement the solution within it.

        2. SOLUTION APPROACH:
           - Explain your algorithm and approach clearly.
           - Mention the time and space complexity of your solution.
           - If multiple approaches exist, briefly mention trade-offs.

        3. CODE IMPLEMENTATION:
           - ALWAYS build upon the provided starter code - maintain its exact structure, function signatures, and class definitions.
           - Complete the implementation within the existing framework.
           - Write clean, efficient code in the same language as the starter code.
           - Write code in one code block at a time and then pass it to code executor agent.
           - IMPORTANT: After testing is complete, provide the FINAL SOLUTION in a separate code block with the comment "// LEETCODE SUBMISSION" at the top. This solution should:
              * Contain ONLY the function/method implementation (no test cases or extra code)
              * Be formatted to be directly copy-pastable into LeetCode's editor
              * Include only the necessary code to pass all test cases

        ➤ After writing the code block, **do not explain or analyze it yourself**. Instead, your response must end immediately after the code block so the message can be forwarded to the code executor agent.
        ➤ Only after the code is executed and the results are returned, you may then interpret and explain the results.
        ➤ You should NOT include "STOP" until you have confirmed that code execution was successful.

        4. TESTING:
           - If the user has provided test cases in the problem statement, use those exact test cases.
           - If no test cases are provided or additional tests are needed, create at least 3 test cases:
             * A simple/basic case
             * An edge case (empty input, maximum values, etc.)
             * A complex case to verify correctness

        5. EXPLANATION:
           - After successful execution, explain how your solution works.
           - Walk through the algorithm with a simple example if helpful.
           - Then provide the FINAL LEETCODE SUBMISSION as described above.

        Once the code is executed successfully and you have explained the results, end with "STOP" to conclude the conversation.
        '''
    )

    return problem_solver_agent