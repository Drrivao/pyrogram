# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import logging
from typing import Union

import pyrogram
from pyrogram.api import functions
from pyrogram.api.errors import FloodWait
from ...ext import BaseClient

log = logging.getLogger(__name__)


class GetHistory(BaseClient):
    async def get_history(
        self,
        chat_id: Union[int, str],
        limit: int = 100,
        offset: int = 0,
        offset_id: int = 0,
        offset_date: int = 0,
        reverse: bool = False
    ):
        """Use this method to retrieve a chunk of the history of a chat.

        You can get up to 100 messages at once.
        For a more convenient way of getting a chat history see :meth:`iter_history`.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, the first 100 messages are returned.

            offset (``int``, *optional*):
                Sequential number of the first message to be returned. Defaults to 0 (most recent message).
                Negative values are also accepted and become useful in case you set offset_id or offset_date.

            offset_id (``int``, *optional*):
                Pass a message identifier as offset to retrieve only older messages starting from that message.

            offset_date (``int``, *optional*):
                Pass a date in Unix time as offset to retrieve only older messages starting from that date.

            reverse (``bool``, *optional*):
                Pass True to retrieve the messages in reversed order (from older to most recent).

        Returns:
            On success, a :obj:`Messages <pyrogram.Messages>` object is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """

        while True:
            try:
                messages = await pyrogram.Messages._parse(
                    self,
                    await self.send(
                        functions.messages.GetHistory(
                            peer=await self.resolve_peer(chat_id),
                            offset_id=offset_id,
                            offset_date=offset_date,
                            add_offset=offset * (-1 if reverse else 1) - (limit if reverse else 0),
                            limit=limit,
                            max_id=0,
                            min_id=0,
                            hash=0
                        )
                    )
                )
            except FloodWait as e:
                log.warning("Sleeping for {}s".format(e.x))
                await asyncio.sleep(e.x)
            else:
                break

        if reverse:
            messages.messages.reverse()

        return messages
