import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1) Запрос любого типа без параметра method
response = requests.get(url)
print(f"1. GET без параметра: {response.status_code} - {response.text}")

# 2) Запрос не из списка (HEAD)
response = requests.head(url)
print(f"2. HEAD запрос: {response.status_code} - {response.text}")

# 3) Запрос с правильным значением metho
response = requests.post(url, params={"method": "POST"})
print(f"3. POST с method=POST: {response.status_code} - {response.text}")

# 4) Проверка всех сочетаний методов
methods = ["GET", "POST", "PUT", "DELETE"]

for method in methods:
    print(f"4. Проверка для реального метода: {method}")

    for param_method in methods:
        if method == "GET":
            response = requests.request(method, url, params={"method": param_method})
        else:
            response = requests.request(method, url, data={"method": param_method})

        print(f"method={param_method}: {response.status_code} - {response.text}")

        if method == param_method:
            if "Wrong method" in response.text:
                print(f"Совпадение по типу ({method}), но сервер отвечает ошибкой")
        else:
            if "Wrong method" not in response.text and response.status_code == 200:
                print(f"Несовпадение по типу - фактический {method}, а параметр: {param_method}),"
                      f" но сервер отвечает успехом")
