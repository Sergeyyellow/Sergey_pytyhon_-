from smartphone import Smartphone

catalog=[
    Smartphone("apple","ip 15", "+79123456789"),
    Smartphone("samsung", "s25", "+79789632145"),
    Smartphone("lg", "g2", "+79428756122"),
    Smartphone("sony", "zflip", "+79564651313"),
    Smartphone("google", "pixel", "+79234567898")
]

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.number}")