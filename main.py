from typing import List, Union, Dict, Optional

from fastapi import FastAPI, Query, Path, Header, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
import time

from data import products_buyers

app = FastAPI()
time.time()
SECRET = "shhh"

@app.get("/products_buyers/", status_code=status.HTTP_200_OK)
async def return_products_buyers(
    Authorization: Optional[str] = Header(None, description="Bearer token you"),
    Accept: Optional[str] = Header(None, description="data type")):
    if "json" in Accept and Authorization == f"Bearer {SECRET}":
        return JSONResponse(content=products_buyers)
    elif "html" in Accept and Authorization == f"Bearer {SECRET}":
        return HTMLResponse(content=f"<h1>{products_buyers}</h1>")


    return HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@app.delete("/products_buyers/remove_buyer/", status_code=status.HTTP_200_OK)
async def remove_buyer(buyer_name: int):
    if buyer_name:
        buyer = next((user for user in products_buyers if user["id"] == buyer_name), None)
        products_buyers.remove(buyer)
        return HTTPException(status_code=status.HTTP_200_OK, detail=f"Покупця {buyer} видалено")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get("/products_buyers/buyer_name/", status_code=status.HTTP_200_OK)
async def get_user_name(name: str = Query(..., description="Знайти покупця")):
    user = next((user for user in products_buyers if user["Buyer_name"] == name), None)
    if user:
        return JSONResponse(content=user)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/products_buyers/{buyer_name}/")
async def get_buyer(buyer_name: int = Path(..., description="Product Buyer ID")):
    buyer = next((user for user in products_buyers if user["id"] == buyer_name), None)
    if buyer:
        return JSONResponse(content=buyer)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {buyer_name} не знайдено")



if __name__ == "__main__":
    uvicorn.run(app)