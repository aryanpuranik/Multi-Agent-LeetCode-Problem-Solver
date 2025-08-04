from autogen_agentchat.teams import RoundRobinGroupChat
from Agents.ProblemSolverAgent import get_problem_solver_agent
from Agents.CodeExecutorAgent import get_code_executor_agent
from autogen_agentchat.conditions import TextMentionTermination
def get_team():
    problem_solver_agent = get_problem_solver_agent() 
    code_executor_agent,docker = get_code_executor_agent()

    termination_condition = TextMentionTermination("STOP")

    team = RoundRobinGroupChat(
        participants=[problem_solver_agent, code_executor_agent],
        termination_condition=termination_condition,
        max_turns=10,
    )

    return team,docker
