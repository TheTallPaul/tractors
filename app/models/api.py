from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SupplierReq(BaseModel):
    order_date: Optional[datetime] = datetime.now()
    part_serial: str
    amount: int
    need_by_date: datetime

class PartSupplier(BaseModel):
    expected_delivery: datetime
    expected_amount: int
    supplier_id: int
    supplier_name: str
    confidence: float

class SupplierRet(BaseModel):
    suppliers: List[PartSupplier]
    recomended_supplier_id: int
    confidence: float

class DemandReq(BaseModel):
    date_start: datetime
    date_end: datetime
    region_id: Optional[int] = None

class TractorDemand(BaseModel):
    tractor_id: int
    amount: int
    confidence: float
