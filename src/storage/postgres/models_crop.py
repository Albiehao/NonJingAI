"""Crop Management System 数据模型 - 农资管理相关表"""

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CropCategory(Base):
    """农资分类"""

    __tablename__ = "crop_agrochemical_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(BigInteger, nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="uk_parent_name"),
    )


class CropAgrochemical(Base):
    """农资商品"""

    __tablename__ = "crop_agrochemicals"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id = Column(Integer, nullable=True)
    product_code = Column(String(20), nullable=True)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(50), nullable=True)
    monthly_sales = Column(Integer, server_default=text("0"))
    price = Column(Integer, nullable=True)  # 单位：分，存储为整数避免精度问题
    registration_no = Column(String(50), nullable=True)
    formulation = Column(String(50), nullable=True)
    content_spec = Column(String(50), nullable=True)
    main_image = Column(String(2048), nullable=True)
    description = Column(Text, nullable=True)
    use_crops = Column(String(255), nullable=True)
    usage_method = Column(Text, nullable=True)
    precautions = Column(Text, nullable=True)
    purchase_links = Column(String(255), nullable=True)
    manufacturer = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True)


class CropCrop(Base):
    """农作物基础信息"""

    __tablename__ = "crop_crops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    scientific_name = Column(String(100), nullable=True, unique=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True)


class CropUser(Base):
    """农资系统用户"""

    __tablename__ = "crop_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=True)
    avatar = Column(String(2048), nullable=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), server_default=text("'USER'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class CropUserCrop(Base):
    """用户与农作物关联"""

    __tablename__ = "crop_user_crops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    crop_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True)
