"""
Main battery monitoring service
"""

import logging
import threading
import time
from typing import Optional

from .config import BatteryConfig
from .battery_status import BatteryStatusMonitor, BatteryStatusError, BatteryInfo
from .notifications import NotificationManager, PlyerNotificationProvider, LogNotificationProvider


logger = logging.getLogger(__name__)


class BatteryMonitorService:
    """Main service for monitoring battery status"""
    
    def __init__(self, config: BatteryConfig):
        self.config = config
        self.config.validate()
        
        # Initialize components
        self.battery_monitor = BatteryStatusMonitor()
        
        # Choose notification provider based on config
        if config.enable_notifications:
            notification_provider = PlyerNotificationProvider(config.app_name)
        else:
            notification_provider = LogNotificationProvider()
        
        self.notification_manager = NotificationManager(notification_provider)
        
        # Threading control
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        self._is_running = False
        
        # State tracking
        self._last_plugged_state: Optional[bool] = None
    
    def start(self) -> None:
        """Start the battery monitoring service"""
        if self._is_running:
            logger.warning("Battery monitor is already running")
            return
        
        logger.info("Starting battery monitor service")
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        self._is_running = True
        
        logger.info(f"Battery monitor started with config: "
                   f"low={self.config.low_battery_threshold}%, "
                   f"full={self.config.full_battery_threshold}%, "
                   f"interval={self.config.check_interval}s")
    
    def stop(self) -> None:
        """Stop the battery monitoring service"""
        if not self._is_running:
            logger.warning("Battery monitor is not running")
            return
        
        logger.info("Stopping battery monitor service")
        self._stop_event.set()
        
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)
        
        self._is_running = False
        logger.info("Battery monitor stopped")
    
    def is_running(self) -> bool:
        """Check if the monitoring service is running"""
        return self._is_running
    
    def get_current_status(self) -> Optional[BatteryInfo]:
        """Get the current battery status"""
        try:
            return self.battery_monitor.get_battery_info()
        except BatteryStatusError as e:
            logger.error(f"Failed to get battery status: {e}")
            return None
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        logger.debug("Battery monitoring loop started")
        
        while not self._stop_event.is_set():
            try:
                self._check_battery_status()
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            # Wait for the specified interval or until stop is requested
            self._stop_event.wait(self.config.check_interval)
        
        logger.debug("Battery monitoring loop ended")
    
    def _check_battery_status(self) -> None:
        """Check battery status and send notifications if needed"""
        try:
            battery_info = self.battery_monitor.get_battery_info()
            
            # Check for charging state changes
            self._handle_charging_state_change(battery_info)
            
            # Check for low battery
            if (battery_info.percent <= self.config.low_battery_threshold and 
                not battery_info.is_plugged):
                self.notification_manager.notify_low_battery(
                    battery_info.percent, 
                    battery_info.time_left
                )
            
            # Check for full battery
            elif (battery_info.percent >= self.config.full_battery_threshold and 
                  battery_info.is_plugged):
                self.notification_manager.notify_full_battery(battery_info.percent)
            
            # Reset notification state if battery is in normal range
            elif (self.config.low_battery_threshold < battery_info.percent < self.config.full_battery_threshold):
                self.notification_manager.reset_notification_state()
            
            # Update last plugged state
            self._last_plugged_state = battery_info.is_plugged
            
        except BatteryStatusError as e:
            logger.error(f"Failed to check battery status: {e}")
    
    def _handle_charging_state_change(self, battery_info: BatteryInfo) -> None:
        """Handle changes in charging state"""
        if self._last_plugged_state is None:
            self._last_plugged_state = battery_info.is_plugged
            return
        
        # Notify when charging starts
        if not self._last_plugged_state and battery_info.is_plugged:
            self.notification_manager.notify_charging_started(battery_info.percent)
            logger.info(f"Charging started at {battery_info.percent}%")
        
        # Log when charging stops
        elif self._last_plugged_state and not battery_info.is_plugged:
            logger.info(f"Charging stopped at {battery_info.percent}%")
            self.notification_manager.reset_notification_state()


class BatteryMonitorApp:
    """Application wrapper for the battery monitor service"""
    
    def __init__(self, config: Optional[BatteryConfig] = None):
        self.config = config or BatteryConfig.from_env()
        self.service = BatteryMonitorService(self.config)
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                *([logging.FileHandler(self.config.log_file)] if self.config.log_file else [])
            ]
        )
        
        logger.info(f"Logging configured at {self.config.log_level} level")
    
    def run(self) -> None:
        """Run the battery monitor application"""
        try:
            self.service.start()
            
            # Keep the main thread alive
            while self.service.is_running():
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.service.stop()
    
    def stop(self) -> None:
        """Stop the application"""
        self.service.stop()
