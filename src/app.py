from fastapi import FastAPI
from src.predict import predict_message
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# create the template folder
templates = Jinja2Templates(directory="templates")

class MessageRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={"request": request}
    )

@app.post("/predict")
def predict(request: MessageRequest):
    prediction = predict_message(request.message)
    print("prediction:", prediction)
    return {
        "prediction": int(prediction)

    }
