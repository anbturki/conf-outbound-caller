from dotenv import load_dotenv
from entrypoint import entrypoint
from livekit.agents import WorkerOptions, cli

load_dotenv()

if __name__ == "__main__":
    opts: WorkerOptions = WorkerOptions(entrypoint_fnc=entrypoint)
    cli.run_app(opts)
