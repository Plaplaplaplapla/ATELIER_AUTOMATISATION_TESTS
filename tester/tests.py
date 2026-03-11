from tester.client import request_json

BASE_URL = "https://pokeapi.co/api/v2"


def test_pokemon_detail_contract_ok():
    result = request_json(f"{BASE_URL}/pokemon/pikachu")

    assert result["ok"] is True
    assert result["status_code"] == 200
    assert "application/json" in result["content_type"]

    data = result["json"]
    assert isinstance(data, dict)

    required_fields = ["id", "name", "height", "weight", "abilities", "forms", "is_default"]
    for field in required_fields:
        assert field in data

    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["height"], int)
    assert isinstance(data["weight"], int)
    assert isinstance(data["abilities"], list)
    assert isinstance(data["forms"], list)
    assert isinstance(data["is_default"], bool)


def test_pokemon_list_contract_ok():
    result = request_json(f"{BASE_URL}/pokemon?limit=5&offset=0")

    assert result["ok"] is True
    assert result["status_code"] == 200
    assert "application/json" in result["content_type"]

    data = result["json"]
    assert isinstance(data, dict)

    required_fields = ["count", "next", "previous", "results"]
    for field in required_fields:
        assert field in data

    assert isinstance(data["count"], int)
    assert isinstance(data["results"], list)

    if data["results"]:
        first = data["results"][0]
        assert isinstance(first, dict)
        assert "name" in first
        assert "url" in first
        assert isinstance(first["name"], str)
        assert isinstance(first["url"], str)


def test_invalid_resource_expected_404():
    result = request_json(f"{BASE_URL}/pokemon/not-a-real-pokemon-xyz")

    assert result["ok"] is True
    assert result["status_code"] == 404


def test_latency_is_measured():
    result = request_json(f"{BASE_URL}/pokemon/pikachu")

    assert result["ok"] is True
    assert result["latency_ms"] is not None
    assert isinstance(result["latency_ms"], float)
    assert result["latency_ms"] > 0
