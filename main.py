#---------------------------------------------------------------------------------
#/_/\ 🌐 This module was loaded through https://t.me/hikkamods_bot
#( o.o ) 🔐 Licensed under the GNU AGPLv3.
#> ^ < ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
#---------------------------------------------------------------------------------
#Name: rockpaperscissors
#Author: hikariatama
#Commands:
#.rockpaperscissors | .rps
#---------------------------------------------------------------------------------

version = (2, 0, 0)

█ █ ▀ █▄▀ ▄▀█ █▀█ ▀
█▀█ █ █ █ █▀█ █▀▄ █
© Copyright 2022
https://t.me/hikariatama
🔒 Licensed under the GNU AGPLv3
🌐 https://www.gnu.org/licenses/agpl-3.0.html
#meta pic: https://static.dan.tatar/rockpaperscissors_icon.png
#meta banner: https://mods.hikariatama.ru/badges/rockpaperscissors.jpg
#meta developer: @hikarimods
#scope: inline
#scope: hikka_only
#scope: hikka_min 1.2.10

import copy
import enum
from random import choice
from typing import List

from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, utils
from ..inline.types import InlineCall

phrases = [
"Let's see who's the best!",
"I'm ready to crush you!",
"Time to show your skills!",
"May the best player win!",
"Prepare to be defeated!",
"This is going to be fun!",
"I hope you're ready for this!",
]

class Choice(enum.Enum):
rock = 1
paper = 2
scissors = 3

def beats(self, other):
    if self == Choice.rock:
        return other == Choice.scissors
    elif self == Choice.paper:
        return other == Choice.rock
    else:
        return other == Choice.paper


class Game:
def init(self, player1, player2):
self.player1 = player1
self.player2 = player2
self.result = None

def play(self, player1_choice, player2_choice):
    if player1_choice == player2_choice:
        self.result = "Tie"
    elif player1_choice.beats(player2_choice):
        self.result = self.player1
    else:
        self.result = self.player2


@loader.tds
class RockPaperScissorsMod(loader.Module):
"""Play rock-paper-scissors in Telegram"""

strings = {
    "name": "RockPaperScissors",
    "gamestart": (
        "🧠 <b>Let's play rock-paper-scissors!</b>\n<i>Waiting for second"
        " player...</i>"
    ),
    "gamestart_ai": "🐻 <b>Bear is ready to compete! Are you?</b>",
    "game_discarded": "Game is discarded",
    "wait_for_your_turn": "Wait for your turn",
    "not_your_game": "It is not your game, don't interrupt it",
    "draw": (
        "🧠 <b>The game is over! It's a draw.</b>"
    ),
    "normal_game": (
        "🧠 <b>{}</b>\n<i>Playing with <b>{}</b></i>\n\n<i>Now is the turn of"
        " <b>{}</b></i>"
    ),
    "win": (
        "🧠 <b>The game is over!</b>\n\n<i>🏆 Winner: <b>{}"
        " ({})</b></i>"
    ),
    "ai_game": (
        "🧠 <b>{}</b>\n<i><b>{}</b> is playing with <b>🐻"
        " Bear</b></i>\n\n<i>You are"
        " {}</i>"
    ),
    "not_with_yourself": "You can't play with yourself!",
}

strings_ru = {
    "gamestart": (
        "🧠 <b>Давай сыграем в камень-ножницы-бумага!</b>\n<i>Ожидание второго игрока...</i>"
    ),
    "gamestart_ai": "🐻 <b>Мишка готов сражаться! А что насчет тебя?</b>",
    "game_discarded": "Игра отменена",
    "wait_for_your_turn": "Ожидание хода",
    "not_your_game": "Это не твоя игра, не мешай",
    "draw": (
        "🧠 <b>Игра окончена! Ничья.</b>"
    ),
    "normal_game": (
        "🧠 <b>{}</b>\n<i>Игра с <b>{}</b></i>\n\n<i>Сейчас ходит <b>{}</b></i>"
    ),
    "win": (
        "🧠 <b>Игра окончена!</b>\n\n<i>🏆 Победитель: <b>{}"
        " ({})</b></i>"
    ),
    "ai_game": (
        "🧠 <b>{}</b>\n<i><b>{}</b> играет с <b>🐻 Мишкой</b></i>\n\n<i>Ты {}</i>"
    ),
    "not_with_yourself": "Ты не можешь играть сам с собой!",
    "_cmd_doc_rockpaperscissors": "Начать новую игру в камень-ножницы-бумага",
    "_cmd_doc_rps": "Сыграть с 🐻 Мишкой (У тебя нет шансов)",
    "_cls_doc": "Сыграй в камень-ножницы-бумага прямо в Телеграм",
}

async def client_ready(self, client, db):
    self._games = {}
    self._me = await client.get_me()

async def _process_click(
    self,
    call: InlineCall,
    choice: Choice,
):
    if call.from_user.id not in [
        self._me.id,
        self._games[call.form["uid"]]["2_player"],
    ]:
        await call.answer(self.strings("not_your_game"))
        return

    if call.from_user.id != self._games[call.form["uid"]]["turn"]:
        await call.answer(self.strings("wait_for_your_turn"))
        return

    player1_choice = choice
    player2_choice = Choice(choice(list(Choice)))

    game = Game(
        self._games[call.form["uid"]]["name"],
        "🐻 Bear" if call.from_user.id != self._me.id else self._games[call.form["uid"]]["name"],
    )
    game.play(player1_choice, player2_choice)

    self._games[call.form["uid"]]["turn"] = (
        self._me.id
        if call.from_user.id != self._me.id
        else self._games[call.form["uid"]]["2_player"]
    )

    await call.edit(**self._render(call.form["uid"], player1_choice, player2_choice, game.result))

async def _process_click_ai(self, call: InlineCall, choice: Choice):
    if call.form["uid"] not in self._games:
        await call.answer(self.strings("game_discarded"))
        await call.delete()

    if call.from_user.id != self._games[call.form["uid"]]["user"].id:
        await call.answer(self.strings("not_your_game"))
        return

    player1_choice = choice
    player2_choice = Choice(choice(list(Choice)))

    game = Game(
        self._games[call.form["uid"]]["user"].first_name,
        "🐻 Bear",
    )
    game.play(player1_choice, player2_choice)

    await call.edit(**self._render_ai(call.form["uid"], player1_choice, player2_choice, game.result))

def _render(self, uid: str, player1_choice: Choice, player2_choice: Choice, result: str) -> dict:
    if uid not in self._games or uid not in self.inline._units:
        return

    game = self._games[uid]
    text = self.strings("normal_game").format(
        choice(phrases),
        game["name"],
        (
            utils.escape_html(get_display_name(self._me))
            if game["turn"] == self._me.id
            else game["name"]
        ),
    )

    if result == "Tie":
        return {"text": self.strings("draw")}
    elif result == game["name"]:
        return {"text": self.strings("win").format(
            utils.escape_html(get_display_name(self._me)),
            "✊" if player1_choice == Choice.rock else "✋" if player1_choice == Choice.paper else "✌️",
        )}
    else:
        return {"text": self.strings("win").format(
            "🐻 Bear",
            "✊" if player2_choice == Choice.rock else "✋" if player2_choice == Choice.paper else "✌️",
        )}

async def inline__start_game(self, call: InlineCall):
    if call.from_user.id == self._me.id:
        await call.answer(self.strings("not_with_yourself"))
        return

    uid = call.form["uid"]
    first = choice([call.from_user.id, self._me.id])
    self._games[uid] = {
        "2_player": call.from_user.id,
        "turn": first,
        "name": utils.escape_html(
            get_display_name(await self._client.get_entity(call.from_user.id))
        ),
    }

    await call.edit(**self._render(uid, None, None, None))

async def inline__start_game_ai(self, call: InlineCall):
    uid = call.form["uid"]

    user = await self._client.get_entity(call.from_user.id)

    first = choice([user.id, "bear"])
    self._games[uid] = {
        "2_player": "bear",
        "turn": user.id,
        "user": user,
    }

    await call.edit(**self._render_ai(uid, None, None, None))

def _render_ai(self, uid: str, player1_choice: Choice, player2_choice: Choice, result: str) -> dict:
    if uid not in self._games or uid not in self.inline._units:
        return

    game = self._games[uid]
    text = self.strings("ai_game").format(
        choice(phrases),
        utils.escape_html(get_display_name(game["user"])),
        "✊" if player1_choice == Choice.rock else "✋" if player1_choice == Choice.paper else "✌️",
    )

    if result == "Tie":
        return {"text": self.strings("draw")}
    elif result == game["user"].first_name:
        return {"text": self.strings("win").format(
            utils.escape_html(get_display_name(game["user"])),
            "✊" if player1_choice == Choice.rock else "✋" if player1_choice == Choice.paper else "✌️",
        )}
    else:
        return {"text": self.strings("win").format(
            "🐻 Bear",
            "✊" if player2_choice == Choice.rock else "✋" if player2_choice == Choice.paper else "✌️",
        )}

async def rockpaperscissorscmd(self, message: Message):
    """Start new rock-paper-scissors game"""
    await self.inline.form(
        self.strings("gamestart"),
        message=message,
        reply_markup={
            "text": "✊ Rock",
            "callback": self._process_click,
            "args": (Choice.rock,),
        } | {
            "text": "✋ Paper",
            "callback": self._process_click,
            "args": (Choice.paper,),
        } | {
            "text": "✌️ Scissors",
            "callback": self._process_click,
            "args": (Choice.scissors,),
        },
        ttl=15 * 60,
        disable_security=True,
    )

async def rpscmd(self, message: Message):
    """Play with 🐻 Bear (You have no chances to win)"""
    await self.inline.form(
        self.strings("gamestart_ai"),
        message=message,
        reply_markup={
            "text": "✊ Rock",
            "callback": self._process_click_ai,
            "args": (Choice.rock,),
        } | {
            "text": "✋ Paper",
            "callback": self._process_click_ai,
            "args": (Choice.paper,),
        } | {
            "text": "✌️ Scissors",
            "callback": self._process_click_ai,
            "args": (Choice.scissors,),
        },
        ttl=15 * 60,
        disable_security=True,
    )
