# Multi-Agent LeetCode Problem Solver

A powerful tool built using Microsoft Autogen that uses AI agents to solve LeetCode problems with clean, efficient Python solutions.


[![LLM](https://img.shields.io/badge/LLM-OpenAI-black?style=flat-square)](https://openai.com/)
[![Autogen](https://img.shields.io/badge/Framework-Autogen-orange?style=flat-square)](https://github.com/microsoft/autogen)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat-square)](https://streamlit.io/)
[![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square)](https://www.python.org/)
[![Agentic AI](https://img.shields.io/badge/Tech-Agentic_AI-blue?style=flat-square)](https://www.microsoft.com/en-us/research/project/autogen/)
[![Gen AI](https://img.shields.io/badge/Type-Gen_AI-purple?style=flat-square)](https://en.wikipedia.org/wiki/Generative_artificial_intelligence)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)](https://github.com/yourusername/leetcode-problem-solver)

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

### Important Requirements

#### Docker Requirement
The app uses Docker for code execution, so users must:
- Have Docker installed and running
- Have appropriate permissions to use Docker
- Docker socket must be accessible to the application

#### API Keys
The users will need to:
- Have valid API keys (OpenAI API key or Gemini is required)
- Set them up in their environment or a `.env` file

  
1. Clone the repository:
```bash
git clone https://github.com/yourusername/leetcode-problem-solver.git
cd leetcode-problem-solver
```

2. Create and activate a conda environment:
```bash
conda create -n leetcode-solver python=3.9
conda activate leetcode-solver
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```
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

## License

[MIT License](LICENSE)
