"""
Configuration module for Battery Monitor
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BatteryConfig:
    """Configuration class for battery monitoring settings"""
    
    # Battery thresholds
    low_battery_threshold: int = 20
    full_battery_threshold: int = 80
    
    # Monitoring settings
    check_interval: int = 60  # seconds
    
    # Notification settings
    app_name: str = "Battery Monitor"
    enable_notifications: bool = True
    
    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'BatteryConfig':
        """Create configuration from environment variables"""
        return cls(
            low_battery_threshold=int(os.getenv('BAT_LOW_THRESHOLD', 20)),
            full_battery_threshold=int(os.getenv('BAT_FULL_THRESHOLD', 80)),
            check_interval=int(os.getenv('BAT_CHECK_INTERVAL', 60)),
            app_name=os.getenv('BAT_APP_NAME', 'Battery Monitor'),
            enable_notifications=os.getenv('BAT_ENABLE_NOTIFICATIONS', 'true').lower() == 'true',
            log_level=os.getenv('BAT_LOG_LEVEL', 'INFO'),
            log_file=os.getenv('BAT_LOG_FILE')
        )
    
    def validate(self) -> None:
        """Validate configuration values"""
        if not 0 <= self.low_battery_threshold <= 100:
            raise ValueError("low_battery_threshold must be between 0 and 100")
        
        if not 0 <= self.full_battery_threshold <= 100:
            raise ValueError("full_battery_threshold must be between 0 and 100")
        
        if self.low_battery_threshold >= self.full_battery_threshold:
            raise ValueError("low_battery_threshold must be less than full_battery_threshold")
        
        if self.check_interval <= 0:
            raise ValueError("check_interval must be positive")
