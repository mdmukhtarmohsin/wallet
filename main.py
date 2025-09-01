from typing import Union
import uvicorn
from fastapi import FastAPI
from db import Base, engine
from controllers import user_controller
from controllers import wallet_controller
from controllers import transactions_controller
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_controller.router)
app.include_router(wallet_controller.router)
app.include_router(transactions_controller.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000,reload=True)