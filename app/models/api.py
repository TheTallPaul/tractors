from pydantic import BaseModel
from typing import List, Optional

class PartOrderReq(BaseModel):
    month: Optional[int] = None
    part_serial: Optional[str] = None

class PartOrder(BaseModel):
    part_serial: str
    month: int
    quantity: int
    supplier_id: int
    supplier_name: str
    confidence: float

class PartOrderRet(BaseModel):
    recommendations: List[PartOrder]
