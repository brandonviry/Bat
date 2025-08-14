"""
Notification system for battery monitoring
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from plyer import notification


logger = logging.getLogger(__name__)


class NotificationError(Exception):
    """Exception raised when notification cannot be sent"""
    pass


class NotificationProvider(ABC):
    """Abstract base class for notification providers"""
    
    @abstractmethod
    def send_notification(self, title: str, message: str, timeout: int = 10) -> None:
        """Send a notification with the given title and message"""
        pass


class PlyerNotificationProvider(NotificationProvider):
    """Notification provider using plyer library"""
    
    def __init__(self, app_name: str = "Battery Monitor"):
        self.app_name = app_name
    
    def send_notification(self, title: str, message: str, timeout: int = 10) -> None:
        """
        Send a notification using plyer
        
        Args:
            title: Notification title
            message: Notification message
            timeout: Notification timeout in seconds
            
        Raises:
            NotificationError: If notification cannot be sent
        """
        try:
            notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                timeout=timeout
            )
            logger.info(f"Notification sent: {title} - {message}")
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            raise NotificationError(f"Unable to send notification: {e}")


class LogNotificationProvider(NotificationProvider):
    """Notification provider that logs messages instead of showing notifications"""
    
    def send_notification(self, title: str, message: str, timeout: int = 10) -> None:
        """Log notification instead of showing it"""
        logger.info(f"NOTIFICATION: {title} - {message}")


class NotificationManager:
    """Manager for handling battery notifications"""
    
    def __init__(self, provider: NotificationProvider):
        self.provider = provider
        self._last_notification_type: Optional[str] = None
    
    def notify_low_battery(self, percent: int, time_left: Optional[int] = None) -> None:
        """
        Send low battery notification
        
        Args:
            percent: Current battery percentage
            time_left: Time remaining in seconds (optional)
        """
        if self._last_notification_type == "low":
            logger.debug("Skipping duplicate low battery notification")
            return
        
        title = "Batterie Faible"
        message = f"La batterie est à {percent}% - Veuillez brancher le chargeur!"
        
        if time_left:
            hours, remainder = divmod(time_left, 3600)
            minutes = remainder // 60
            if hours > 0:
                time_str = f"{hours}h {minutes}min"
            else:
                time_str = f"{minutes}min"
            message += f" (Temps restant: {time_str})"
        
        try:
            self.provider.send_notification(title, message)
            self._last_notification_type = "low"
        except NotificationError as e:
            logger.error(f"Failed to send low battery notification: {e}")
    
    def notify_full_battery(self, percent: int) -> None:
        """
        Send full battery notification
        
        Args:
            percent: Current battery percentage
        """
        if self._last_notification_type == "full":
            logger.debug("Skipping duplicate full battery notification")
            return
        
        title = "Batterie Chargée"
        message = f"La batterie est à {percent}% - Débranchez le chargeur pour préserver la batterie!"
        
        try:
            self.provider.send_notification(title, message)
            self._last_notification_type = "full"
        except NotificationError as e:
            logger.error(f"Failed to send full battery notification: {e}")
    
    def notify_charging_started(self, percent: int) -> None:
        """
        Send charging started notification
        
        Args:
            percent: Current battery percentage
        """
        title = "Charge Démarrée"
        message = f"Charge en cours - Batterie à {percent}%"
        
        try:
            self.provider.send_notification(title, message, timeout=5)
            self._last_notification_type = "charging"
        except NotificationError as e:
            logger.error(f"Failed to send charging notification: {e}")
    
    def reset_notification_state(self) -> None:
        """Reset the notification state to allow new notifications"""
        self._last_notification_type = None
        logger.debug("Notification state reset")
