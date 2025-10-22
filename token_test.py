import time
import requests


print("1. Создаем задачу...")
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
response_data = response.json()
token = response_data["token"]
seconds = response_data["seconds"]

print("2. Проверяем статус до завершения задачи")
response_before = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
response_before_data = response_before.json()

if "status" in response_before_data and response_before_data["status"] == "Job is NOT ready":
    print("Получен корректный статус, задача в процессе")
else:
    print("Некорректный статус")

print(f"3. Ожидаем {seconds} секунд")
time.sleep(seconds + 1)

print("4. Проверка статуса после завершения задачи")
response_after = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
response_after_data = response_after.json()

if "status" in response_after_data and response_after_data["status"] == "Job is ready":
    print("Получен корректный статус, задача в завершена")
else:
    print("Некорректный статус")

if "result" in response_after_data:
    print("Поле result присутствует")
else:
    print("Поле result отсутствует")


