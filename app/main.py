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
partOrderPredictor = PartOrderPredictor()

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, session: SessionDep):
    ret = await predict_part_orders(PartOrderReq(), session)
    
    # Group recommendations by month name
    sortRecs = defaultdict(list)
    for rec in ret["recommendations"]:
        sortRecs[month_name[rec.month]].append(rec)
    ctx = {"recs": dict(sortRecs)}

    return templates.TemplateResponse(request, "index.html", ctx)

@app.post("/predict/part_order")
async def predict_part_orders(req: PartOrderReq, session: SessionDep) -> PartOrderRet:
    # Get the current inventory and supplier IDs
    inventory_dict = get_inventory_dict(session)
    supplier_dict = get_supplier_id_dict(session)

    recommendations: List[PartOrder] = []
    max_temp, min_precip, temp_chng, precip_chng, july = 90, 5, 10, 3, 7

    # Predict for the provided part and month
    # If none are provided, predict for each month and part
    for month in ([req.month] if req.month else range(1, 13)):
        for part in ([req.part_serial] if req.part_serial else PartSerials):
            avg_temp = max_temp - temp_chng * abs(july - month) # 30° F in January, 90° F in July
            precipitation = min_precip + precip_chng * abs(july - month) # 23" in January, 5" in July
            
            result = partOrderPredictor.predict(
                month=month,
                part_serial=part,
                current_quantity=inventory_dict.get(part, 0),
                avg_temp=avg_temp,
                precipitation=precipitation
            )

            recommendations.append(PartOrder(
                part_serial=part,
                month=month,
                quantity=result["quantity_to_order"],
                supplier_id=result["supplier_id"],
                supplier_name=supplier_dict.get(result["supplier_id"], "Unknown"),
                confidence=result["confidence"]
            ))

            # Update inventory for the necxt month with the orders
            inventory_dict[part] += result["quantity_to_order"]

    return {"recommendations": recommendations}
