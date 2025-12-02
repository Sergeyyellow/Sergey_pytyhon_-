import math

def square(side):
    area = side * side
    return math.ceil(area)  

side = float(input("Введите длину стороны квадрата: "))
print(f"Площадь равна: {square(side)}")