"""Test Multiple ERDDAP search."""

import sys

import pytest

from erddapy.multiple_server_search import fetch_results, search_servers


@pytest.mark.web
@pytest.mark.vcr()
def test_fetch_results():
    """This search should return results."""
    url = (
        "https://standards.sensors.ioos.us/erddap/search/index.csv?"
        'page=1&itemsPerPage=100000&searchFor="sea_water_temperature"'
    )
    key = "ioos"
    protocol = "tabledap"
    data = fetch_results(url, key, protocol)
    assert data is not None


@pytest.mark.web
@pytest.mark.vcr()
def test_fetch_no_results():
    """This search should return no results."""
    url = (
        "https://standards.sensors.ioos.us/erddap/search/index.csv?page=1&itemsPerPage=100000&searchFor"
        '="incredibly_long_string_that_should_never_match_a_real_dataset" '
    )
    key = "ioos"
    protocol = "tabledap"
    data = fetch_results(url, key, protocol)
    assert data is None


@pytest.mark.web
@pytest.mark.skipif(
    sys.platform in ["win32", "darwin"],
    reason="run only on linux to avoid extra load on the server",
)
def test_search_awesome_erddap_servers_True():
    """Test multiple server search on awesome ERDDAP list parallel=True."""
    df = search_servers(
        query="glider",
        protocol="tabledap",
        parallel=True,
    )
    assert df is not None
    assert not df.empty


@pytest.mark.web
@pytest.mark.skipif(
    sys.platform in ["win32", "darwin"],
    reason="run only on linux to avoid extra load on the server",
)
def test_search_awesome_erddap_servers_False():
    """Test multiple server search on awesome ERDDAP list with parallel=False."""
    df = search_servers(
        query="glider",
        protocol="tabledap",
        parallel=False,
    )
    assert df is not None
    assert not df.empty


@pytest.fixture
@pytest.mark.web
def servers_list():
    """Objects for server search."""
    servers_list = {
        "servers_list": [
            "https://standards.sensors.ioos.us/erddap/",
            "https://gliders.ioos.us/erddap/",
        ],
        "query": "sea_water_temperature",
        "protocol": "tabledap",
    }
    yield servers_list


@pytest.mark.web
@pytest.mark.skipif(
    (sys.platform in ["win32", "darwin"] or sys.version_info < (3, 10)),
    reason="run only on linux and latest to avoid extra load on the server",
)
def test_search_servers_with_a_list_parallel_True(servers_list):
    """
    Check that downloads are made and that serial and parallel results are similar.

    Ideally they should be identical but the servers are live
    and changes from one request to another can happen.

    """
    df = search_servers(
        query=servers_list["query"],
        servers_list=servers_list["servers_list"],
        protocol=servers_list["protocol"],
        parallel=True,
    )

    assert df is not None
    assert not df.empty


@pytest.mark.vcr()
@pytest.mark.web
@pytest.mark.skipif(
    sys.platform in ["win32", "darwin"],
    reason="run only on linux to avoid extra load on the server",
)
def test_search_servers_with_a_list_parallel_False(servers_list):
    """
    Check that downloads are made and that serial and parallel results are similar.

    Ideally they should be identical but the servers are live
    and changes from one request to another can happen.

    """
    df = search_servers(
        query=servers_list["query"],
        servers_list=servers_list["servers_list"],
        protocol=servers_list["protocol"],
        parallel=False,
    )

    assert df is not None
    assert not df.empty
