<img src="../../images/mubble_logo.png" alt="Mubble logo" width="50%" height="50%">

# Keyboards (Ukrainian 🇺🇦)
Цей приклад створений для того, щоб показати як працювати з **клавіатурами** в **Mubble**

* Класи `InlineKeyboard` та `InlineButton` потрібно для того, щоб ви могли робити Inline-клавіатуру _(Inline - клавіатури, які прикріплені до повідомлень)_
* Класи `CallbackData` та `CallbackDataMarkup` потрібні для того, щоб ви могли хендлити _(оброблювати)_ `callback_data`, яке ви написали у кнопці, це щось по типу правил `Text` та `Markup` у звичайних повідомленнях.
* Далі ми створюємо клас `Keyboard`, в якому ми просто сгрупували наші клавіатури. За допомогою `.add()` ми додаємо кнопку, а за допомогою `.row()` робимо рядок.
* Ми робимо обробник команди `/start`, де йому відправляється текст, а у параметр `reply_markup` ми вказуємо нашу клавіатуру з фруктами.
* У `@bot.on.callback_query` ми можемо вказувати наші правила через бінарні оператори _(| - або; & - та/і; ~ - не...)_. За допомогою `CallbackData` ми можемо "реагувати" на звичайний `callback_data`, як на звичайний текст.
<br>
Ми бачимо, що за домомогою `cq: CallbackQuery` ми можемо зробити `.answer`, `.edit_text` та `cq.ctx_api.send_message`. Що ж це означає?
<br><br>
`cq.answer` робить alert у Telegram, тобто вилізає віконечко з вашим надписом.
<br>
`cq.edit_text` робить редагує повідомлення, на якому ви натиснули на кнопку клавіатури.
<br>
`cq.ctx_api.send_message` робить звичайну відправку повідомлення за допомогою контекстного API, тобто ми напряму вказуємо, що ми хочемо відправити повідомлення саме через цей метод Telegram Bot API. В середині `ctx_api` є дуже багато методів, якими ви можете скористатись.
* Далі ми вказали `CallbackDataMarkup`, це аналогічно звичайному `Markup`, в який ви можете писати свої "патерни" _(шаблони)_. Після чого по нашому шаблону у параметр `number` буде передаватись інформація з повідомлення і далі відправка.
* Далі йде реакція на `callback_data` - `back`, яке по факту робить те саме, що й команда `/start`, але воно редагує наше повідомлення та показує "підказку/алерт".

## Приклад коду для відправки зображення
```python
from mubble import Token, API, Mubble, CallbackQuery, Message
from mubble.tools import InlineKeyboard, InlineButton
from mubble.rules import StartCommand, CallbackData, CallbackDataMarkup

api = API(Token.from_env())
bot = Mubble(api)


class Keyboard:
    fruits = (
        InlineKeyboard()
        .add(InlineButton("🍌 Banana", callback_data="banana"))
        .add(InlineButton("🍍 Pineapple", callback_data="pineapple"))
        .add(InlineButton("🍎 Apple", callback_data="apple"))
        .row()
        .add(InlineButton("1️⃣ One", callback_data="number/1"))
        .add(InlineButton("2️⃣ Two", callback_data="number/2"))
    ).get_markup()

    back = (
        InlineKeyboard()
        .add(InlineButton("⬅️ Back", callback_data="back"))
        .get_markup()
    )

emojis = {"banana": "🍌", "pineapple": "🍍", "apple": "🍎"}


@bot.on.message(StartCommand())
async def start_handler(message: Message):
    await message.answer("🥩 Choose your action", reply_markup=Keyboard.fruits)


@bot.on.callback_query(
        CallbackData("banana")
        | CallbackData("pineapple")
        | CallbackData("apple")
)
async def fruits_handler(cq: CallbackQuery):
    emoji = emojis[cq.data.unwrap()]
    await cq.answer(f"You've choosen {emoji}")
    await cq.ctx_api.send_message(
        cq.message.unwrap().chat.id, f"Eat lots of {emoji}, it's healthy!"
    )
    await cq.edit_text(f"{emoji} is great choice!", reply_markup=Keyboard.back)


@bot.on.callback_query(CallbackDataMarkup("number/<number:int>"))
async def number_handler(cq: CallbackQuery, number: int):
    await cq.edit_text(f"You've choosen number {number}!", reply_markup=Keyboard.back)


@bot.on.callback_query(CallbackData("back"))
async def back_handler(cq: CallbackQuery):
    await cq.answer("You've returned to the menu.")
    await cq.edit_text("🥩 Choose your action", reply_markup=Keyboard.fruits)


bot.run_forever()

```

## Приклади використання
<img src="../../images/keyboards_1.jpg" alt="Mubble logo" width="50%" height="50%">
<img src="../../images/keyboards_2.jpg" alt="Mubble logo" width="50%" height="50%">
<img src="../../images/keyboards_3.jpg" alt="Mubble logo" width="50%" height="50%">
<img src="../../images/keyboards_4.jpg" alt="Mubble logo" width="50%" height="50%">
