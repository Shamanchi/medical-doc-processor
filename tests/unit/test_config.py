"""Unit tests for config."""
import pytest


class TestConfig:
    def test_settings_load(self):
        from app.core.config import get_settings
        settings = get_settings()
        assert settings.app_name == "Medical Document Processor"
        assert settings.app_version == "0.1.0"