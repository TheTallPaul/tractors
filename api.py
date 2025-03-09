from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI()

class SupplierReq(BaseModel):
    order_date: Optional[datetime] = datetime.now()
    part_id: int
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


@app.post("/predict/part_supplier")
async def supplier_endpoint(req: SupplierReq) -> SupplierRet:
    return {
        "suppliers": [
            {
                "expected_delivery": req.need_by_date,
                "expected_amount": 10,
                "supplier_id": 1,
                "supplier_name": "Supplier 1",
                "confidence": 0.9
            },
            {
                "expected_delivery": req.need_by_date,
                "expected_amount": 10,
                "supplier_id": 2,
                "supplier_name": "Supplier 2",
                "confidence": 0.8
            }
        ],
        "recomended_supplier_id": 1,
        "confidence": 0.39
    }

class DemandReq(BaseModel):
    date_start: datetime
    date_end: datetime
    region_id: Optional[int] = None

class TractorDemand(BaseModel):
    tractor_id: int
    amount: int
    confidence: float

@app.post("/predict/tractor_demand")
async def demand_endpoint(req: DemandReq) -> List[TractorDemand]:
    return [
        {
            "tractor_id": 1,
            "amount": 10,
            "confidence": 0.9
        },
        {
            "tractor_id": 2,
            "amount": 10,
            "confidence": 0.8
        }
    ]
