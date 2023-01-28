from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def root():
    return "HELLO WORLD!"


@app.get(
    "/error-http-exception",
)
def http_exception():
    return HTTPException(
        status_code=500,
        detail={"CUSTOM-ERROR-BODY-KEY": "VALUE"},
        headers={"CUSTOM-HEADER": "VALUE"},
    )
