from pydantic import BaseModel

class ProductInfo(BaseModel):
    product_name: str
    category : str
    price : float