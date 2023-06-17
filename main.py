import platform
from datetime import datetime, timedelta
import aiohttp
import asyncio
import sys


async def get_exchange_rates(date_string):
    
    link = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    full_link = link + date_string

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(full_link) as response:
                result = await response.json()
                return result
        except aiohttp.ClientError as e:
            print(f'Помилка: {e}')
            return None


async def main():
    
    num_days = int(sys.argv[1])  # Задаємо кількість днів, за які хочемо отримати дані
    if num_days > 10:
        print('Не більше, ніж 10 днів.')
        sys.exit(1)

    current_time = datetime.today().date()

    currency_list = []
    for i in range(num_days):
        date_string = (current_time - timedelta(days=i)).strftime('%d.%m.%Y')
        result = await get_exchange_rates(date_string)

        if result is not None:
            exchange_rates = {}
            for item in result['exchangeRate']:
                currency = item['currency']
                if currency in ['USD', 'EUR']:
                    sale_rate = item.get('saleRate', None)
                    purchase_rate = item.get('purchaseRate', None)

                    if sale_rate and purchase_rate:
                        exchange_rates[currency] = {
                            'sale': sale_rate,
                            'purchase': purchase_rate
                        }

            currency_dict = {
                date_string: exchange_rates
            }
            currency_list.append(currency_dict)

    return currency_list


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    result = asyncio.run(main())
    print(result)