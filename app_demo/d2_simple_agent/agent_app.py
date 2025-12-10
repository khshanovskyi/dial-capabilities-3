import os

import uvicorn
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from app_demo.d2_simple_agent.agent import AgentSample
from app_demo.d2_simple_agent.prompts import SYSTEM_PROMPT
from app_demo.d2_simple_agent.tools.base import BaseTool
from app_demo.d2_simple_agent.tools.deployment.essay_generation_tool import EssayGenerationTool
from app_demo.d2_simple_agent.tools.deployment.image_generation_tool import ImageGenerationTool

DIAL_URL = os.getenv('DIAL_URL', "http://localhost:8080")
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME', 'gpt-4o')


class AgentSampleApplication(ChatCompletion):

    def __init__(self):
        self.tools: list[BaseTool] = [
            ImageGenerationTool(endpoint=DIAL_URL),
            EssayGenerationTool(endpoint=DIAL_URL),
        ]

    async def chat_completion(self, request: Request, response: Response) -> None:
        with response.create_single_choice() as choice:
            await AgentSample(
                endpoint=DIAL_URL,
                system_prompt=SYSTEM_PROMPT,
                tools=self.tools
            ).handle_request(
                choice=choice,
                deployment_name=DEPLOYMENT_NAME,
                request=request,
                response=response,
            )


app: DIALApp = DIALApp()
agent_app = AgentSampleApplication()
app.add_chat_completion(deployment_name="agent-sample", impl=agent_app)

if __name__ == "__main__":
    import sys

    if 'pydevd' in sys.modules:
        config = uvicorn.Config(app, port=5030, host="0.0.0.0", log_level="info")
        server = uvicorn.Server(config)
        import asyncio

        asyncio.run(server.serve())
    else:
        uvicorn.run(app, port=5030, host="0.0.0.0", log_level="info")
