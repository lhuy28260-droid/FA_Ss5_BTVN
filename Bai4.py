from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Hệ thống Quản lý Sản phẩm")

# Cấu trúc dữ liệu sản phẩm gửi từ Client lên
class ProductUpdate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

# Dữ liệu ban đầu đề bài cung cấp
products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000.0, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000.0, "stock": 5}
]

@app.put("/products/{product_id}")
def update_product(product_id: int, payload: ProductUpdate):
    
    # -------------------------------------------------------------
    # RÀNG BUỘC & VALIDATE DỮ LIỆU ĐẦU VÀO (Quy tắc 3, 4, 5)
    # -------------------------------------------------------------
    # Quy tắc 3: name không được rỗng
    # (Loại bỏ khoảng trắng thừa bằng .strip() để kiểm tra chính xác)
    if not payload.name or payload.name.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name cannot be empty"
        )
        
    # Quy tắc 4: price phải lớn hơn 0
    if payload.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0"
        )
        
    # Quy tắc 5: stock phải lớn hơn hoặc bằng 0
    if payload.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock must be greater than or equal to 0"
        )

    # -------------------------------------------------------------
    # KIỂM TRA NGHIỆP VỤ BẰNG VÒNG LẶP CỔ ĐIỂN
    # -------------------------------------------------------------
    
    # Quy tắc 1 / Bẫy 1: Tìm xem product_id có tồn tại trong hệ thống hay không
    target_product = None
    for p in products:
        if p["id"] == product_id:
            target_product = p
            break
            
    if target_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"  # Khớp chính xác với hình ảnh Bẫy 1
        )

    # Quy tắc 2 / Bẫy 2: Kiểm tra xem mã code mới có bị trùng với sản phẩm KHÁC hay không
    is_code_duplicated = False
    for p in products:
        # Nếu trùng mã code và ĐÓ KHÔNG PHẢI là sản phẩm hiện tại chúng ta đang sửa
        if p["code"] == payload.code and p["id"] != product_id:
            is_code_duplicated = True
            break
            
    if is_code_duplicated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product code already exists"  # Khớp chính xác với hình ảnh Bẫy 2
        )

    # -------------------------------------------------------------
    # THỰC HIỆN CẬP NHẬT (Nếu vượt qua tất cả các bẫy)
    # -------------------------------------------------------------
    target_product["code"] = payload.code
    target_product["name"] = payload.name
    target_product["price"] = payload.price
    target_product["stock"] = payload.stock

    # Trả về thông tin sản phẩm sau khi cập nhật thành công
    return target_product