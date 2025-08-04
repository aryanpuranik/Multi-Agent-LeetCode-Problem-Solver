
async def start_docker(docker):
    print("Docker Starting")
    await docker.start()

async def stop_docker(docker):
    print("Docker Stopped.")
    await docker.stop()
