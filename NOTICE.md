# Notices

CYBER SH AGENT includes components from the following third-party projects:

- **llama-cpp-python**: This project utilizes `llama-cpp-python` (https://github.com/abetlen/llama-cpp-python), 
  which is licensed under the MIT License. Copyright (c) 2023 Andrei Betlen.

## Operational Warnings

### AI Agency & Shell Commands
CYBER SH AGENT is designed to execute shell commands on your local machine based on AI reasoning. 
- **RISK:** AI models can sometimes generate unexpected or destructive commands. 
- **PRECAUTION:** Always review actions before confirming. We strongly recommend running this tool inside an isolated environment (such as a Docker container or a dedicated virtual machine) to prevent unauthorized changes to your host system.

### AI Behavior
As an AI-driven tool, the Agent may occasionally exhibit "weird" or repetitive behavior, especially during long sessions or after complex task sequences.
- **TROUBLESHOOTING:** If you notice the agent starting to hallucinate, repeat itself, or behave erratically, please use the `/clear` command to reset the session history and force the agent to start with a fresh, clean context.

Thank you to the open-source community for the tools that make this project possible.
