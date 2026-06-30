from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Hệ thống Quản lý Cửa hàng - Soft Delete")

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "is_active": True},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "is_active": True},
    {"id": 3, "code": "SP003", "name": "Monitor", "price": 2500000, "is_active": False}
]

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    
    target_product = None
    
    for p in products:
        if p["id"] == product_id:
            target_product = p
            break 
            
    if target_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    if target_product["is_active"] is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already inactive"
        )
        
    target_product["is_active"] = False
    
    return {
        "message": "Ngừng kinh doanh thành công",
        "data": target_product
    }