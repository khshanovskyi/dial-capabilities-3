import uvicorn
from aidial_interceptors_sdk.chat_completion import interceptor_to_chat_completion
from aidial_interceptors_sdk.examples.chat_completion import PirateInterceptor
from aidial_interceptors_sdk.utils._http_client import get_http_client
from aidial_sdk import DIALApp


async def client_factory():
    return get_http_client()


DIAL_URL = "http://localhost:8080"

pirate_interceptor_app = interceptor_to_chat_completion(
    cls=PirateInterceptor,
    dial_url=DIAL_URL,
    client_factory=client_factory,
)

app = DIALApp(
    dial_url=DIAL_URL,
    propagate_auth_headers=True
)
app.add_chat_completion(deployment_name="reply-as-pirate", impl=pirate_interceptor_app)

if __name__ == "__main__":
    uvicorn.run(app, port=5042, host="0.0.0.0", log_level="info")
