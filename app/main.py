from fastapi import HTTPException
from typing import List
from app import app
from .database import SessionDep, Supplier
from .models import SupplierReq, SupplierRet, DemandReq, TractorDemand

@app.post("/predict/part_supplier")
async def supplier_endpoint(req: SupplierReq, session: SessionDep) -> SupplierRet:
    supplier = session.get(Supplier, 1)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return {
        "suppliers": [
            {
                "expected_delivery": req.need_by_date,
                "expected_amount": 10,
                "supplier_id": 1,
                "supplier_name": supplier.name,
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


@app.post("/predict/tractor_demand")
async def demand_endpoint(req: DemandReq, session: SessionDep) -> List[TractorDemand]:
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
