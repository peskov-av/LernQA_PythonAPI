import requests


class TestHeadersMethod:
    def test_headers_method_request(self):

        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert response.status_code == 200

        headers = response.headers

        assert len(headers) > 0, "headers отсутствуют в ответе"

        print("Заголовки ответа:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        expected_headers = {
            "Content-Type": "application/json",
            "Content-Length": "15",
            "Connection": "keep-alive",
            "Keep-Alive": "timeout=10",
            "Server": "Apache",
            "x-secret-homework-header": "Some secret value",
            "Cache-Control": "max-age=0"
        }

        for header, expected_value in expected_headers.items():
            assert header in response.headers, f"Заголовок {header} отсутствует в ответе"
            actual_value = response.headers.get(header)
            assert actual_value == expected_value, (
                f"Заголовок {header} отличается. "
                f"Ожидалось: {expected_value}, Фактически: {actual_value}"
            )
