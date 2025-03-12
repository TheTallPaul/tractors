from pydantic import BaseModel

class PartOrderRecommendation(BaseModel):
    quantity_to_order: int
    supplier_id: int
    confidence: float
