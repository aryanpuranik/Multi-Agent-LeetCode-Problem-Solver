from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from configs.constants import Word_dir
def get_docker_executor():
    docker = DockerCommandLineCodeExecutor(
        work_dir= Word_dir,
        timeout= 120
    )
    return docker