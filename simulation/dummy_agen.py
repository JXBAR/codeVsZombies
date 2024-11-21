from agent  import AbstractAgen
class DummyAgen(AbstractAgen):
    def play(self, x, y, human_count, humans, zombie_count, zombies):
        return {
            "target_x": x,
            "target_y": y,
        }