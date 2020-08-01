"""The module provides API for Unified Resource Locator (URL) endpoints."""
from punish import AbstractStyle, abstractstyle
from uurl.host import Host
from uurl.path import EmptyPath, Path
from uurl.protocol import HttpProtocol, HttpsProtocol, Protocol


class Address(AbstractStyle):
    """The class represents an interface of an address."""

    @abstractstyle
    def matcher(self) -> str:
        """Returns a path of the URL."""
        pass

    @abstractstyle
    def host(self) -> str:
        """Returns a domain name (host)."""
        pass

    @abstractstyle
    def __str__(self) -> str:
        """Returns address as a string."""
        pass


class Url(Address):
    """The class represents regular WEB URL item."""

    def __init__(self, host: Host, protocol: Protocol, path: Path = EmptyPath()) -> None:
        self._host = host
        self._path = path
        self._protocol = protocol

    def matcher(self) -> str:
        """Returns a path of the URL."""
        return self._path.compose()

    def host(self) -> str:
        """Returns a domain name (host)."""
        return self._host.value()

    def __str__(self) -> str:
        """Returns address as a string."""
        if self._host.begin_with_protocol(self._protocol):
            return self._host.value_with_port(self._protocol.port())
        return (
            f'{self._protocol.value()}://{self._host.value_with_port(self._protocol.port())}/'
            f'{self._path.compose()}'
        )


class HttpUrl(Address):
    """The class represents HTTP WEB URL item."""

    def __init__(self, host: Host, path: Path = EmptyPath()) -> None:
        self._http: Url = Url(host, protocol=HttpProtocol(), path=path)

    def matcher(self) -> str:
        """Returns a path of the HTTP URL."""
        return self._http.matcher()

    def host(self) -> str:
        """Returns a domain name (host)."""
        return self._http.host()

    def __str__(self) -> str:
        """Returns address as a string."""
        return str(self._http)


class HttpsUrl(Address):
    """The class represents HTTPS WEB URL item."""

    def __init__(self, host: Host, path: Path = EmptyPath()) -> None:
        self._https: Url = Url(host, protocol=HttpsProtocol(), path=path)

    def matcher(self) -> str:
        """Returns a path of the HTTPS URL."""
        return self._https.matcher()

    def host(self) -> str:
        """Returns a domain name (host)."""
        return self._https.host()

    def __str__(self) -> str:
        """Returns address as a string."""
        return str(self._https)
