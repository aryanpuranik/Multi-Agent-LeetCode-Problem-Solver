# Multi-Agent LeetCode Problem Solver

A powerful tool that uses AI agents to solve LeetCode problems with clean, efficient Python solutions.

## Features

- **Dual Input System**: Separate input areas for problem description and starter code
- **Python Solutions**: Specialized in generating Python solutions for LeetCode problems
- **Collaborative AI Agents**: Uses multiple agents working together:
  - Problem Solver Agent: Analyzes and develops solutions
  - Code Executor Agent: Tests and verifies code
- **LeetCode Format Compatibility**: Solutions maintain the exact function signatures and class structures required by LeetCode
- **Error Handling**: Fallback solutions for common problems if API timeouts occur

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker (for code execution)
- Conda (recommended for environment management)



## Usage

1. Enter your LeetCode problem description in the left text area
2. Paste the starter code from LeetCode in the right text area
3. Click "Solve Problem" to generate a solution
4. The solution will be formatted for direct submission to LeetCode

## Project Structure

- `app.py`: Main Streamlit application
- `Teams/`: Contains team configuration for agent collaboration
- `Agents/`: Contains agent definitions and system messages
- `configs/`: Configuration files for Docker and other settings


