from pegada.models import Evidence


def test_fingerprint_is_stable():
    a = Evidence(title="Exemplo", url="https://example.org", source="teste")
    b = Evidence(title=" exemplo ", url="HTTPS://EXAMPLE.ORG", source="outro")
    assert a.fingerprint == b.fingerprint


def test_to_dict_contains_fingerprint():
    item = Evidence(title="A", url="urn:a", source="x")
    assert len(item.to_dict()["fingerprint"]) == 64
