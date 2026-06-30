from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Hệ thống Quản lý Cửa hàng - Soft Delete")

# Dữ liệu ban đầu đề bài cung cấp (có bổ sung trường is_active)
products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "is_active": True},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "is_active": True},
    {"id": 3, "code": "SP003", "name": "Monitor", "price": 2500000, "is_active": False}
]

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    
    # Dùng biến cờ hiệu để tìm kiếm sản phẩm theo cách cổ điển
    target_product = None
    
    for p in products:
        if p["id"] == product_id:
            target_product = p
            break  # Tìm thấy thì dừng vòng lặp ngay
            
    # Trường hợp 1: product_id không tồn tại trong hệ thống
    if target_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    # Trường hợp 2: Sản phẩm tồn tại nhưng đã ở trạng thái inactive từ trước
    if target_product["is_active"] is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already inactive"
        )
        
    # Trường hợp 3: Sản phẩm tồn tại và đang active -> Tiến hành XÓA MỀM
    target_product["is_active"] = False
    
    # Ràng buộc 5: Response trả về rõ ràng, dễ hiểu
    return {
        "message": "Ngừng kinh doanh thành công",
        "data": target_product
    }