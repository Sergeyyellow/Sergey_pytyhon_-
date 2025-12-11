from address import Address
from mailing import Mailing

to_addres = Address("123456", "Monako", "sovkhoznaya", "20", "3")
from_addres = Address("475454", "LA", "lenina", "77", "85")

mailing=Mailing(
    to_address=to_addres,
    from_address=from_addres,
    cost=1400,
    track="UEA121212"
)

print(f"Отправление {mailing.track} из {mailing.from_addres.index},{mailing.from_addres.city}, {mailing.from_addres.street}, {mailing.from_addres.house}, {mailing.from_addres.kv} в {mailing.to_address.index}, {mailing.to_address.city}, {mailing.to_address.street}, {mailing.to_address.house}, {mailing.to_address.kv}. Стоимость {mailing.cost} рублей")