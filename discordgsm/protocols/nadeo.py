import time
from typing import TYPE_CHECKING

import opengsq

from discordgsm.protocols.protocol import Protocol

if TYPE_CHECKING:
    from discordgsm.gamedig import GamedigResult


class Nadeo(Protocol):
    name = "nadeo"

    async def query(self):
        host, port = str(self.kv["host"]), int(str(self.kv["port"]))
        username = str(self.kv.get("username", ""))
        password = str(self.kv.get("password", ""))

        nadeo = opengsq.Nadeo(host, port, self.timeout)
        start = time.time()

        async with nadeo:
            if username and password:
                await nadeo.authenticate(username, password)
            
            status = await nadeo.get_status()
            ping = int((time.time() - start) * 1000)

            players = []
            for player in status.players:
                players.append({
                    "name": player.get("Name", player.get("Login", "")),
                    "raw": player
                })

            result: GamedigResult = {
                "name": status.server_options.name,
                "map": status.map_info.name,
                "password": status.server_options.password,
                "numplayers": len(status.players),
                "numbots": 0,
                "maxplayers": status.server_options.max_players,
                "players": players,
                "bots": [],
                "connect": f"{host}:{port}",
                "ping": ping,
                "raw": status.server_options.__dict__
            }

            return result
