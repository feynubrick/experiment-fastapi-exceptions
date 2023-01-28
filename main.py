from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return "HELLO WORLD!"


@app.get(
    "/error-http-exception",
)
def http_exception():
    raise HTTPException(
        status_code=500,
        detail={"CUSTOM-ERROR-BODY-KEY": "VALUE"},
        headers={"CUSTOM-HEADER": "VALUE"},
    )


# 위와 같이 하면 자동 생성되는 document에는 반영되지 않는다.
# 에러를 문서에도 명시하려면 어떻게 해야하는가?
# https://fastapi.tiangolo.com/advanced/additional-responses/
class ErrorMessage(BaseModel):
    message: str


@app.get("/error-with-jsonresponse", responses={500: {"model": ErrorMessage}})
def json_response():
    return JSONResponse(
        status_code=500,
        content=ErrorMessage(message="Internal Server Error").json(),
        headers={"CUSTOM-HEADER": "VALUE"},
    )
