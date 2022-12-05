from aiogram import types
from dispatcher import dp
import config
import re
from bot import BotBD

@dp.message_handler(commands='start')
async def start(message: types.Message):
    if(not BotBD.user_exists(message.from_user.id)):
        BotBD.add_user(message.from_user.id)
    await message.bot.send_message(message.from_user.id,'Добро пожаловать!')

@dp.message_handler(commands=('spend','s','earned','e'),commands_prefix='/!')
async def record(message: types.Message):
    cmd_var = (('/spend','/s','!spend','!s'),('/earned','/e','!earned','!e'))
    operation = '-' if message.text.startswith(cmd_var[0]) else '+'
    value = message.text
    for i in cmd_var:
        for j in i:
            value = value.replace(j,'').strip()
    if len(value):
        x = re.findall(r"\d+(?:.\d+)?",value)

        if len(x):
            value = float(x[0].replace(',','.'))

            BotBD.add_record(message.from_user.id,operation,value)

            if operation == '-':
                await message.reply('✅ Запись о расходе успешно внесена!')
            else:
                await message.reply('✅ Запись о доходе успешно внесена')

        else:
            await message.reply('Не удалось определеть сумму')
    else:
        await message.reply('Не введена сумма')

@dp.message_handler(commands=('history','h'),commands_prefix='/!')
async def history(message: types.Message):
    cmd_var = ('/history','/h','!history','!h')
    within_als = {'day':('today','day','сегодня','день'),
    'month':('month','месяц'),
    'year':('year','год')}

    cmd = message.text
    for r in cmd_var:
        cmd = cmd.replace(r,'').strip()
    within = 'day'
    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k
    records = BotBD.get_records(message.from_user.id,within)

    if len(records):
        answer = f'🕘 История операций за {within_als[within][-1]}\n\n'
        for r in records:
            answer += "<b>" + ("➖ Расход" if not r[2] else "➕ Доход") + "</b>"
            answer += f'-{r[3]}'
            answer += f" <i>({r[4]})</i>\n"

        await message.reply(answer)
    else:
        await message.reply('Таких записей не обнаружено')














