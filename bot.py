import hashlib
import json
from datetime import datetime

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher import filters
import prometheus_client

import messages
import metrics

from consts import TOKEN, DB_FILENAME, CRASH_STORAGE_FILENAME, SALT

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

db = None

with open(DB_FILENAME, "r") as read_file:
    db = json.load(read_file)


metrics.users.set(len(db))
with open(CRASH_STORAGE_FILENAME, "r") as f:
    metrics.storage_records.set(len(f.read().split()))


def update_db():
    with open(DB_FILENAME, "w") as write_file:
        json.dump(db, write_file)
    metrics.users.set(len(db))


@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    await message.answer(messages.WelcomeMessage.format(name=message.from_user.first_name))


def find_for_data(hashed_value: str) -> bool:
    dbFile = None

    try:
        dbFile = open(CRASH_STORAGE_FILENAME, 'r')
    except FileNotFoundError:
        dbFile = open(CRASH_STORAGE_FILENAME, 'w')
        dbFile.close()
        dbFile = open(CRASH_STORAGE_FILENAME, 'r')

    data = dbFile.read().split('\n')
    dbFile.close()

    if (hashed_value in data):
        return True
    return False


def add_data(hashed_value: str) -> None:
    dbFile = open(CRASH_STORAGE_FILENAME, 'a')
    dbFile.write(f"{hashed_value}\n")
    dbFile.close()
    metrics.storage_records.inc()


def update_data(storage: list) -> None:
    dbFile = open(CRASH_STORAGE_FILENAME, 'w')
    dbFile.write("\n".join(storage))
    dbFile.close()
    metrics.storage_records.set(len(storage))


def find_for_pair_and_write_new_pair(aliasA: str, aliasB: str) -> bool:
    hashed_value_to_check = hashlib.sha256(
        f"{aliasB}{aliasA}{SALT}".encode("utf-8")).hexdigest()
    hashed_value_to_write = hashlib.sha256(
        f"{aliasA}{aliasB}{SALT}".encode("utf-8")).hexdigest()

    if (find_for_data(hashed_value_to_check)):
        add_data(hashed_value_to_write)
        return True
    else:
        add_data(hashed_value_to_write)
        return False


async def send_error(message: Message) -> None:
    await message.answer(messages.AliasError)
    metrics.alias_errors.inc()


async def send_error_timeout(message: Message) -> None:
    await message.answer(messages.Throttle)
    metrics.timeout_errors.inc()


def throttle_check(timestamp: float):
    difference = datetime.now() - datetime.fromtimestamp(timestamp)
    return difference.total_seconds() <= 1 * 24 * 60 * 60


@dp.message_handler(filters.Text(startswith='@'))
async def alias_handler(message: Message) -> None:
    metrics.match_attempt.inc()

    from_user_alias = message.from_user.username.lower()
    crash_alias = message.text[1:].lower()

    if str(message.from_user.id) not in db:
        db[str(message.from_user.id)] = {
            "alias": from_user_alias
        }
        update_db()

    if "timestamp" in db[str(message.from_user.id)]:
        if throttle_check(db[str(message.from_user.id)]["timestamp"]):
            await send_error_timeout(message)
            return
        await message.answer(messages.FirstlyRemove)
        return

    if crash_alias == from_user_alias:
        await send_error(message)
        return

    db[str(message.from_user.id)]["timestamp"] = datetime.timestamp(datetime.now())
    update_db()

    if find_for_pair_and_write_new_pair(from_user_alias, crash_alias):
        crash_id = None
        for user in db:
            if db[user]["alias"] == crash_alias:
                crash_id = user
                break

        await message.answer(messages.Match.format(alias=crash_alias))
        await bot.send_message(
            text=messages.MatchMessageToAnotherPerson.format(alias=from_user_alias), 
            chat_id=crash_id
        )
    else:
        await message.answer(messages.MatchPending)


@dp.message_handler(commands=["unmatch"])
async def unmatch_handler(message: Message) -> None:
    metrics.unmatch_attempt.inc()

    from_user_alias = message.from_user.username.lower()
    crash_alias = message.get_args()[1:].lower()
    if str(message.from_user.id) not in db:
        db[str(message.from_user.id)] = {
            "alias": from_user_alias
        }
        update_db()

    if "timestamp" not in db[str(message.from_user.id)]:
        await message.answer(messages.NoMatchesDuringRemove)
        return
    elif throttle_check(db[str(message.from_user.id)]["timestamp"]):
        await send_error_timeout(message)
        return

    dbFile = open(CRASH_STORAGE_FILENAME, 'r')
    data = dbFile.read().split('\n')
    dbFile.close()

    if not message.get_args().startswith('@'):
        await send_error(message)
        return

    hashed_value = hashlib.sha256(
        f"{from_user_alias}{crash_alias}{SALT}".encode("utf-8")).hexdigest()

    if hashed_value in data:
        data.remove(hashed_value)

        update_data(data)

        db[str(message.from_user.id)] = {
            "alias": from_user_alias
        }
        update_db()

        await message.answer(messages.MatchRemoved)
        return

    await message.answer(messages.MatchNotFound)


@dp.message_handler()
async def other_messages_handler(message: Message) -> None:
    await send_error(message)


if __name__ == "__main__":
    prometheus_client.start_http_server(8000)
    executor.start_polling(dp, skip_updates=True)
