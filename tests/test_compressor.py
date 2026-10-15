import pytest

from link_compressor.compressor import UrlCompressor


def test_simple() -> None:
    url = "https://www.subdomain.domain.com/path/subpath?query=value&key=value#fragment"
    c = UrlCompressor()
    compressed = c.compress(url)
    decompressed = c.decompress(compressed)
    assert url == decompressed


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
