from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from server.utils.auth_middleware import get_current_user, get_db
from src.storage.postgres.models_order import CropCart
from src.storage.postgres.models_crop import CropAgrochemical
from src.storage.postgres.models_business import User


router = APIRouter(
    prefix="/cart",
    tags=["购物车"]
)


# =========================
# 获取购物车列表
# =========================
@router.get("/list")
async def get_cart_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    stmt = (
        select(
            CropCart,
            CropAgrochemical
        )
        .join(
            CropAgrochemical,
            CropCart.product_id == CropAgrochemical.id
        )
        .where(
            CropCart.user_id == current_user.id
        )
    )

    result = await db.execute(stmt)

    rows = result.all()

    data = []

    for cart, product in rows:
        data.append(
            {
                "id": cart.id,
                "product_id": product.id,
                "product_name": product.product_name,
                "price": product.price,
                "main_image": product.main_image,
                "quantity": cart.quantity,
                "created_at": cart.created_at,
                "updated_at": cart.updated_at
            }
        )
    return data



# =========================
# 添加购物车
# =========================
@router.post("/add")
async def add_cart(
    body: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    product_id = body.get("product_id")
    quantity = body.get("quantity", 1)


    if not product_id:
        raise HTTPException(
            status_code=400,
            detail="product_id不能为空"
        )


    product = await db.get(
        CropAgrochemical,
        product_id
    )


    if not product:
        raise HTTPException(
            status_code=404,
            detail="商品不存在"
        )


    stmt = select(CropCart).where(
        CropCart.user_id == current_user.id,
        CropCart.product_id == product_id
    )


    result = await db.execute(stmt)

    cart = result.scalar_one_or_none()


    if cart:
        cart.quantity += quantity

    else:

        cart = CropCart(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )

        db.add(cart)


    await db.commit()

    await db.refresh(cart)


    return {
        "id": cart.id,
        "product_id": cart.product_id,
        "quantity": cart.quantity
    }



# =========================
# 修改购物车数量
# =========================
@router.post("/update/{cart_id}")
async def update_cart(
    cart_id: int,
    body: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    quantity = body.get("quantity")


    if quantity is None:
        raise HTTPException(
            status_code=400,
            detail="quantity不能为空"
        )


    cart = await db.get(
        CropCart,
        cart_id
    )


    if not cart:
        raise HTTPException(
            status_code=404,
            detail="购物车不存在"
        )


    if cart.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="无权限操作"
        )


    cart.quantity = quantity


    await db.commit()

    await db.refresh(cart)


    return {
        "id": cart.id,
        "quantity": cart.quantity
    }



# =========================
# 删除购物车商品
# =========================
@router.post("/delete/{cart_id}")
async def delete_cart(
    cart_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    cart = await db.get(
        CropCart,
        cart_id
    )


    if not cart:
        raise HTTPException(
            status_code=404,
            detail="购物车不存在"
        )


    if cart.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="无权限操作"
        )


    await db.delete(cart)

    await db.commit()


    return {
        "message": "删除成功"
    }



# =========================
# 清空购物车
# =========================
@router.post("/clear")
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    stmt = delete(CropCart).where(
        CropCart.user_id == current_user.id
    )


    await db.execute(stmt)

    await db.commit()


    return {
        "message": "购物车已清空"
    }