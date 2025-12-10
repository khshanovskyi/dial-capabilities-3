import uvicorn
from aidial_interceptors_sdk.chat_completion import interceptor_to_chat_completion
from aidial_interceptors_sdk.chat_completion.base import ChatCompletionInterceptor
from aidial_interceptors_sdk.utils._http_client import get_http_client
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import Stage
from typing_extensions import override


class PrePostInterceptorSample(ChatCompletionInterceptor):

    @override
    async def on_stream_start(self) -> None:
        with Stage(self.response._queue,
                   0,
                   0,
                   "Greeting Stage",
                   ) as stage:
            stage.append_content("Hi, from Greeting Stage👋")

    @override
    async def on_stream_end(self) -> None:
        with Stage(self.response._queue,
                   0,
                   1,
                   "Goodbye Stage",
                   ) as stage:
            stage.append_content("Goodbye, from Goodbye Stage👋")


async def client_factory():
    return get_http_client()


DIAL_URL = "http://localhost:8080"

pre_post_interceptor_app = interceptor_to_chat_completion(
    cls=PrePostInterceptorSample,
    dial_url=DIAL_URL,
    client_factory=client_factory,
)

app = DIALApp(
    dial_url=DIAL_URL,
    propagate_auth_headers=True,
)
app.add_chat_completion(deployment_name="pre-post-interceptor", impl=pre_post_interceptor_app)

if __name__ == "__main__":
    import sys

    if 'pydevd' in sys.modules:
        config = uvicorn.Config(app, port=5041, host="0.0.0.0", log_level="info")
        server = uvicorn.Server(config)
        import asyncio

        asyncio.run(server.serve())
    else:
        uvicorn.run(app, port=5041, host="0.0.0.0")
