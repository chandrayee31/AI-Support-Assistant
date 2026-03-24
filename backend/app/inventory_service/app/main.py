from fastapi import FastAPI
from app.inventory_service.app.inventory_loader import get_remaining_inventory,get_inventory_health

app = FastAPI()

@app.get("/inventory/remaining")
def inventory_remaining(item: str):
    return get_remaining_inventory(item)



@app.get("/inventory/health")
def inventory_health():
    return get_inventory_health()

