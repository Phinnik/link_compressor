class UrlCompressor:
    def __init__(self) -> None:
        pass

    def compress(self, url: str) -> bytes:
        return url.encode()

    def decompress(self, bytes_: bytes) -> str:
        return bytes_.decode()
