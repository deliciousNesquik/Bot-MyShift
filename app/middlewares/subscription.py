from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from app.modules import utils

import logging

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Subscription(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:

        logging.info(f"Пользователь {data['event_context'].chat.id} пытается написать боту")
        if await utils.check_subscription(int(data['event_context'].chat.id)):
            result = await handler(event, data)
            logging.info(f"У пользователя {data['event_context'].chat.id} есть подписка")
            return result
        else:
            await data['bots'][0].send_message(
                chat_id=data['event_context'].chat.id,
                text="<b>У вас нет подписки!</b>\n\nЕсли вы являетесь работником, тогда попросите работадателя "
                     "оплатить подписку"
            )
            logging.info(f"У пользователя {data['event_context'].chat.id} нет подписки")
