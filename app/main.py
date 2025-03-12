from fastapi import Request
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app import app
from calendar import month_name
from collections import defaultdict
from .database import SessionDep, PartSerials
from .models import PartOrderReq, PartOrder, PartOrderRet
from .learning import PartOrderPredictor
from .domain import get_supplier_id_dict, get_inventory_dict

templates = Jinja2Templates(directory="app/web/templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, session: SessionDep):
    ret = await predict_part_orders(PartOrderReq(), session)
    
    sortRecs = defaultdict(list)
    for rec in ret["recommendations"]:
        sortRecs[month_name[rec.month]].append(rec)

    ctx = {"recs": dict(sortRecs)}

    return templates.TemplateResponse(request, "index.html", ctx)

partOrderPredictor = PartOrderPredictor()

@app.post("/predict/part_order")
async def predict_part_orders(req: PartOrderReq, session: SessionDep) -> PartOrderRet:
    months = [req.month] if req.month else range(1, 13)
    parts = [req.part_serial] if req.part_serial else PartSerials

    inventoryDict = get_inventory_dict(session)
    supplierDict = get_supplier_id_dict(session)

    recommendations: List[PartOrder] = []
    for month in months:
        for part in parts:
            result = partOrderPredictor.predict(
                month=month,
                part_serial=part,
                current_quantity=inventoryDict.get(part, 0),
                avg_temp=90 - 10 * abs(7 - month),   # 30° F in January, 90° F in July
                precipitation=5 + 3 * abs(7 - month) # 23" in January, 5" in July
            )
            recommendation = PartOrder(
                part_serial=part,
                month=month,
                quantity=result["quantity_to_order"],
                supplier_id=result["supplier_id"],
                supplier_name=supplierDict.get(result["supplier_id"], "Unknown"),
                confidence=result["confidence"]
            )
            inventoryDict[part] += result["quantity_to_order"]
            recommendations.append(recommendation)

    return {
        "recommendations": recommendations
    }
