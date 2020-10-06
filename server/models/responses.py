from typing import Any, Dict, Union

import orjson
from fastapi.responses import JSONResponse as _JSONResponse
from pydantic.main import BaseModel


class JSONResponse(_JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)


class APIResponse(BaseModel):
    success: bool
    result: Dict[str, Any]


class Success(APIResponse):
    success: bool = True


class Error(APIResponse):
    success: bool = False


class NotFound(Error):
    result: Dict[str, Any] = {"detail": "Not found"}
