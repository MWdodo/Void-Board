import pygame
import random
import sys
import math
import datetime
import os

pygame.init()

WIDTH, HEIGHT = 600, 325
SUITS = ['♣', '♦', '♠', '♥']
NUMBERED_RANKS = [str(n) for n in range(2, 11)]
FACE_RANKS = ['J', 'Q', 'K', 'A']
BUTTON_SHINE = (255, 255, 255, 120)
COLORS = {
    'bg': (30, 30, 30),
    'caller': {
        'button': (70, 255, 50),
        'active': (75, 255, 125),
        'result': (20, 40, 30),
        'flash': (160, 230, 140),
        'border': (120, 255, 100)
    },
    'playlist': {
        'button': (20, 210, 255),
        'active': (50, 230, 255),
        'result': (20, 30, 40),
        'flash': (160, 215, 240),
        'border': (0, 230, 255)
    },
    'd6': {
        'button': (255, 150, 30),
        'active': (255, 180, 60),
        'result': (40, 30, 20),
        'flash': (255, 195, 100),
        'border': (255, 180, 100)
    },
    'history': {
        'bg': (20, 20, 30),
        'text': (200, 200, 220),
        'border': (60, 60, 80)
    }
}

class CardDeck:
    
    def __init__(self, suits, ranks, deck_type):
        self.deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        self.type = deck_type
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def draw(self):
        return self.deck.pop() if self.deck else None

class App:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("VOID 1680 AM Caller/Player Decks")
        self.caller_deck = CardDeck(SUITS, FACE_RANKS, "Caller")
        self.playlist_deck = CardDeck(SUITS, NUMBERED_RANKS, "Playlist")
        self.caller_result = ""
        self.playlist_result = ""
        self.d6_result = ""
        self.font_main = pygame.font.SysFont("segoeuiemoji", 16, bold=True)
        self.font_result = pygame.font.SysFont("segoeuiemoji", 14)
        self.font_title = pygame.font.SysFont("Courier Regular", 110, bold=True, italic=True)
        self.font_other = pygame.font.SysFont("Courier New", 32, bold=True)
        btn_width, btn_height = 120, 40
        result_width, result_height = 120, 35
        vertical_spacing = 10
        group1_x = WIDTH//6 - btn_width//2
        group2_x = WIDTH//2 - btn_width//2
        group3_x = 5*WIDTH//6 - btn_width//2
        self.caller_button = pygame.Rect(group1_x, 100, btn_width, btn_height)
        self.caller_result_rect = pygame.Rect(group1_x, 100 + btn_height + vertical_spacing, result_width, result_height)
        self.playlist_button = pygame.Rect(group2_x, 100, btn_width, btn_height)
        self.playlist_result_rect = pygame.Rect(group2_x, 100 + btn_height + vertical_spacing, result_width, result_height)
        self.d6_button = pygame.Rect(group3_x, 100, btn_width, btn_height)
        self.d6_result_rect = pygame.Rect(group3_x, 100 + btn_height + vertical_spacing, result_width, result_height)
        self.wave_position = 10
        self.wave_speed = 0.25
        self.flash_active = False
        self.flash_time = 0
        self.flash_target = None
        self.flash_value = ""
        self.button_pressed = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.on_air = True
        self.switch_rect = pygame.Rect(WIDTH - 465, 280, 120, 35)
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 3):
            pygame.draw.line(self.overlay, (0, 0, 0, 100), (0, y), (WIDTH, y))
        self.overlay.fill((100, 100, 100, 100), special_flags=pygame.BLEND_MULT)
        self.switch_progress = 1.0 if self.on_air else 0.0
        self.block_buttons = []
        block_width, block_height = 50, 40
        start_x, start_y = 20, 230
        button_spacing = 5
        for i, suit in enumerate(SUITS):
            row = i // 2
            col = i % 2
            btn_rect = pygame.Rect(
                start_x + col * (block_width + button_spacing),
                start_y + row * (block_height + button_spacing),
                block_width,
                block_height
            )
            self.block_buttons.append(btn_rect)
        self.active_block = None
        self.block_font = pygame.font.SysFont("arial", 16, bold=True)
        self.history = []
        self.history_max_entries = 15
        self.history_rect = pygame.Rect(WIDTH - 205, 230, 190, 85)
        self.history_scroll = 0
        self.history_font = pygame.font.SysFont("Courier New", 12)
        self.clear_history_rect = pygame.Rect(WIDTH - 220, 325, 190, 200)
        self.history_file = "VOID_1680AM_LOG.txt"
        self.max_visible_entries = 5
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                f.write("VOID 1680 AM History Log\n\nLog from " + (datetime.datetime.now().strftime("%Y/%m/%d %H:%M\n\n")))
        else:
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write("\nLog from " + (datetime.datetime.now().strftime("%Y/%m/%d %H:%M\n\n")))
        self.credits_font = pygame.font.SysFont("Arial", 8)
        self.credits_text = "Program by Matthew Wrisley | 'VOID 1680 AM' by Ken Lowery | © 2023 Bannerless Games"
        self.credits_color = (80, 80, 80)

    def log_history(self, action, result):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        entry = f"[{timestamp}] {action}: {result}"
        self.history.insert(0, entry)
        if len(self.history) > self.history_max_entries:
            self.history = self.history[:self.history_max_entries]
        with open(self.history_file, 'a', encoding='utf-8') as f:
            f.write(entry + "\n")


    def draw_block_selector(self):
        label = self.block_font.render("Block No.", True, (200, 200, 200))
        self.screen.blit(label, (20, 210))
        for i, (btn_rect, suit) in enumerate(zip(self.block_buttons, SUITS)):
            bg_color = (50, 50, 80) if self.active_block == i else (30, 30, 50)
            border_color = (100, 100, 150) if self.active_block == i else (70, 70, 100)
            pygame.draw.rect(self.screen, bg_color, btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, btn_rect, 2, border_radius=8)
            btn_text = f"{i+1} {suit}"
            text_surf = self.block_font.render(btn_text, True, (220, 220, 220))
            text_rect = text_surf.get_rect(center=btn_rect.center)
            self.screen.blit(text_surf, text_rect)
            mouse_pos = pygame.mouse.get_pos()
        for i, btn_rect in enumerate(self.block_buttons):
            if btn_rect.collidepoint(mouse_pos) and self.active_block != i:
                highlight = pygame.Surface((btn_rect.width, btn_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(highlight, (255, 255, 255, 30), (0, 0, btn_rect.width, btn_rect.height), border_radius=8)
                self.screen.blit(highlight, btn_rect)

    
    def draw_on_off_switch(self):
        bg_color = (50, 205, 50) if self.on_air else (200, 50, 50)
        pygame.draw.rect(self.screen, bg_color, self.switch_rect, border_radius=20)
        border_color = (120, 255, 100) if self.on_air else (255, 120, 100)
        pygame.draw.rect(self.screen, border_color, self.switch_rect, 3, border_radius=20)
        indicator_pos = self.switch_progress
        indicator_x = self.switch_rect.left + 20 + int(indicator_pos * (self.switch_rect.width - 40))
        pygame.draw.circle(self.screen, (240, 240, 240), (indicator_x, self.switch_rect.centery), 12)
        label_text = "  ON AIR" if self.on_air else "OFF AIR  "
        label = self.font_main.render(label_text, True, (240, 240, 240))
        if self.on_air:
            text_x = self.switch_rect.left + 15
        else:
            text_x = self.switch_rect.right - label.get_width() - 15
        shadow = self.font_main.render(label_text, True, (0, 0, 0, 150))
        self.screen.blit(shadow, (text_x + 1, self.switch_rect.centery - shadow.get_height()//2 + 1))
        self.screen.blit(label, (text_x, self.switch_rect.centery - label.get_height()//2))
            
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.switch_rect.collidepoint(event.pos):
                    self.on_air = not self.on_air
                if not self.on_air:
                    continue
                for i, btn_rect in enumerate(self.block_buttons):
                    if btn_rect.collidepoint(event.pos):
                        self.active_block = i
                        self.playlist_deck = CardDeck([SUITS[i]], NUMBERED_RANKS, "Playlist")
                        self.log_history("B-SEL", f"Block {i+1} ({SUITS[i]})")
                        break
                if self.caller_button.collidepoint(event.pos):
                    self.button_pressed = "caller"
                    self.draw_card(self.caller_deck, "caller")
                if self.playlist_button.collidepoint(event.pos):
                    self.button_pressed = "playlist"
                    self.draw_card(self.playlist_deck, "playlist")
                if self.d6_button.collidepoint(event.pos):
                    self.button_pressed = "d6"
                    self.roll_d6()
                if self.clear_history_rect.collidepoint(event.pos):
                    self.history.clear()
                    with open(self.history_file, 'w', encoding='utf-8') as f:
                        f.write("VOID 1680 AM History Log (Cleared)\n\n")
            if event.type == pygame.MOUSEWHEEL:
                mouse_pos = pygame.mouse.get_pos()
                if self.history_rect.collidepoint(mouse_pos):
                    new_scroll = self.history_scroll - event.y
                    max_scroll = max(0, len(self.history) - self.max_visible_entries)
                    self.history_scroll = max(0, min(new_scroll, max_scroll))
            '''if event.type == pygame.MOUSEBUTTONUP:
                self.button_pressed = None'''

    def update(self):
        self.wave_position += self.wave_speed
        if self.wave_position > 20:
            self.wave_position = 0
        if self.flash_active:
            self.flash_time += 1
            if self.flash_time >= 9:
                self.flash_active = False
                if self.flash_target == "caller":
                    self.caller_result = self.flash_value
                elif self.flash_target == "playlist":
                    self.playlist_result = self.flash_value
                elif self.flash_target == "d6":
                    self.d6_result = self.flash_value
        target = 1.0 if self.on_air else 0.0
        self.switch_progress += (target - self.switch_progress) * 0.2
    
    def draw(self):
        self.screen.fill(COLORS['bg'])
        title_text = "VOID 1680 AM"
        title_surf = self.font_title.render(title_text, True, (255, 255, 255)).convert_alpha()
        gradient = pygame.Surface(title_surf.get_size(), pygame.SRCALPHA)
        for x in range(title_surf.get_width()):
            r = int(255 - (x/title_surf.get_width())*75)
            g = int(50 - (x/title_surf.get_width())*30)
            b = int(200 - (x/title_surf.get_width())*50)
            pygame.draw.line(gradient, (r, g, b, 255), (x, 0), (x, title_surf.get_height()))
        final_title = gradient.copy()
        final_title.blit(title_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        shadow = self.font_title.render(title_text, True, (100, 0, 60, 150))
        self.screen.blit(shadow, (WIDTH//2 - title_surf.get_width()//2 + 2, 19))
        self.screen.blit(final_title, (WIDTH//2 - title_surf.get_width()//2, 15))
        self.draw_block_selector()
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(self.caller_button, "CALLER", COLORS['caller'], self.caller_button.collidepoint(mouse_pos), self.button_pressed == "caller")
        self.draw_button(self.playlist_button, "PLAYLIST", COLORS['playlist'], self.playlist_button.collidepoint(mouse_pos), self.button_pressed == "playlist")
        self.draw_button(self.d6_button, "ROLL D6", COLORS['d6'], self.d6_button.collidepoint(mouse_pos), self.button_pressed == "d6")
        self.draw_result_box(self.caller_result_rect, self.caller_result, COLORS['caller']['result'], COLORS['caller']['flash'] if self.flash_active and self.flash_target == "caller" else COLORS['caller']['result'], COLORS['caller']['button'])
        self.draw_result_box(self.playlist_result_rect, self.playlist_result, COLORS['playlist']['result'], COLORS['playlist']['flash'] if self.flash_active and self.flash_target == "playlist" else COLORS['playlist']['result'], COLORS['playlist']['button'])
        self.draw_result_box(self.d6_result_rect, self.d6_result, COLORS['d6']['result'], COLORS['d6']['flash'] if self.flash_active and self.flash_target == "d6" else COLORS['d6']['result'], COLORS['d6']['button'])
        self.draw_antenna()
        self.draw_on_off_switch()
        if not self.on_air:
            msg = self.font_other.render("Switch to \"ON AIR\" to interact", True, (255, 100, 100))
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 175))
            self.screen.blit(self.overlay, (0, 0))
        pygame.draw.rect(self.screen, COLORS['history']['bg'], self.history_rect, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['history']['border'], self.history_rect, 1, border_radius=5)
        history_title = self.font_main.render("HISTORY", True, (200, 200, 220))
        self.screen.blit(history_title, (self.history_rect.x + 10, self.history_rect.y - 20))
        for i in range(self.max_visible_entries):
            entry_idx = self.history_scroll + i
            if entry_idx < len(self.history):
                entry = self.history_font.render(self.history[entry_idx], True, COLORS['history']['text'])
                self.screen.blit(entry, (self.history_rect.x + 5, self.history_rect.y + 5 + i * 15))
        credits_surface = self.credits_font.render(self.credits_text, True, self.credits_color)
        self.screen.blit(credits_surface, (10, 5))
        
        pygame.display.flip()
    
    def draw_button(self, rect, text, colors, is_hovered, is_pressed):
        y_offset = 3 if is_pressed else 0
        draw_rect = rect.copy()
        draw_rect.y += y_offset
        corner_radius = 10
        shadow_rect = draw_rect.move(4, 4)
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=corner_radius)
        button_surface = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        base_color = colors['active'] if is_hovered else colors['button']
        for i in range(draw_rect.height):
            alpha = 255 - int(i * (100/draw_rect.height))
            shade_color = tuple(min(max(c - int(i * (30/draw_rect.height)), 0), 255) for c in base_color)
            pygame.draw.line(button_surface, shade_color, (0, i), (draw_rect.width, i))
        mask = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, draw_rect.width, draw_rect.height), border_radius=corner_radius)
        button_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(button_surface, draw_rect)
        pygame.draw.rect(self.screen, colors['border'], draw_rect, 3, border_radius=corner_radius)
        if is_hovered and not is_pressed:
            shine_height = draw_rect.height//4
            shine_surface = pygame.Surface((draw_rect.width, shine_height), pygame.SRCALPHA)
            pygame.draw.rect(shine_surface, BUTTON_SHINE, (0, 0, draw_rect.width, shine_height), border_top_left_radius=corner_radius, border_top_right_radius=corner_radius, border_bottom_left_radius=0, border_bottom_right_radius=0)
            old_clip = self.screen.get_clip()
            self.screen.set_clip(draw_rect)
            self.screen.blit(shine_surface, (draw_rect.x, draw_rect.y))
            self.screen.set_clip(old_clip)
        text_color = (240, 240, 240)
        text_surf = self.font_main.render(text, True, text_color)
        text_pos = (draw_rect.centerx - text_surf.get_width()//2, draw_rect.centery - text_surf.get_height()//2 + (1 if is_pressed else 0))
        shadow_surf = self.font_main.render(text, True, (0, 0, 0, 250))
        self.screen.blit(shadow_surf, (text_pos[0]+1, text_pos[1]+1))
        self.screen.blit(text_surf, text_pos)
        if is_hovered and not is_pressed:
            glow_intensity = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 40
            glow_color = (*colors['border'], glow_intensity)
            glow_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, glow_color, (0, 0, draw_rect.width, draw_rect.height),border_radius=corner_radius)
            self.screen.blit(glow_surf, draw_rect)

    def draw_result_box(self, rect, text, bg_color, flash_color, text_color):
        current_bg = flash_color if self.flash_active and (
            (self.flash_target == "caller" and rect == self.caller_result_rect) or
            (self.flash_target == "playlist" and rect == self.playlist_result_rect) or
            (self.flash_target == "d6" and rect == self.d6_result_rect)
        ) else bg_color
        pygame.draw.rect(self.screen, current_bg, rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 2, border_radius=5)
        if text and isinstance(text, str):
            words = text.split(' ')
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_width = self.font_result.size(test_line)[0]
                if test_width < rect.width - 20:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            for i, line in enumerate(lines):
                text_surf = self.font_result.render(line, True, text_color)
                self.screen.blit(text_surf, (rect.centerx - text_surf.get_width()//2, rect.y + 10 + i * 20))

    def draw_antenna(self):
        center_x = WIDTH // 2
        tower_top = 300
        if self.on_air:
            num_arcs = 3
            for i in range(num_arcs):
                offset = self.wave_position + (i * 20) +10
            
                pygame.draw.arc(self.screen, (219, 222, 231), 
                           (center_x - offset + 3, tower_top - 65 - (i * 15), 
                            offset * 2, 30 + (i * 30)),
                           math.radians(155), math.radians(205), 1)
            
                pygame.draw.arc(self.screen, (219, 222, 231), 
                           (center_x - offset, tower_top - 65 - (i * 15), 
                            offset * 2, 30 + (i * 30)),
                           math.radians(-25), math.radians(25), 1)
                pygame.draw.circle(self.screen, (245, 35, 85), (center_x + 1, tower_top - 50), 6)
        pygame.draw.line(self.screen, (136, 136, 136), (center_x, tower_top + 7), (center_x, tower_top - 45), 3)
        pygame.draw.line(self.screen, (68, 68, 68), (center_x - 10, tower_top + 7), (center_x + 10, tower_top + 7), 5)
        pygame.draw.line(self.screen, (127, 128, 159), (center_x - 38, tower_top + 7), (center_x, tower_top - 45), 1)
        pygame.draw.line(self.screen, (127, 128, 159), (center_x + 38, tower_top + 7), (center_x, tower_top - 45), 1)
        pygame.draw.line(self.screen, (127, 128, 159), (center_x - 20, tower_top + 7), (center_x, tower_top - 25), 1)
        pygame.draw.line(self.screen, (127, 128, 159), (center_x + 20, tower_top + 7), (center_x, tower_top - 25), 1)
        if not self.on_air:
            pygame.draw.circle(self.screen, (127, 128, 159), (center_x + 1, tower_top - 50), 6)

    def flash_result(self, target, value, flash_color, normal_color):
        self.flash_active = True
        self.flash_time = 0
        self.flash_target = target
        self.flash_value = value
        self.flash_color = flash_color
        self.normal_color = normal_color
        if target == "caller":
            self.caller_result = ""
        elif target == "playlist":
            self.playlist_result = ""
        elif target == "d6":
            self.d6_result = ""
            
    def draw_card(self, deck, target):
        card = deck.draw()
        if card:
            self.flash_result(target, card, COLORS[deck.type.lower()]['flash'], COLORS[deck.type.lower()]['result'])
            self.log_history(deck.type, card)
        else:
            self.flash_result(target, "Empty!", COLORS[deck.type.lower()]['button'], COLORS[deck.type.lower()]['result'])
            self.log_history(deck.type, "Empty!")

    def roll_d6(self):
        value = random.randint(1, 6)
        self.flash_result("d6", f"🎲 {value}", COLORS['d6']['flash'], COLORS['d6']['result'])
        self.log_history("D6 Roll", str(value))
    


if __name__ == "__main__":
    app = App()
    app.run()
