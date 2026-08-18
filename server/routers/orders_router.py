from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from datetime import datetime
import time

from server.utils.auth_middleware import get_current_user

from src.storage.postgres.manager import pg_manager
from src.storage.postgres.models_order import (
    CropCart,
    CropOrder,
    CropOrderItem
)
from src.storage.postgres.models_crop import CropAgrochemical
from src.storage.postgres.models_business import User



router = APIRouter(
    prefix="/orders",
    tags=["订单"]
)



# 创建订单
@router.post("/create")
async def create_order(
    data: dict,
    current_user: User = Depends(get_current_user)
):

    address_id = data.get("shipping_address_id")

    if not address_id:
        raise HTTPException(
            400,
            "请选择收货地址"
        )


    async with pg_manager.get_async_session_context() as db:


        # 查询购物车

        result = await db.execute(
            select(
                CropCart,
                CropAgrochemical
            )
            .join(
                CropAgrochemical,
                CropCart.product_id ==
                CropAgrochemical.id
            )
            .where(
                CropCart.user_id ==
                current_user.id
            )
        )


        carts = result.all()


        if not carts:
            raise HTTPException(
                400,
                "购物车为空"
            )


        total = 0


        for cart, product in carts:
            total += product.price * cart.quantity



        order = CropOrder(

            order_no=
            "ORD"+str(int(time.time())),

            user_id=current_user.id,

            total_amount=total,

            status="pending",

            shipping_address_id=address_id
        )


        db.add(order)

        await db.flush()



        # 创建订单商品

        for cart, product in carts:


            item = CropOrderItem(

                order_id=order.id,

                product_id=product.id,

                product_name=product.product_name,

                price=product.price,

                quantity=cart.quantity,

                main_image=product.main_image

            )


            db.add(item)



        # 清购物车

        for cart,product in carts:

            await db.delete(cart)



        await db.commit()


        return {

            "order_id":order.id,

            "order_no":order.order_no,

            "total_amount":total,

            "status":"pending"

        }





# 我的订单

@router.get("/list")
async def order_list(
    current_user:User=Depends(get_current_user)
):


    async with pg_manager.get_async_session_context() as db:


        result=await db.execute(

            select(CropOrder)
            .where(
                CropOrder.user_id ==
                current_user.id
            )

        )


        orders=result.scalars().all()


        return [

            {
             "id":o.id,
             "order_no":o.order_no,
             "amount":o.total_amount,
             "status":o.status
            }

            for o in orders

        ]





# 订单详情

@router.get("/{order_id}")
async def order_detail(

    order_id:int,

    current_user:User=Depends(get_current_user)

):


    async with pg_manager.get_async_session_context() as db:


        order=await db.get(
            CropOrder,
            order_id
        )


        if not order or order.user_id!=current_user.id:

            raise HTTPException(
                404,
                "订单不存在"
            )


        result=await db.execute(

            select(CropOrderItem)
            .where(
                CropOrderItem.order_id==
                order_id
            )

        )


        items=result.scalars().all()



        return {


            "order_no":order.order_no,

            "status":order.status,

            "total_amount":order.total_amount,


            "items":[

                {
                 "product_name":i.product_name,
                 "price":i.price,
                 "quantity":i.quantity
                }

                for i in items

            ]

        }