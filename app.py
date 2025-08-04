import streamlit as st
from Teams.dsa_team import get_team as get_dsa_team_and_docker
from configs.docker_utils import start_docker as start_docker_container
from configs.docker_utils import stop_docker as stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio
import time

# Set page config
st.set_page_config(
    page_title="LeetCode Problem Solver",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/microsoft/autogen',
        'Report a bug': 'https://github.com/microsoft/autogen/issues',
        'About': 'Multi-Agent DSA Problem Solver powered by AutoGen'
    }
)

# Custom CSS for a neutral theme that works with both light and dark modes
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    /* Sub header styling */
    .sub-header {
        font-size: 1.2rem;
        opacity: 0.8;
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4F8BF9;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        border: none;
    }
    
    /* Chat container styling */
    .chat-container {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 2rem;
    }
    
    /* Error container */
    .error-container {
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    
    /* Solution container */
    .solution-container {
        border-left: 5px solid #4caf50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    
    /* Remove any borders from containers */
    .element-container, .stButton, .stTextInput, .stTextArea {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.markdown("## About")
    st.info("""
    This app uses multiple AI agents working together to solve your LeetCode problems:
    
    - 🧑‍💻 **Problem Solver Agent**: Analyzes and solves problems in Python Only
    - 🤖 **Code Executor Agent**: Tests and verifies solutions
    
    Developed with AutoGen.
    """)

# Initialize session state for task
if 'task' not in st.session_state:
    st.session_state.task = ''

# Initialize session state for solution visibility
if 'show_solution' not in st.session_state:
    st.session_state.show_solution = False

# Initialize session state for problem description and starter code
if 'problem_description' not in st.session_state:
    st.session_state.problem_description = """Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Example 1:
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5."""

if 'starter_code' not in st.session_state:
    st.session_state.starter_code = """class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        \"\"\"
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        \"\"\"
        # Your code here"""

# Main content
st.markdown("<h1 class='main-header'>Multi-Agent DSA Problem Solver</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Get expert solutions to data structures and algorithms problems using collaborative AI agents</p>", unsafe_allow_html=True)

# Add LeetCode submission info - bigger, centered, and better styled
st.markdown("""
<div style="text-align: center; padding: 20px; margin: 20px 0; border-radius: 10px; background-color: rgba(70, 70, 70, 0.2);">
    <h2 style="margin-bottom: 15px;">📋 LeetCode-Ready Solutions</h2>
    <p style="font-size: 1.2rem; margin-bottom: 10px;">Easily get solutions tailored to LeetCode's exact format.</p>
    <p style="font-size: 1.1rem; margin-bottom: 10px;">Just paste the problem description on the left and the starter code from LeetCode on the right.</p>
    <p style="font-size: 1.1rem;">Our agents will return a solution in Python that fits directly into LeetCode's editor - keeping the function names, class structure, and format exactly as required.</p>
</div>
""", unsafe_allow_html=True)

# Create two separate input areas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Problem Description")
    problem_description = st.text_area("Problem:", 
                                     value=st.session_state.problem_description,
                                     height=300,
                                     placeholder="Paste your problem description here...")
    
    if problem_description != st.session_state.problem_description:
        st.session_state.problem_description = problem_description

with col2:
    st.subheader("Starter Code")
    starter_code = st.text_area("Code:", 
                              value=st.session_state.starter_code,
                              height=300,
                              placeholder="Paste your starter code here...")
    
    if starter_code != st.session_state.starter_code:
        st.session_state.starter_code = starter_code

# Combine both inputs for processing
if 'task' not in st.session_state or st.session_state.task != problem_description + "\n\nStarter code:\n```python\n" + starter_code + "\n```":
    st.session_state.task = problem_description + "\n\nStarter code:\n```python\n" + starter_code + "\n```"

# Add a small gap
st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

# Use columns to create space around the button
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    solve_clicked = st.button("Solve Problem", use_container_width=True)

# Solution area - only created when needed
solution_container = st.empty()

# Fallback solutions for common problems
fallback_solutions = {
    "Write a function to detect a cycle in a linked list": {
        "explanation": """
        To detect a cycle in a linked list, we can use the Floyd's Cycle-Finding Algorithm (also known as "tortoise and hare" algorithm).
        
        The algorithm uses two pointers that move through the list at different speeds:
        1. A slow pointer (tortoise) that moves one step at a time
        2. A fast pointer (hare) that moves two steps at a time
        
        If there is a cycle, the fast pointer will eventually catch up to the slow pointer. If there's no cycle, the fast pointer will reach the end of the list.
        """,
        "code": """
        def has_cycle(head):
            # Edge case: empty list or single node
            if not head or not head.next:
                return False
                
            # Initialize slow and fast pointers
            slow = head
            fast = head
            
            # Traverse the list
            while fast and fast.next:
                # Move slow pointer one step
                slow = slow.next
                # Move fast pointer two steps
                fast = fast.next.next
                
                # If slow and fast pointers meet, there's a cycle
                if slow == fast:
                    return True
                    
            # If we reach here, fast pointer reached the end, so no cycle
            return False
        """,
        "time_complexity": "O(n) where n is the number of nodes in the linked list",
        "space_complexity": "O(1) as we only use two pointers regardless of input size"
    },
    "Write a function to add two numbers": {
        "explanation": """
        This is a simple function that takes two numbers as input and returns their sum.
        """,
        "code": """
        def add_numbers(a, b):
            return a + b
            
        # Example usage
        print(add_numbers(5, 3))  # Output: 8
        print(add_numbers(-1, 1))  # Output: 0
        print(add_numbers(0, 0))  # Output: 0
        """,
        "time_complexity": "O(1) - constant time operation",
        "space_complexity": "O(1) - constant space"
    },
    "Write a function to find the maximum subarray sum": {
        "explanation": """
        This is the classic Kadane's algorithm problem. The algorithm finds the maximum sum of a contiguous subarray within a one-dimensional array of numbers.
        """,
        "code": """
        def max_subarray_sum(arr):
            if not arr:
                return 0
                
            max_so_far = arr[0]
            max_ending_here = arr[0]
            
            for i in range(1, len(arr)):
                # Either extend the previous subarray or start a new one
                max_ending_here = max(arr[i], max_ending_here + arr[i])
                # Update the global maximum
                max_so_far = max(max_so_far, max_ending_here)
                
            return max_so_far
            
        # Example usage
        print(max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # Output: 6 (from [4, -1, 2, 1])
        print(max_subarray_sum([-1, -2, -3, -4]))  # Output: -1
        print(max_subarray_sum([1, 2, 3, 4]))  # Output: 10
        """,
        "time_complexity": "O(n) where n is the length of the array",
        "space_complexity": "O(1) as we only use a few variables"
    },
    "Implement a function to check if a string is a palindrome": {
        "explanation": """
        A palindrome is a string that reads the same backward as forward. The function removes non-alphanumeric characters and converts to lowercase before checking.
        """,
        "code": """
        def is_palindrome(s):
            # Remove non-alphanumeric characters and convert to lowercase
            s = ''.join(char.lower() for char in s if char.isalnum())
            
            # Check if the string equals its reverse
            return s == s[::-1]
            
        # Example usage
        print(is_palindrome("racecar"))  # Output: True
        print(is_palindrome("A man, a plan, a canal: Panama"))  # Output: True
        print(is_palindrome("hello"))  # Output: False
        """,
        "time_complexity": "O(n) where n is the length of the string",
        "space_complexity": "O(n) for storing the cleaned string"
    }
}

async def run(team, docker, task):
    try:
        with st.spinner("Starting Docker container..."):
            await start_docker_container(docker)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        message_count = 0
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                message_count += 1
                progress_value = min(0.9, message_count / 10)  # Cap at 90%
                progress_bar.progress(progress_value)
                status_text.text(f"Processing... ({message_count} messages generated)")
                
                msg = f"{message.source} : {message.content}"
                yield msg
            elif isinstance(message, TaskResult):
                progress_bar.progress(1.0)
                status_text.text("Task completed!")
                msg = f"Stop Reason: {message.stop_reason}"
                yield msg
        
        yield "TASK_COMPLETED"
    except Exception as e:
        error_msg = f"Error: {e}"
        st.error(error_msg)
        yield error_msg
    finally:
        with st.spinner("Cleaning up resources..."):
            await stop_docker_container(docker)

def display_fallback_solution(task, chat_history):
    # Find the closest matching problem
    solution = None
    for key in fallback_solutions:
        if key.lower() in task.lower():
            solution = fallback_solutions[key]
            break
    
    if not solution:
        # If no direct match, use the first solution as default
        solution = fallback_solutions["Write a function to detect a cycle in a linked list"]
    
    with chat_history.container():
        st.markdown("<div class='error-container'>", unsafe_allow_html=True)
        st.warning("⚠️ We encountered an API timeout. Here's a fallback solution:")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='solution-container'>", unsafe_allow_html=True)
        st.subheader("Solution")
        st.markdown(solution["explanation"])
        
        st.subheader("Implementation")
        st.code(solution["code"], language="python")
        
        st.subheader("Complexity Analysis")
        st.markdown(f"**Time Complexity**: {solution['time_complexity']}")
        st.markdown(f"**Space Complexity**: {solution['space_complexity']}")
        st.markdown("</div>", unsafe_allow_html=True)

if solve_clicked:
    # Set session state to show solution
    st.session_state.show_solution = True
    
    # Get the combined task from session state
    task = st.session_state.task
    
    # Create the solution container only when needed
    with solution_container.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        st.subheader("Solution Process")
        st.write("Our agents are working on your problem...")
        
        # Create placeholders for agent messages
        user_placeholder = st.empty()
        solver_placeholder = st.empty()
        executor_placeholder = st.empty()
        
        try:
            with st.spinner("Initializing agents..."):
                team, docker = get_dsa_team_and_docker()
            
            chat_history = st.container()
            
            async def collect_messages():
                user_messages = []
                solver_messages = []
                executor_messages = []
                error_occurred = False
                
                async for msg in run(team, docker, task):
                    if "Error: APITimeoutError" in msg:
                        error_occurred = True
                        with chat_history.chat_message('system', avatar='⚠️'):
                            st.markdown(f"API timeout error occurred. Switching to fallback solution.")
                        display_fallback_solution(task, chat_history)
                        break
                        
                    if msg == "TASK_COMPLETED":
                        st.success("✅ Solution complete! Review the conversation above.")
                        break
                        
                    if isinstance(msg, str):
                        if msg.startswith("user"):
                            user_messages.append(msg)
                            with chat_history.chat_message('user', avatar='👤'):
                                st.markdown(msg)
                        elif msg.startswith('DSA_Problem_Solver_Agent'):
                            solver_messages.append(msg)
                            with chat_history.chat_message('assistant', avatar='🧑‍💻'):
                                st.markdown(msg)
                        elif msg.startswith('CodeExecutorAgent'):
                            executor_messages.append(msg)
                            with chat_history.chat_message('assistant', avatar='🤖'):
                                st.markdown(msg)
                        else:
                            with chat_history.chat_message('system', avatar='🔧'):
                                st.markdown(msg)
                    elif isinstance(msg, TaskResult):
                        with chat_history.chat_message('system', avatar='🚫'):
                            st.markdown(f"Task Completed: {msg.result}")
                
                if not error_occurred and len(user_messages) == 0:
                    # If no messages were generated at all, show fallback
                    with chat_history.chat_message('system', avatar='⚠️'):
                        st.markdown(f"No response received from agents. Showing fallback solution.")
                    display_fallback_solution(task, chat_history)
            
            asyncio.run(collect_messages())
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            chat_history = st.container()
            display_fallback_solution(task, chat_history)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
            