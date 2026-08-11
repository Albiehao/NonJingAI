"""PostgreSQL 订单业务数据模型 - 购物车、订单、支付"""

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    text,
)

from sqlalchemy.orm import relationship

# 使用公共 Base，不能自己 declarative_base()
from src.storage.postgres.base import Base


class CropCart(Base):
    """购物车"""

    __tablename__ = "crop_cart"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # 用户
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # 商品
    product_id = Column(
        BigInteger,
        ForeignKey("crop_agrochemicals.id"),
        nullable=False,
        index=True,
    )

    # 数量
    quantity = Column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )


class CropOrder(Base):
    """订单主表"""

    __tablename__ = "crop_orders"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # 订单号
    order_no = Column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )

    # 用户
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # 总金额，单位：分
    total_amount = Column(
        Integer,
        nullable=False,
    )

    # pending 待支付
    # paid 已支付
    # completed 已完成
    # cancelled 已取消
    status = Column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
    )

    # 收货地址
    shipping_address_id = Column(
        Integer,
        ForeignKey("user_addresses.id"),
        nullable=False,
    )

    # 地址快照
    shipping_address = Column(
        JSON,
        nullable=True,
    )

    paid_at = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )


    items = relationship(
        "CropOrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )


    payment_records = relationship(
        "CropPaymentRecord",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class CropOrderItem(Base):
    """订单商品明细"""

    __tablename__ = "crop_order_items"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id = Column(
        Integer,
        ForeignKey("crop_orders.id"),
        nullable=False,
        index=True,
    )

    # 商品ID
    product_id = Column(
        BigInteger,
        nullable=False,
    )

    # 商品名称快照
    product_name = Column(
        String(255),
        nullable=False,
    )

    # 单价，单位：分
    price = Column(
        Integer,
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
    )

    main_image = Column(
        String(2048),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )


    order = relationship(
        "CropOrder",
        back_populates="items",
    )


class CropPaymentRecord(Base):
    """支付记录"""

    __tablename__ = "crop_payment_records"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id = Column(
        Integer,
        ForeignKey("crop_orders.id"),
        nullable=False,
        index=True,
    )

    # 支付金额，单位：分
    amount = Column(
        Integer,
        nullable=False,
    )

    # mock模拟支付
    payment_method = Column(
        String(20),
        nullable=False,
        default="mock",
    )

    # success / failed
    status = Column(
        String(20),
        nullable=False,
        default="success",
    )

    paid_at = Column(
        DateTime,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )


    order = relationship(
        "CropOrder",
        back_populates="payment_records",
    )