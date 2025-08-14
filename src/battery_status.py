"""
Battery status monitoring module
"""

import logging
from dataclasses import dataclass
from typing import Optional
import psutil


logger = logging.getLogger(__name__)


@dataclass
class BatteryInfo:
    """Data class representing battery information"""
    percent: int
    is_plugged: bool
    time_left: Optional[int] = None  # seconds remaining
    
    @property
    def is_charging(self) -> bool:
        """Check if battery is currently charging"""
        return self.is_plugged and self.percent < 100


class BatteryStatusError(Exception):
    """Exception raised when battery status cannot be determined"""
    pass


class BatteryStatusMonitor:
    """Monitor for battery status using psutil"""
    
    def __init__(self):
        self._last_status: Optional[BatteryInfo] = None
    
    def get_battery_info(self) -> BatteryInfo:
        """
        Get current battery information
        
        Returns:
            BatteryInfo: Current battery status
            
        Raises:
            BatteryStatusError: If battery information cannot be retrieved
        """
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                raise BatteryStatusError("No battery found on this system")
            
            # Convert time_left from seconds to int, handle None case
            time_left = None
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                time_left = int(battery.secsleft)
            
            battery_info = BatteryInfo(
                percent=int(battery.percent),
                is_plugged=battery.power_plugged,
                time_left=time_left
            )
            
            logger.debug(f"Battery status: {battery_info.percent}%, plugged: {battery_info.is_plugged}")
            
            self._last_status = battery_info
            return battery_info
            
        except Exception as e:
            logger.error(f"Failed to get battery information: {e}")
            raise BatteryStatusError(f"Unable to retrieve battery status: {e}")
    
    @property
    def last_status(self) -> Optional[BatteryInfo]:
        """Get the last retrieved battery status"""
        return self._last_status
    
    def has_status_changed(self, current_status: BatteryInfo, threshold: int = 1) -> bool:
        """
        Check if battery status has significantly changed
        
        Args:
            current_status: Current battery information
            threshold: Minimum percentage change to consider significant
            
        Returns:
            bool: True if status has changed significantly
        """
        if self._last_status is None:
            return True
        
        percent_change = abs(current_status.percent - self._last_status.percent)
        plug_change = current_status.is_plugged != self._last_status.is_plugged
        
        return percent_change >= threshold or plug_change
