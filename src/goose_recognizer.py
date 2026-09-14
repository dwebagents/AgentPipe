import sys

# Скрипт автоматического распознавания значения Goose
# Логика: поиск и анализ данных, похожих на "Goose value"

def recognize_goose_value(data):
    # Упрощенная эвристика: ищем в данных ключи или значения, связанные с 'goose'
    found_values = {}
    for key, value in data.items():
        if 'goose' in str(key).lower() or 'goose' in str(value).lower():
            found_values[key] = value
    return found_values

# Пример тестового вызова (для верификации)
test_data = {"goose_price": 500, "banana_price": 10, "goose_status": "gold"}
print(f"Recognized: {recognize_goose_value(test_data)}")
