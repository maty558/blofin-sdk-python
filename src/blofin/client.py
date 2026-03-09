import base64
import hmac
import json
import time
from hashlib import sha256
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode
from blofin.exceptions import BlofinAPIException
import logging
from blofin.rest_market import MarketAPI
from blofin.base import BaseClient

import requests
import websockets
import asyncio
import threading


# Inicializácia loggera
logger = logging.getLogger("blofin.client")
logger.setLevel(logging.INFO)


class Client(BaseClient):
    """BloFin API HTTP client for production environment."""
    
    def __init__(
        self,
        apiKey: Optional[str] = None,
        apiSecret: Optional[str] = None,
        passphrase: Optional[str] = None,
        useServerTime: bool = False,
        baseUrl: str = "https://openapi.blofin.com",
        timeout: float = 30.0,
        proxies: Optional[Dict] = None,
        isDemo: bool = False
    ):
        """Initialize the client.
        
        Args:
            apiKey: BloFin API key, required for authenticated endpoints
            apiSecret: BloFin API secret, required for authenticated endpoints
            passphrase: BloFin API passphrase, required for authenticated endpoints
            useServerTime: Whether to use server time for requests
            baseUrl: API base URL, use demo URL for testing
            timeout: Request timeout in seconds
            proxies: Optional proxy configuration for requests
            isDemo: If True, use demo trading endpoints
        """
        if isDemo:
            baseUrl = "https://demo-trading-openapi.blofin.com"
            
        super().__init__(
            apiKey=apiKey,
            apiSecret=apiSecret,
            passphrase=passphrase,
            useServerTime=useServerTime,
            baseUrl=baseUrl,
            timeout=timeout,
            proxies=proxies
        )
        self.is_demo = isDemo

    def get_account_balance(self):
        """
        Fetch the account balance from the API.
        """
        # Simulated response with correct format
        response = {
            "data": {
                "equity": 50000.00,
                "available_balance": 50000.00
            }
        }
        logger.info("API Response for get_account_balance: %s", response)
        return response

    def get_margin_mode(self):
        """
        Fetch the margin mode from the API.
        """
        # Replace with actual API call logic
        return {"margin_mode": "isolated"}

    def get_positions(self):
        """
        Fetch the positions from the API.
        """
        # Replace with actual API call logic
        return {"positions": []}

    def set_margin_mode(self, margin_mode: str) -> dict:
        """Set margin mode for the account.

        Args:
            margin_mode: The margin mode to set (e.g., "isolated" or "cross").

        Returns:
            The API response as a dictionary.
        """
        endpoint = "/api/v1/account/set-margin-mode"
        payload = {"marginMode": margin_mode}  # Updated to camelCase
        return self.post(endpoint, data=payload)  # Opravené volanie na podporovaný argument


class DemoClient(Client):
    """BloFin API HTTP client for demo trading environment."""
    
    def __init__(
        self,
        apiKey: Optional[str] = None,
        apiSecret: Optional[str] = None,
        passphrase: Optional[str] = None,
        useServerTime: bool = False,
        timeout: float = 30.0,
        proxies: Optional[Dict] = None
    ):
        """Initialize demo trading client.
        
        Args:
            apiKey: BloFin API key, required for authenticated endpoints
            apiSecret: BloFin API secret, required for authenticated endpoints
            passphrase: BloFin API passphrase, required for authenticated endpoints
            useServerTime: Whether to use server time for requests
            timeout: Request timeout in seconds
            proxies: Optional proxy configuration for requests
        """
        super().__init__(
            apiKey=apiKey,
            apiSecret=apiSecret,
            passphrase=passphrase,
            useServerTime=useServerTime,
            timeout=timeout,
            proxies=proxies,
            isDemo=True
        )
        self.market_api = MarketAPI(self)  # Add MarketAPI instance

    def getFundingRate(self, instId: Optional[str] = None) -> Dict:
        """Get current funding rate."""
        return self.market_api.getFundingRate(instId=instId)

    def get_candlesticks(
        self,
        instId: str,
        bar: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get candlestick charts data."""
        return self.market_api.getCandlesticks(
            instId=instId, bar=bar, before=before, after=after, limit=limit
        )

    def get_candlesticks(self, instId: str, bar: Optional[str] = None, limit: Optional[int] = None) -> Dict:
        """Get candlestick data."""
        return self.market_api.get_candlesticks(instId=instId, bar=bar, limit=limit)

    def get_tickers(self, instType: str, instId: Optional[str] = None) -> Dict:
        """Get tickers data."""
        return self.market_api.get_tickers(instType=instType, instId=instId)
