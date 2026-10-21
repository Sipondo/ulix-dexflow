import json

PLAYERNAME = "ulixtestman"


class BattleManager:
    def __init__(self, game):
        self.game = game
        self.state = BattleState()  # TODO: make more
        self.player_id = -888
        self.opponent_id = -999

    def incoming_message(self, values):
        list_message = values[0]

        print("\n\n[SCHMAMAHandle] ", list_message)
        # print(f"`-----------\n\n[BattleHandler]{message}\n----------------")
        # should be split by |

        if isinstance(list_message, list):
            print("\n\n[Send Handle] ", list_message)
            self.game.m_thr.send("showdown", list_message[0])
            return

        for message in list_message.split("\n"):
            print("\n\n[Handle] ", message)
            if message.startswith(">battle"):
                continue  # TODO: remove
                self.state.teamsize_1 = int(
                    message.split("|teamsize|p1|")[1].split()[0]
                )
                self.state.teamsize_2 = int(
                    message.split("|teamsize|p1|")[1].split()[0]
                )
            elif message.startswith("|player|"):
                def_player = message.split("|player|")[1]
                number, name = def_player.split("|")[:2]

                if PLAYERNAME in name:
                    if "p1" in number:
                        self.player_id = 1
                        self.opponent_id = 2
                    elif "p2" in number:
                        self.player_id = 2
                        self.opponent_id = 1
                    else:
                        raise Exception(f"Invalid player number: {message}")

            elif message.startswith("|request|"):
                continue  # TODO: remove
                print(json.loads(message))
            elif message.startswith(f"|switch|p{self.player_id}a:"):
                def_battler = message.split(f"|switch|p{self.player_id}a:")[1]
                name, info, hp = def_battler.split("|")[:3]

                active, level = info.split(",")[:2]

                self.state.active_1 = active.strip()
                self.state.name_1 = name.strip()
                self.state.level_1 = int(level.split("L")[1].strip())
                # self.state.gender_1 = gender.strip()

                self.state.hp_1, self.state.max_hp_1 = list(map(int, hp.split("/")))

            elif message.startswith(f"|switch|p{self.opponent_id}a:"):
                def_battler = message.split(f"|switch|p{self.opponent_id}a:")[1]
                name, info, hp = def_battler.split("|")[:3]

                active, level = info.split(",")[:2]

                self.state.active_2 = active.strip()
                self.state.name_2 = name.strip()
                self.state.level_2 = int(level.split("L")[1].strip())
                # self.state.gender_2 = gender.strip()

                self.state.hp_2, self.state.max_hp_2 = list(map(int, hp.split("/")))


class BattleState:
    active_1 = None
    name_1 = "ACTIVE_1"
    active_2 = None
    name_2 = "ACTIVE_2"
    level_1 = -1
    level_2 = -1
    hp_1 = 1
    max_hp_1 = 1
    hp_2 = 1
    max_hp_2 = 1
