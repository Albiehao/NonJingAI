"""MQTT device ownership bindings for the main business system.

The main system stores only the authenticated user <-> device SN relationship.
MQTT passwords remain owned by the standalone MQTT gateway.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text

from src.storage.postgres.base import Base


class MqttDeviceBinding(Base):
    __tablename__ = "mqtt_device_bindings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sn = Column(String(128), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sn": self.sn,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
