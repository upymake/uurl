import pytest
from uurl.host import Host
from uurl.port import HttpPort, Port
from uurl.protocol import HttpProtocol, HttpsProtocol, Protocol
from tests.markers import unit

pytestmark = unit

_host: str = 'example.com'
_http_host: str = f'http://{_host}'
_https_host: str = f'https://{_host}'


@pytest.fixture
def host() -> Host:
    yield Host(_host)


@pytest.fixture
def port() -> Port:
    yield HttpPort()


def test_host_value(host: Host) -> None:
    assert host.value() == _host


def test_host_value_with_port(host: Host, port: Port) -> None:
    assert host.value_with_port(port) == f'{_host}:{port.value()}'


@pytest.mark.parametrize(
    'host_input, protocol, outcome',
    (
        (Host(_http_host), HttpProtocol(), True),
        (Host(_https_host), HttpsProtocol(), True),
        (Host(_host), HttpProtocol(), False),
    ),
)
def test_host_begin_with_protocol(host_input: Host, protocol: Protocol, outcome: bool) -> None:
    assert host_input.begin_with_protocol(protocol) is outcome
