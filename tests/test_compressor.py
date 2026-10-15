from urllib.parse import urlsplit

import pytest

from link_compressor.compressor import (
    SCHEME_MAX_LENGTH,
    SchemeTooLong,
    _compress_scheme_and_www,
)

# fmt: off
sheme_and_www_tests = (
    ("",                                   0b000, "# 0. no scheme, no www"),
    ("www.",                               0b001, "# 1. no scheme, www"),
    ("http://",                            0b010, "# 2. http, no www"),
    ("http://www.",                        0b011, "# 3. http,  www"),
    ("https://",                           0b100, "# 4. https, no www"),
    ("https://www.",                       0b101, "# 5. https, www"),
    # ("magnet://",              0b110_00000_000_0, "# 6.a. known, no www"),    # TODO: implement # 6.a
    # ("magnet://www",           0b110_00000_000_0, "# 6.b. known, www"),       # TODO: implement # 6.b
    # ("tel://",                 0b110_00000_000_0, "# 6.c. other known"),      # TODO: implement # 6.с
    # ("Tel://",                 0b110_00000_000_0, "# 6.c. known uppercase"),  # TODO: implement # 6.с
    ("zz://",           0b111_01010_1111101000_0, "# 7.a. unknown scheme, no www (zz://)"),
    ("zz://www.",       0b111_01010_1111101000_1, "# 7.b. unknown scheme, www (zz://www)"),
    ("zzz://",    0b111_10000_1001100001110001_0, "# 7.c. other unknown scheme (zzz://)"),
    ("ZZZ://",    0b111_10000_1001100001110001_0, "# 7.d. other unknown scheme uppercase (ZZZ://)"),
)
# fmt: on


@pytest.mark.parametrize(
    ("sheme_and_www", "expected"),
    [(t[0], t[1]) for t in sheme_and_www_tests],
    ids=[t[2] for t in sheme_and_www_tests],
)
def test__compress_scheme_and_subdomain(sheme_and_www: str, expected: int) -> None:
    url = f"{sheme_and_www}example.com"
    parts = urlsplit(url)
    compressed = _compress_scheme_and_www(parts)
    assert compressed == expected


def test__raises_if_scheme_too_long() -> None:
    sheme = "a" * SCHEME_MAX_LENGTH
    url = f"{sheme}://example.com"
    parts = urlsplit(url)
    _compress_scheme_and_www(parts)

    sheme = "a" * (SCHEME_MAX_LENGTH + 1)
    url = f"{sheme}://example.com"
    parts = urlsplit(url)
    with pytest.raises(SchemeTooLong):
        _compress_scheme_and_www(parts)


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
