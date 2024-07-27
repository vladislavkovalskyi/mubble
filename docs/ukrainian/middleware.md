<img src="../../images/mubble_logo.png" alt="Mubble logo" width="50%" height="50%">

# Middleware (Ukrainian 🇺🇦)
Цей приклад створений для того, щоб показати як працювати з **Middlewares** в **Mubble**

**Для чого Middlewares потрібні?**<br>
Вони можуть бути потрібні, коли вам знадобиться викликати якісь алгоритми **До** _(pre)_, або **Після** _(post)_ ваших хендлерів.<br>
Наприклад: Ви хочете зробити реєстрацію не просто, коли людина пише команду `/start`, а реєстрацію, коли людина вже користується ботом і пише будь-яке повідомлення. Також він може відразу, за допомогою контексту, відправити в хендлер якусь інформацію (наприклад об'єкт самого користувача), щоб в різних хендлерах не робити `CTRL+C/V` отримання даних користувача за допомогою його `Telegram ID`.


* Ми створюємо клас `Middleware`, який успадковується від абстрактного `ABCMiddleware`.<br>
В нашому абстрактному `ABCMiddleware` є функції `pre` та `post`, які ми можемо переписати.<br>
Функція `pre` буде працювати перед тим, як спрацює хендлер, а функція `post` спрацює тоді, коли хендлер вже спрацював.<br>
Коротко: Якщо функція `pre` _(як в нашому прикладі)_ повертає False, то робота хендлера блокується. Якщо вона повертає True, то хендлер продовжує працювати.<br>
`ctx.set("generated_number", number)` - тут ми в контекст встановлюємо ключ `generated_number` _(його ми потім будемо чекати в хендлері)_, а його значенням `number`.

* Далі ми викликаємо наш звичайний декоратор, який реагує на `/number`, але особливість полягає в тому, що наша асинхронна функція якраз приймає наш ключ `generated_number` з хендлера.<br>

#### ⚠️ Будьте уважні. Якщо ви будете брати цей код за основний, то пам'ятайте, що наш `Middleware` блокує роботу будь-яких хендлерів, так як рандом може повернути число `1` !!!

## Приклад коду
В цьому прикладі **Middleware** генерує рандомне число від 1 до 3. Якщо число 1, то
він блокує роботу хендлерів, але якщо число 2 або 3, то він спокійно додає їх в контекст та наш хендлер їх ловить.
```python
import random

from mubble import Token, API, Mubble, ABCMiddleware, Message
from mubble.bot import Context
from mubble.rules import Text

api = API(Token.from_env())
bot = Mubble(api)


class Middleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        number = random.randint(1, 3)
        if number == 1:
            await event.answer(
                "🖥 Hello! I'm middleware!\n"
                f"Generated number is {number}\n"
                "Unfortunately I blocked your handler because it turned out to be number 1."
            )
            return False
        
        await event.answer(
            "🖥 Hello! I'm middleware!\n"
            f"Generated number is {number}\n"
            "Now this context will be available to you in a handler."
        )
        ctx.set("generated_number", number)
        return True
        


@bot.on.message(Text("/number"))
async def number(m: Message, generated_number: int):
    await m.reply(f"🙄 Your number from middleware is {generated_number}")


bot.on.message.middlewares.append(Middleware())
bot.run_forever()

```

## Приклад використання
<img src="../../images/middleware.jpg" alt="Mubble logo" width="50%" height="50%">
