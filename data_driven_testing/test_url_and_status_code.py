def test_status_code(base_url, status_code, request_method):
    response = request_method(base_url)
    assert response.status_code == status_code
