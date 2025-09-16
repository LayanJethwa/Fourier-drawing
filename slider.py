import pygame
white = (255,255,255)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, percent=False):
        self.rect = pygame.Rect(x, y, w, h)  # Slider track
        self.knob_radius = h // 2
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        # Knob position along the track
        self.knob_x = self.get_knob_x_from_value(initial_val)
        self.dragging = False
        self.font = pygame.font.SysFont(None, h)
        self.percent = percent

    def get_knob_x_from_value(self, value):
        return int(self.rect.x + (value - self.min_val) / (self.max_val - self.min_val) * self.rect.w)

    def get_value_from_knob(self, knob_x):
        ratio = (knob_x - self.rect.x) / self.rect.w
        return round(self.min_val + ratio * (self.max_val - self.min_val))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.knob_x - self.knob_radius, self.rect.centery - self.knob_radius,
                           self.knob_radius*2, self.knob_radius*2).collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.w))
            self.value = self.get_value_from_knob(self.knob_x)

    def draw(self, screen, track_color=(100,100,100), knob_color=(200,0,0)):
        # Draw track
        pygame.draw.rect(screen, track_color, self.rect)
        # Draw knob
        pygame.draw.circle(screen, knob_color, (self.knob_x, self.rect.centery), self.knob_radius)
        value_text = str(int(self.value))
        if self.percent:
            value_text += "%"
        text_surf = self.font.render(value_text, True, white)
        text_rect = text_surf.get_rect(center=(self.knob_x, self.rect.centery))
        screen.blit(text_surf, text_rect)