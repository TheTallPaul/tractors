from sqlmodel import Session
from datetime import timedelta, date
from random import randint, choice

from .schemas import *
from .connection import engine

PartSerials = ["wheels-x77346", "engine-67xsj97", "flashy-bits-85yunb443"]

def fill_db() -> None:
    with Session(engine) as session:
        dbObjects = [
            Inventory(part_serial=PartSerials[0], quantity=10),
            Inventory(part_serial=PartSerials[1], quantity=20),
            Inventory(part_serial=PartSerials[2], quantity=30),
            Supplier(name="Parts-R-Us"),
            Supplier(name="Parts World"),
            Supplier(name="Parting Ways"),
            Supplier(name="Parts Emporium"),
            Supplier(name="Parts Galore"),
            Supplier(name="Parts Palace"),
            Supplier(name="Parts Mart"),
            Supplier(name="Parts Depot"),
            Supplier(name="Parts Place"),
            Supplier(name="Parts Store"),
            Tractor(name="Bigfoot"),
            Tractor(name="Dogman"),
            Tractor(name="Jackalope"),
            TractorParts(tractor_id=1, part_serial=PartSerials[0], quantity_required=6),
            TractorParts(tractor_id=2, part_serial=PartSerials[0], quantity_required=4),
            TractorParts(tractor_id=3, part_serial=PartSerials[0], quantity_required=4),
            TractorParts(tractor_id=1, part_serial=PartSerials[1], quantity_required=4),
            TractorParts(tractor_id=2, part_serial=PartSerials[1], quantity_required=2),
            TractorParts(tractor_id=3, part_serial=PartSerials[1], quantity_required=1),
            TractorParts(tractor_id=1, part_serial=PartSerials[2], quantity_required=300),
            TractorParts(tractor_id=2, part_serial=PartSerials[2], quantity_required=84),
            TractorParts(tractor_id=3, part_serial=PartSerials[2], quantity_required=53),
        ]

        start_date, end_date = date(2021, 1, 1), date(2024, 12, 31)
        while start_date <= end_date:
            for i in range(1, 11):
                dbObjects.append(ConditionsHistory(
                    conditions_date=start_date,
                    region_id=i,
                    temperature=randint(0,100),
                    precipitation=randint(0,5),
                ))
                dbObjects.append(Sales(
                    tractor_id=choice([1,2,3]),
                    quantity=randint(1,10),
                    region_id=i,
                    price=randint(10000,1000000),
                    sales_date=start_date,
                ))
            dbObjects.append(Deliveries(
                part_serial=choice(PartSerials),
                quantity=randint(1,100),
                supplier_id=randint(1,10),
                delivery_date=start_date,
                days_after_expected=randint(-5,5),
            ))
            start_date += timedelta(days=1)
        
        session.bulk_save_objects(dbObjects)
        session.commit()
        print("🌱🌱🌱 Database filled with seed data 🌱🌱🌱")
