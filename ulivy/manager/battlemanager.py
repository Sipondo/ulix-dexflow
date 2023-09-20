import json


class BattleManager:
    def __init__(self, game):
        self.game = game
        self.state = BattleState()

    def incoming_message(self, values):
        message = values[0]

        print("\n\n[Handle] ", message)
        # print(f"`-----------\n\n[BattleHandler]{message}\n----------------")
        # should be split by |

        if isinstance(message, list):
            self.game.m_thr.send("showdown", message[0])

        if message.startswith(">battle"):
            self.state.teamsize_1 = int(message.split("|teamsize|p1|")[1].split()[0])
            self.state.teamsize_2 = int(message.split("|teamsize|p1|")[1].split()[0])
        elif message.startswith("|request|"):
            print(json.loads(message))
        elif message.startswith("|switch|p1a:"):
            self.state.active_1 = message.split("|switch|p1a:")[1].split("|")[0].strip()
        elif message.startswith("|switch|p2a:"):
            self.state.active_1 = message.split("|switch|p2a:")[1].split("|")[0].strip()


class BattleState:
    pass
