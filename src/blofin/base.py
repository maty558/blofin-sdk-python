class BaseClient:
    """Base class for BloFin API clients."""

    def __init__(
        self,
        apiKey: Optional[str] = None,
        apiSecret: Optional[str] = None,
        passphrase: Optional[str] = None,
        useServerTime: bool = False,
        baseUrl: str = "https://openapi.blofin.com",
        timeout: float = 30.0,
        proxies: Optional[Dict] = None
    ):
        self.API_KEY = apiKey
        self.API_SECRET = apiSecret.encode('utf-8') if apiSecret else None
        self.PASSPHRASE = passphrase
        self.use_server_time = useServerTime
        self.base_url = baseUrl