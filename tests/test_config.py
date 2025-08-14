"""
Tests for configuration module
"""

import os
import pytest
from unittest.mock import patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.config import BatteryConfig


class TestBatteryConfig:
    """Test cases for BatteryConfig class"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = BatteryConfig()
        
        assert config.low_battery_threshold == 20
        assert config.full_battery_threshold == 80
        assert config.check_interval == 60
        assert config.app_name == "Battery Monitor"
        assert config.enable_notifications is True
        assert config.log_level == "INFO"
        assert config.log_file is None
    
    def test_custom_config(self):
        """Test custom configuration values"""
        config = BatteryConfig(
            low_battery_threshold=15,
            full_battery_threshold=85,
            check_interval=30,
            app_name="Custom Monitor",
            enable_notifications=False,
            log_level="DEBUG",
            log_file="test.log"
        )
        
        assert config.low_battery_threshold == 15
        assert config.full_battery_threshold == 85
        assert config.check_interval == 30
        assert config.app_name == "Custom Monitor"
        assert config.enable_notifications is False
        assert config.log_level == "DEBUG"
        assert config.log_file == "test.log"
    
    @patch.dict(os.environ, {
        'BAT_LOW_THRESHOLD': '25',
        'BAT_FULL_THRESHOLD': '90',
        'BAT_CHECK_INTERVAL': '45',
        'BAT_APP_NAME': 'Env Monitor',
        'BAT_ENABLE_NOTIFICATIONS': 'false',
        'BAT_LOG_LEVEL': 'WARNING',
        'BAT_LOG_FILE': 'env.log'
    })
    def test_from_env(self):
        """Test configuration from environment variables"""
        config = BatteryConfig.from_env()
        
        assert config.low_battery_threshold == 25
        assert config.full_battery_threshold == 90
        assert config.check_interval == 45
        assert config.app_name == "Env Monitor"
        assert config.enable_notifications is False
        assert config.log_level == "WARNING"
        assert config.log_file == "env.log"
    
    def test_validate_valid_config(self):
        """Test validation of valid configuration"""
        config = BatteryConfig()
        config.validate()  # Should not raise
    
    def test_validate_invalid_low_threshold(self):
        """Test validation with invalid low threshold"""
        config = BatteryConfig(low_battery_threshold=-5)
        
        with pytest.raises(ValueError, match="low_battery_threshold must be between 0 and 100"):
            config.validate()
        
        config = BatteryConfig(low_battery_threshold=105)
        
        with pytest.raises(ValueError, match="low_battery_threshold must be between 0 and 100"):
            config.validate()
    
    def test_validate_invalid_full_threshold(self):
        """Test validation with invalid full threshold"""
        config = BatteryConfig(full_battery_threshold=-5)
        
        with pytest.raises(ValueError, match="full_battery_threshold must be between 0 and 100"):
            config.validate()
        
        config = BatteryConfig(full_battery_threshold=105)
        
        with pytest.raises(ValueError, match="full_battery_threshold must be between 0 and 100"):
            config.validate()
    
    def test_validate_threshold_order(self):
        """Test validation of threshold order"""
        config = BatteryConfig(low_battery_threshold=80, full_battery_threshold=20)
        
        with pytest.raises(ValueError, match="low_battery_threshold must be less than full_battery_threshold"):
            config.validate()
    
    def test_validate_invalid_interval(self):
        """Test validation with invalid check interval"""
        config = BatteryConfig(check_interval=0)
        
        with pytest.raises(ValueError, match="check_interval must be positive"):
            config.validate()
        
        config = BatteryConfig(check_interval=-10)
        
        with pytest.raises(ValueError, match="check_interval must be positive"):
            config.validate()
