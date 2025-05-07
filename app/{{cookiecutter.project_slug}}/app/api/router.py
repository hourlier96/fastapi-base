import os
from typing import Dict, List

from fastapi import APIRouter

# Add any path to file containing a router module
ROUTERS_DIRECTORIES: List[str] = ['app/api/routers']

api_router = APIRouter()

@api_router.api_route("/health", methods=['HEAD'], tags=["Health"])
def get_health() -> Dict:
    return {"status": "OK"}


def import_router(router_directory: str, module_name: str):
    # Import the module dynamically
    module = __import__(f"{router_directory}.{module_name}", fromlist=["router"])

    router = getattr(module, "router")

    api_router.include_router(
        router,
        prefix=f"/{module_name}",
        tags=[module_name.capitalize().replace("_", " ")],
    )


for directory in ROUTERS_DIRECTORIES:
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".py") and filename != "__init__.py":
                import_router(directory.replace("/", "."), filename[:-3])
    except FileNotFoundError:
        pass
