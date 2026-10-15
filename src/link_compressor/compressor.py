from string import ascii_lowercase, digits
from urllib.parse import SplitResult, urlsplit

# https://www.rfc-editor.org/info/rfc3986/#section-3.1
SHEME_ALPHABET = ascii_lowercase + digits + "+-."
UNKNOWN_SCHEME_BIT_LENGTH = 5
SCHEME_MAX_LENGTH = 2**UNKNOWN_SCHEME_BIT_LENGTH - 1


class URICompressorException(Exception): ...


class SchemeTooLong(URICompressorException): ...


def _encode_alphabet(s: str, alphabet: str) -> int:
    result = 0

    for char in s.lower():
        result = result * len(alphabet) + alphabet.index(char)
    return result


def _compress_scheme_and_www(parts: SplitResult) -> int:
    www = parts.netloc.startswith("www.") or (
        not parts.netloc and parts.path.startswith("www.")
    )

    scheme = {"": 0, "http": 1, "https": 2}.get(parts.scheme)
    if scheme is not None:
        return (scheme << 1) | int(www)

    # TODO: Use 0b110 marker for encoding one of the registered schemes from
    # https://www.iana.org/assignments/uri-schemes
    if len(parts.scheme) > SCHEME_MAX_LENGTH:
        msg = f"{parts.scheme} is too long. Expected it to be <= {SCHEME_MAX_LENGTH}"
        raise SchemeTooLong(msg)

    encoded = _encode_alphabet(parts.scheme, SHEME_ALPHABET)
    length = encoded.bit_length()
    return (
        (0b111 << (UNKNOWN_SCHEME_BIT_LENGTH + length + 1))
        | (length << (length + 1))
        | (encoded << 1)
        | int(www)
    )


class UrlCompressor:
    def __init__(self) -> None:
        pass

    def compress(self, url: str) -> bytes:
        parts = urlsplit(url)
        return url.encode()

    def decompress(self, bytes_: bytes) -> str:
        return bytes_.decode()
