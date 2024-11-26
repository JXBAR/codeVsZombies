class InfoDisplay:
    def __init__(self):
        self.storage = {}

    def store(self, position, label, value):
        self.storage[position] = (label, value)

    def draw(self, screen, font, offset_x, offset_y, color):
        y_offset = offset_y
        for position, (label, value) in sorted(self.storage.items()):
            text = f"{label}: {value}"
            self.draw_text(screen, text, (offset_x, y_offset), font, color)
            y_offset += 20
    
    @staticmethod
    def draw_text(screen, text, position, font, color):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)