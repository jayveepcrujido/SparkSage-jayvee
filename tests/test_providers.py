import pytest
import providers
import config

def test_fallback_order(monkeypatch):
    config.AI_PROVIDER = "openai"
    config.FREE_FALLBACK_CHAIN = ["gemini", "groq"]
    
    # Mock providers to all be enabled
    mock_providers = {
        "openai": {"enabled": True},
        "gemini": {"enabled": True},
        "groq": {"enabled": True}
    }
    monkeypatch.setattr(config, "PROVIDERS", mock_providers)
    
    # We need to manually trigger the internal builder if we change config
    order = providers._build_fallback_order()
    
    assert order[0] == "openai"
    assert "gemini" in order
    assert "groq" in order

def test_available_providers(monkeypatch):
    # Mock providers to all be enabled
    mock_providers = {
        "openai": {"enabled": True},
        "gemini": {"enabled": True},
        "groq": {"enabled": True}
    }
    monkeypatch.setattr(config, "PROVIDERS", mock_providers)
    
    # Mock _clients to have gemini and groq
    monkeypatch.setattr(providers, "_clients", {"gemini": True, "groq": True})
    monkeypatch.setattr(providers, "FALLBACK_ORDER", ["gemini", "groq", "openai"])
    
    available = providers.get_available_providers()
    assert "gemini" in available
    assert "groq" in available
    assert "openai" not in available

def test_pricing_calculation():
    # Verify pricing is defined for core providers
    assert "gemini" in config.PROVIDER_PRICING
    assert "openai" in config.PROVIDER_PRICING
    assert len(config.PROVIDER_PRICING["openai"]) == 2 # input, output
