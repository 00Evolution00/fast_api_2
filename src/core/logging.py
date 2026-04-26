import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Request
from sqlalchemy import JSON, Boolean, DateTime, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/user_actions.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class UserActionLog(Base):
    """Model for logging user actions."""
    __tablename__ = "user_action_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    resource: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class UserActionLogger:
    """Service for logging user actions."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        resource: Optional[str] = None,
        resource_id: Optional[str] = None,
        request: Optional[Request] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> UserActionLog:
        """Log a user action."""
        
        # Extract request information
        ip_address = None
        user_agent = None
        
        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
        
        # Create log entry
        log_entry = UserActionLog(
            user_id=user_id,
            username=username,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        
        # Save to database
        self.db.add(log_entry)
        await self.db.commit()
        
        # Log to file
        log_message = f"User {username or 'anonymous'} ({user_id or 'N/A'}) performed {action}"
        if resource:
            log_message += f" on {resource}"
        if resource_id:
            log_message += f" (ID: {resource_id})"
        if ip_address:
            log_message += f" from {ip_address}"
        
        logger.info(log_message)
        
        return log_entry
    
    async def get_user_actions(
        self,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 100
    ) -> list[UserActionLog]:
        """Get user actions with optional filters."""
        from sqlalchemy import select, and_
        
        query = select(UserActionLog)
        
        conditions = []
        if user_id:
            conditions.append(UserActionLog.user_id == user_id)
        if username:
            conditions.append(UserActionLog.username == username)
        if action:
            conditions.append(UserActionLog.action == action)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(UserActionLog.timestamp.desc()).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()


# Dependency for getting logger
async def get_user_action_logger(db: AsyncSession) -> UserActionLogger:
    """Get user action logger instance."""
    return UserActionLogger(db)
