from pydantic import BaseModel, ConfigDict, Field

class ProductCardDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(alias='id')
    name: str = Field(alias='name')
    price: float = Field(alias='price')
    sale_price: float = Field(alias='sale_price')
    rating: float = Field(alias='rating')
    review_count: int = Field(alias='review_count')
