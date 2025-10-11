def is_year_leap(year):
    return year % 4 == 0

year = int(input("Введите год для проверки: "))
result = is_year_leap(year)
print(f"год {year}: {result}")