from sqlmodel import Field, SQLModel
from datetime import date

PartSerials = ["wheels-x77346", "engine-67xsj97", "flashy-bits-85yunb443"]

class Inventory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    part_serial: str = Field(index=True)
    quantity: int = Field()

class Deliveries(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    part_serial: str = Field(index=True)
    quantity: int = Field()
    supplier_id: int = Field(foreign_key="supplier.id")
    delivery_date: date = Field()
    days_after_expected: int = Field()

class Supplier(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()

class Sales(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tractor_id: int = Field(index=True)
    quantity: int = Field()
    region_id: int = Field()
    price: int = Field()
    sales_date: date = Field()

class ConditionsHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conditions_date: date = Field()
    region_id: int = Field()
    temperature: int = Field()
    precipitation: int = Field()

class Tractor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()

class TractorParts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tractor_id: int = Field(foreign_key="tractor.id")
    part_serial: str = Field()
    quantity_required: int = Field()
