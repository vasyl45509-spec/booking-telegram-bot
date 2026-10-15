# def check_age(age):
#     if age >= 18:
#         return "Доступ дозволено ✅"
#     else:
#         return "Доступ заборонено ❌"
# print(check_age(16))
# print(check_age(20))

# Наша база даних замовлень за сьогодні
orders_list = [
    {"id": 1, "amount": 500, "status": "paid"},
    {"id": 2, "amount": 1200, "status": "pending"},  # Очікує оплати (не рахуємо!)
    {"id": 3, "amount": 350, "status": "paid"},
    {"id": 4, "amount": 2000, "status": "paid"}
]


# 1. Оголошуємо функцію
def calculate_earnings(orders):
    total = 0

    # 2. Пишемо цикл для перебору замовлень
    for order in orders:
        # 3. Перевіряємо, чи замовлення оплачене
        if order["status"] == "paid":
            # 4. Додаємо суму до total (пам'ятаєш лайфхак += ?)
            total += order ["amount"]

    return total


# 5. Викликаємо функцію і передаємо туди наш список orders_list
final_earnings = calculate_earnings(orders_list)

print(f"💰 Загальний заробіток за день: {final_earnings} грн.")
