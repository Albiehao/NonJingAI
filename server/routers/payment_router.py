from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from server.utils.auth_middleware import get_current_user

from src.storage.postgres.manager import pg_manager
from src.storage.postgres.models_order import (
    CropOrder,
    CropPaymentRecord
)

from src.storage.postgres.models_business import User



router=APIRouter(

    prefix="/payment",

    tags=["支付"]

)




@router.post("/pay/{order_id}")
async def pay_order(

    order_id:int,

    current_user:User=Depends(get_current_user)

):


    async with pg_manager.get_async_session_context() as db:



        order=await db.get(
            CropOrder,
            order_id
        )


        if not order:

            raise HTTPException(
                404,
                "订单不存在"
            )


        if order.user_id != current_user.id:

            raise HTTPException(
                403,
                "无权限"
            )



        if order.status=="paid":

            return {
                "message":"订单已支付"
            }



        order.status="paid"

        order.paid_at=datetime.now()



        record=CropPaymentRecord(

            order_id=order.id,

            amount=order.total_amount,

            payment_method="mock",

            status="success",

            paid_at=datetime.now()

        )


        db.add(record)



        await db.commit()



        return {

            "message":"支付成功",

            "order_id":order.id,

            "status":"paid"

        }