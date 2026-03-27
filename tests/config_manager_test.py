"""Shared pytest fixtures and hooks. Add fixtures here as needed."""


from cfgfw import DefaultConfigManagerFactory
from pathlib import Path

def test_config_manager_factory()->None:
    factory = DefaultConfigManagerFactory()
    config_manager = factory.config_manager
    config = config_manager.load_config(path=Path(__file__).parent / "a.py")
    print(config)
    assert type(config) == dict