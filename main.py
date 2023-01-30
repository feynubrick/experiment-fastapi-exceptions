from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union

app = FastAPI()


@app.get("/")
async def root():
    return "HELLO WORLD!"


@app.get(
    "/error-http-exception",
)
async def http_exception():
    raise HTTPException(
        status_code=500,
        detail={"CUSTOM-ERROR-BODY-KEY": "VALUE"},
        headers={"CUSTOM-HEADER": "VALUE"},
    )


# 위와 같이 하면 자동 생성되는 document에는 반영되지 않는다.
# 에러를 문서에도 명시하려면 어떻게 해야하는가?
# https://fastapi.tiangolo.com/advanced/additional-responses/
class ErrorMessage(BaseModel):
    detail_code: int
    message: str


@app.get(
    "/error-with-jsonresponse",
    responses={500: {"model": ErrorMessage, "description": "CUSTOM DESCRIPTION"}},
)
async def json_response():
    return JSONResponse(
        status_code=500,
        content={"detail_code": 5000, "message": "CUSTOM MESSAGE"},
        headers={"CUSTOM-HEADER": "VALUE"},
    )


class CustomQueryParameter(BaseModel):
    q: str


async def query_parameter_validation_handler(q: Union[str, None] = None):
    if q == None:
        raise HTTPException(
            status_code=400,
            detail={"detail_code": 4000, "message": "q required"},
        )

    if len(q) > 5:
        raise HTTPException(
            status_code=400,
            detail={"detail_code": 4000, "message": "max length of q = 5"},
        )
    return q


@app.get(
    "/query-parameter-error",
    responses={
        400: {"model": ErrorMessage, "description": "CUSTOM DESCRIPTION"},
        422: {"model": None},
    },
)
async def json_response(q: str = Depends(query_parameter_validation_handler)):
    return q


class CustomException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = {"message": "custom exception occurred"}


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(content=exc.detail, status_code=exc.status_code)


@app.get("/custom-exception")
async def custom_exception():
    raise CustomException()
