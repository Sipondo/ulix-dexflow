"""fobject
Retrieve a list of all entities with substring in their UID.

Retrieve a list of all entities that have the given string as a substring in their unique identifier.
Supplying an empty string retrieves all entities.

in:
- String: substring to filter on

out:
- List of entities: list of entities that match the filter

"""


class GetEntities:
    def __init__(self, act, src, user, s):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = s

    def on_read(self):
        if self.s == "":
            return self.game.m_ent.entities.values()
        return [x for x in self.game.m_ent.entities.values() if self.s in x.entity_uid]
