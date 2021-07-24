# from game.event.opponentevent import OpponentEvent
# from game.event.walkevent import WalkEvent


# class EventManager:
#     def __init__(self, game):
#         self.game = game
#         self.events = []
#         self.interact_entity = None

#     def check_events(self, time, frame_time):
#         print("Scanning")
#         if self.game.maphack:
#             return False
#         locked = False
#         for evt in self.events:
#             if evt.check_trigger():
#                 if not evt.triggered:
#                     evt.on_trigger(time)
#                     if evt.lock:
#                         locked = True
#         return locked

#     def check_interact(self):
#         # TODO: dubious whether this should be here or not...
#         pos = self.game.m_ent.player.get_pos()
#         direc = self.game.m_ent.player.get_dir()

#         target_pos = (pos[0] + direc[0], pos[1] + direc[1])
#         for entity in self.game.m_ent.entities:
#             if entity.game_position == target_pos:
#                 print(entity)
#                 self.interact_entity = entity
#                 entity.on_interact()
#                 self.game.m_gst.switch_state("interact")
#                 return

#     def add_event(self, event):
#         self.events.append(event)

#     def add_opponent_event(self, opponent):
#         x, y = opponent.game_position
#         dx, dy = opponent.direction
#         locations = []
#         for i in range(opponent.view_range):
#             locations.append((x + dx * (i + 1), y + dy * (i + 1)))
#         walk_event = WalkEvent(self.game, locations, opponent)
#         battle_event = OpponentEvent(self.game, [locations[0]], opponent)
#         self.events.append(walk_event)
#         self.events.append(battle_event)

#     def flush_events(self):
#         self.events.clear()
