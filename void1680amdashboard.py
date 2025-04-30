'''

Code and layout by Matthew Wrisley
Created v1 14APR2025
Created v2 30APR2025

"VOID 1680 AM" and "Voices in the Void"
is copyright of Bannerless Games
and created by Ken Lowery

'''

import pygame
import random
import sys
import math
import datetime
import os
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 1110, 480
SUITS = ['♣', '♦', '♠', '♥']
RANKS = ['J', 'Q', 'K', 'A']
BUTTON_SHINE = (255, 255, 255, 120)
HISTORY_FILE = "VOID_1680_AM_LOG.txt"
MAX_HISTORY_ENTRIES = 15
MAX_VISIBLE_ENTRIES = 5

# Colors used
COLORS = {
    'bg': (30, 30, 30),
    'caller': {
        'button': (70, 255, 50),
        'active': (75, 255, 125),
        'result': (20, 40, 30),
        'flash': (160, 230, 140),
        'border': (120, 255, 100)
    },
    'subject': {
        'button': (20, 210, 255),
        'active': (50, 230, 255),
        'result': (20, 30, 40),
        'flash': (160, 215, 240),
        'border': (0, 230, 255)
    },
    'request': {
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
    },
    'block': {
        'current': (80, 80, 120),
        'other': (50, 50, 80)
    },
    'second_call': {
        'button': (180, 100, 255),
        'active': (200, 120, 255),
        'result': (40, 20, 50),
        'flash': (210, 170, 255),
        'border': (180, 100, 255)
    },
    'third_call': {
        'button': (255, 100, 180),
        'active': (255, 120, 200),
        'result': (50, 20, 40),
        'flash': (255, 170, 210),
        'border': (255, 100, 180)
    },
    'fourth_call': {
        'button': (100, 255, 180),
        'active': (120, 255, 200),
        'result': (20, 50, 40),
        'flash': (170, 255, 210),
        'border': (100, 255, 180)
    },
    'multi_call': {
        'result': (30, 30, 50),
        'flash': (150, 150, 200),
        'border': (100, 100, 150)
    },
    'playlist': {
        'button': (255, 100, 100),
        'active': (255, 140, 140),
        'result': (40, 20, 20),
        'flash': (255, 170, 170),
        'border': (255, 120, 120)
    }
}

# Playlist
PLAYLIST = {
    'clubs_1_block': {
        2: 'The new obsession – the thing you listen to every day right now.Why do you think it\'s resonating?',
        3: 'An offhand suggestion that became a favorite song.Who or what recommended it to you?',
        4: 'The first song you think of when you think of someone important to you.Who came to mind? Why that song?',
        5: 'The one you sing along to every time you hear it. What\'s your favorite bit?',
        6: 'A song about a dream, a goal, or an aspiration – realistic or whimsical. What does it make you aspire to be?',
        7: 'Something you sing along to with a friend. How did you both come to love it?',
        8: 'The drum beat that always has you tapping your foot and drumming on your desk. What\'s your favorite bit?',
        9: 'You\'re ready to take a walk orgo running. What song sets thepace for you?',
        10: 'The sleaziest song you love. Is it liberating, or a dirty secret?',
    },
    'diamonds_2_block': {
        2: 'A song you listen to to psyche yourself up for a big moment. When has it worked?',
        3: 'You misunderstood the lyrics for years. You think your version is better.',
        4: 'Something with lyrics you quote often. What\'s the line that grabs you?',
        5: 'A song from a curveball genre, unlike anything else you listen to. Is it embarrassing to admit to it?',
        6: 'A song that helps you focus and tune in. What has it helped you with?',
        7: 'A song that helps you imagine yourself a villain.',
        8: 'One of the stupidest songs you love. It sucks, but you can\'t shake it.',
        9: 'You\'re at the beach. What are you listening to? Is it chill or does it get you fired up?',
        10: 'A song that makes you feel sexy or cool. What kind of scenarios do you imagine yourself in when you listen to it?',
    },
    'spades_3_block': {
        2: 'A song that always makes you tear up. What is it that gets you?',
        3: 'One of your "our" songs, something you shared with someone close to you. Who was it? Why this song?',
        4: 'The first song you think about when you think of summers as a kid. What does it feel like to listen to now?',
        5: 'The first song you think about when you think of winters as a kid. Does winter still feel this way to you?',
        6: 'It\'s summer. It\'s late. You have all the windows open and you\'re restless. What do you put on?',
        7: 'You\'re driving late at night down a lonesome highway. What song are you putting on? Does it make you feel less alone, or more?',
        8: 'A song about something ending. Is it bitter or bittersweet to you?',
        9:'A song from when your parents were young. How did you discover it?',
        10: 'The saddest song that makes you smile. What about it is so endearing?',
    },
    'hearts_4_block': {
        2: 'A song from one of the first acts you saw live. Did you choose the show, or did someone take you?',
        3: 'A song from one of the first albums you bought yourself. Where did you buy it?',
        4: 'One of the first songs you learned all the lyrics to. Do you still remember them?',
        5: 'A song that got you through a breakup, romantic or platonic. How does it feel to hear it again?',
        6: 'A song your family bonded over. Who loved it the most? Why?',
        7: 'A song from a band you hid from your parental figure. Were you right to, or was it kind of silly?',
        8: 'A song that makes you feel invincible. Barring that, like a survivor.Why this one?',
        9: 'One of the most memorable songs you saw live.Where was it? Who was with you?',
        10: 'You\'ve been out all night, and the sun is rising. What song reinvigorates you for the day?',
    }
}

# Caller Rules
CALLER_RULES = {
    'rank': {
        'J': "Young Caller, on the cusp of adulthood",
        'Q': "Established adult, 20s to 40s",
        'K': "Elder, middle aged or older",
        'A': "Ambiguous - possibly using voice modulation"
    },
    'request': {
        1: "Something sunny and warm, a dream of another place",
        2: "An old standard - a cliché - you haven't listened to in years",
        3: "An undeniably good song from an act you dislike",
        4: "A Top 40 track from the last year",
        5: "A song you associate with someone you no longer talk to",
        6: "Something cool, and dark - something to drift away to"
    },
    'subject': {
        '♣': {
            'mood': "Mellow, introspective",
            1: "Romance, blooming or evolving",
            2: "Friendship, strengthened or reignited",
            3: "Family, shifting definitions or calcifying ones",
            4: "Money, more important or less all the time",
            5: "Today's Events, mundane or portentous",
            6: "Last Night's Dream, enlightening or confusing"
        },
        '♠': {
            'mood': "Quiet, melancholy",
            1: "Romance, unrequited or star-crossed",
            2: "Friendship, lopsided in their favor or against",
            3: "Family, overwhelming or nonexistent",
            4: "Prospects, narrow or shallow",
            5: "A Conversation, definitive or nagging",
            6: "A Conclusion, painfully slow or violently sudden"
        },
        '♦': {
            'mood': "Agitated, worried",
            1: "Romance, on the rocks or ending",
            2: "Friendship, in a fight or considering a betrayal",
            3: "Family, deepening rivalries or an unpleasant revelation",
            4: "Money, not enough or a terrible windfall",
            5: "The Future, uncertain or all too clear",
            6: "The Past, forever out of reach or all too present"
        },
        '♥': {
            'mood': "Passionate, energized",
            1: "Romance, full of potential or rife with jealousy",
            2: "Friendship, shared secret or shared conspiracy",
            3: "Family, growing by one or reduced by one",
            4: "Money, career prospects or a permanent change",
            5: "Infatuation, innocent or scandalous",
            6: "A Decision, quotidian or life-changing"
        }
    },
    'second_call': {
        1: "Things have calmed. What is the Caller optimistic about?",
        2: "Things have calmed, the Caller is certain something will break the fragile peace.",
        3: "Things have intensified, possibly for the better.",
        4: "Things have intensified, definitely for the worse.",
        5: "Fortunes are reversed; where does this leave the Caller?",
        6: "A third party has intervened, upsetting things. Who is this person to the Caller?"
    },
    'third_call': {
        1: "Something they've told you before was a lie. What is the truth? Why did they lie?",
        2: "The Caller opens up about something personal connected to their issue. What do they share?",
        3: "The Caller misunderstood something about their issue until it was too late. What was it?",
        4: "The law has become involved in the Caller's issue. How bad does it look?",
        5: "The Caller has found a strong kinship with someone unexpected. Who is it?",
        6: "The Caller has had an explosive falling-out with someone close involved. Who, and why?"
    },
    'fourth_call': {
        1: "Things ended abruptly; much was learned. What is the Caller's takeaway?",
        2: "Things ended abruptly; much still confuses the Caller. What can't they let go?",
        3: "The Caller got what they wanted. Why aren't they happy about it?",
        4: "The Caller lost everything. Why are they so strangely relieved?",
        5: "The Caller is cryptic, and confusing. What do they say that sticks with you?",
        6: "The Caller is wistful and vague. What is the last thing they say to you?"
    }
}

class CardDeck:
    def __init__(self, suits, ranks):
        self.deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def draw(self):
        return self.deck.pop() if self.deck else None

class CallerRoller:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("VOID 1680 AM - Dashboard")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.caller_deck = CardDeck(SUITS, RANKS)
        self.current_block = 0  # 0=Clubs, 1=Diamonds, 2=Spades, 3=Hearts
        
        self.caller_result = ""
        self.subject_result = ""
        self.request_result = ""
        self.multi_call_result = ""
        self.playlist_result = ""
        
        self.on_air = True
        self.wave_position = 10
        self.wave_speed = 0.25
        self.flash_active = False
        self.flash_time = 0
        self.flash_target = None
        self.flash_value = ""
        self.button_pressed = None
        self.switch_progress = 1.0
        self.history_scroll = 0
        self.history = []
        
        # Fonts
        self.font_main = pygame.font.SysFont("segoeuiemoji", 16, bold=True)
        self.font_result = pygame.font.SysFont("segoeuiemoji", 14)
        self.font_title = pygame.font.SysFont("Courier Regular", 110, bold=True, italic=True)
        self.font_block = pygame.font.SysFont("Arial", 16, bold=True)
        self.history_font = pygame.font.SysFont("Courier New", 12)
        self.credits_font = pygame.font.SysFont("Arial", 8)
        self.clock_font = pygame.font.SysFont("Courier New", 14, bold=True)
        self.font_other = pygame.font.SysFont("Courier New", 32, bold=True)
        
        self.used_playlist_prompts = {block: set() for block in PLAYLIST.keys()}
        self._init_ui_elements()
        self._init_history_log()
        self._create_overlay()

    def _init_ui_elements(self):
        # Button dimensions
        main_btn_width, btn_height = 150, 40
        small_btn_width = 60
        
        # Result box dimensions
        result_width, result_height = 200, 130
        vertical_spacing = 10
        horizontal_spacing = 70

        # Main buttons (Playlist, Caller, Subject, Request)
        group1_x = 20
        group2_x = group1_x + main_btn_width + horizontal_spacing
        group3_x = group2_x + main_btn_width + horizontal_spacing
        group4_x = group3_x + main_btn_width + horizontal_spacing

        # Create buttons
        self.playlist_button = pygame.Rect(group1_x + 25, 100, main_btn_width, btn_height)
        self.caller_button = pygame.Rect(group2_x + 25, 100, main_btn_width, btn_height)
        self.subject_button = pygame.Rect(group3_x + 25, 100, main_btn_width, btn_height)
        self.request_button = pygame.Rect(group4_x + 25, 100, main_btn_width, btn_height)
        
        # Small buttons for call types
        small_btn_spacing = 5
        group5_x = group4_x + main_btn_width + horizontal_spacing
        
        self.second_call_button = pygame.Rect(group5_x, 100, small_btn_width, btn_height)
        self.third_call_button = pygame.Rect(group5_x + small_btn_width + small_btn_spacing, 100, small_btn_width, btn_height)
        self.fourth_call_button = pygame.Rect(group5_x + 2*(small_btn_width + small_btn_spacing), 100, small_btn_width, btn_height)
            
        # Result boxes
        self.playlist_result_rect = pygame.Rect(group1_x, 100 + btn_height + vertical_spacing, result_width, result_height)
        self.caller_result_rect = pygame.Rect(group2_x, 100 + btn_height + vertical_spacing, result_width, result_height)
        self.subject_result_rect = pygame.Rect(group3_x, 100 + btn_height + vertical_spacing, result_width, result_height)
        self.request_result_rect = pygame.Rect(group4_x, 100 + btn_height + vertical_spacing, result_width, result_height)
        self.multi_call_result_rect = pygame.Rect(group5_x, 100 + btn_height + vertical_spacing, 
                                            3*small_btn_width + 2*small_btn_spacing, result_height)
    
        switch_width = 120
        switch_height = 40
        self.switch_rect = pygame.Rect((WIDTH - switch_width)-20, HEIGHT - 165, switch_width, switch_height)
        self.block_rect = pygame.Rect(20, HEIGHT-165, 200, 30)
        self.history_rect = pygame.Rect(20, HEIGHT - 105, WIDTH - 40, 85)
        
        # Block selector buttons with numbers
        self.block_buttons = []
        block_width, block_height = 50, 30
        start_x, start_y = 230, HEIGHT-165
        
        for i, suit in enumerate(SUITS):
            btn_rect = pygame.Rect(
                start_x + i * (block_width + 5),
                start_y,
                block_width,
                block_height
            )
            self.block_buttons.append(btn_rect)

    def _init_history_log(self):
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                f.write("VOID 1680 AM Log\n\nLog from " + 
                       datetime.datetime.now().strftime("%Y/%m/%d %H:%M\n\n"))
        else:
            with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
                f.write("\nLog from " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M\n\n"))

    def _create_overlay(self):
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 3):
            pygame.draw.line(self.overlay, (0, 0, 0, 100), (0, y), (WIDTH, y))
        self.overlay.fill((100, 100, 100, 100), special_flags=pygame.BLEND_MULT)

    def log_history(self, action, result):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        entry = f"[{timestamp}] {action}: {result}"
        self.history.insert(0, entry)
        
        if len(self.history) > MAX_HISTORY_ENTRIES:
            self.history = self.history[:MAX_HISTORY_ENTRIES]
            
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(entry + "\n")

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(event.pos)
            
            if event.type == pygame.MOUSEWHEEL:
                self._handle_mouse_wheel(event)

    def _handle_mouse_click(self, pos):
        if self.switch_rect.collidepoint(pos):
            self.on_air = not self.on_air
            self.button_pressed = None
            return
            
        if not self.on_air:
            self.button_pressed = None
            return
            
        # Check block selection
        for i, btn_rect in enumerate(self.block_buttons):
            if btn_rect.collidepoint(pos):
                self.current_block = i
                self.log_history("Block", f"Selected {SUITS[i]} block")
                self.button_pressed = None
                break
                
        if self.playlist_button.collidepoint(pos):
            self.button_pressed = "playlist"
            self._roll_playlist()
            
        if self.caller_button.collidepoint(pos):
            self.button_pressed = "caller"
            self._draw_caller()
            
        if self.subject_button.collidepoint(pos):
            self.button_pressed = "subject"
            self._roll_subject()
            
        if self.request_button.collidepoint(pos):
            self.button_pressed = "request"
            self._roll_request()

        if self.second_call_button.collidepoint(pos):
            self.button_pressed = "second_call"
            self._roll_second_call()
        
        if self.third_call_button.collidepoint(pos):
            self.button_pressed = "third_call"
            self._roll_third_call()
            
        if self.fourth_call_button.collidepoint(pos):
            self.button_pressed = "fourth_call"
            self._roll_fourth_call()

    def _handle_mouse_wheel(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.history_rect.collidepoint(mouse_pos):
            new_scroll = self.history_scroll - event.y
            max_scroll = max(0, len(self.history) - MAX_VISIBLE_ENTRIES)
            self.history_scroll = max(0, min(new_scroll, max_scroll))

    def _update(self):
        self.wave_position += self.wave_speed
        if self.wave_position > 20:
            self.wave_position = 0
            
        if self.flash_active:
            self.flash_time += 1
            if self.flash_time >= 9:
                self.flash_active = False
                if self.flash_target == "playlist":
                    self.playlist_result = self.flash_value
                elif self.flash_target == "caller":
                    self.caller_result = self.flash_value
                elif self.flash_target == "subject":
                    self.subject_result = self.flash_value
                elif self.flash_target == "request":
                    self.request_result = self.flash_value
                    
        target = 1.0 if self.on_air else 0.0
        self.switch_progress += (target - self.switch_progress) * 0.2
        pygame.display.update(self._get_clock_rect())

    def _draw(self):
        self.screen.fill(COLORS['bg'])
        self._draw_title()
        self._draw_controls()
        self._draw_main_buttons()
        self._draw_result_boxes()
        self._draw_history_panel()
        self._draw_antenna()
        self._draw_clock()
        self._draw_credits()
        
        if not self.on_air:
            self._draw_off_air_message()
            self.screen.blit(self.overlay, (0, 0))
        
        pygame.display.flip()

    def _draw_title(self):
        title_text = "VOID 1860 AM DASHBOARD"
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
        
        title_x = WIDTH//2 - title_surf.get_width()//2
        self.screen.blit(shadow, (title_x + 2, 19))
        self.screen.blit(final_title, (title_x, 15))
        
    def _draw_controls(self):
        # ON/OFF switch
        bg_color = (50, 205, 50) if self.on_air else (200, 50, 50)
        border_color = (120, 255, 100) if self.on_air else (255, 120, 100)
        
        pygame.draw.rect(self.screen, bg_color, self.switch_rect, border_radius=20)
        pygame.draw.rect(self.screen, border_color, self.switch_rect, 3, border_radius=20)
        
        indicator_x = self.switch_rect.left + 20 + int(self.switch_progress * (self.switch_rect.width - 40))
        pygame.draw.circle(self.screen, (240, 240, 240), (indicator_x, self.switch_rect.centery), 12)
        
        label_text = "ON AIR" if self.on_air else "OFF AIR"
        label = self.font_main.render(label_text, True, (240, 240, 240))
        
        if self.on_air:
            text_x = self.switch_rect.left + 15
        else:
            text_x = self.switch_rect.right - label.get_width() - 15
        
        shadow = self.font_main.render(label_text, True, (0, 0, 0, 150))
        self.screen.blit(shadow, (text_x + 1, self.switch_rect.centery - shadow.get_height()//2 + 1))
        self.screen.blit(label, (text_x, self.switch_rect.centery - label.get_height()//2))
        
        # Current block display with number and suit
        pygame.draw.rect(self.screen, COLORS['block']['current'], self.block_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 150), self.block_rect, 2, border_radius=5)
        
        block_text = f"Current Block: {self.current_block + 1} {SUITS[self.current_block]}"
        block_surf = self.font_block.render(block_text, True, (220, 220, 220))
        self.screen.blit(block_surf, (self.block_rect.x + 10, self.block_rect.centery - block_surf.get_height()//2))
        
        # Block selector buttons with numbers
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (btn_rect, suit) in enumerate(zip(self.block_buttons, SUITS)):
            bg_color = COLORS['block']['current'] if self.current_block == i else COLORS['block']['other']
            border_color = (100, 100, 150) if self.current_block == i else (70, 70, 100)
            
            pygame.draw.rect(self.screen, bg_color, btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, border_color, btn_rect, 2, border_radius=5)
            
            # Display block number and suit
            btn_text = f"{i+1} {suit}"
            text_surf = self.font_block.render(btn_text, True, (220, 220, 220))
            text_rect = text_surf.get_rect(center=btn_rect.center)
            self.screen.blit(text_surf, text_rect)
            
            if btn_rect.collidepoint(mouse_pos) and self.current_block != i:
                highlight = pygame.Surface((btn_rect.width, btn_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(highlight, (255, 255, 255, 30), highlight.get_rect(), border_radius=5)
                self.screen.blit(highlight, btn_rect)

    def _draw_result_box(self, rect, text, bg_color, flash_color, border_color):
        current_bg = flash_color if flash_color else bg_color
        pygame.draw.rect(self.screen, current_bg, rect, border_radius=5)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)
        
        if text:
            # Use textwrap to handle long lines
            lines = []
            for line in text.split('\n'):
                if self.font_result.size(line)[0] <= rect.width - 10:
                    lines.append(line)
                else:
                    # Manually wrap long lines
                    words = line.split(' ')
                    wrapped_line = words[0]
                    for word in words[1:]:
                        test_line = wrapped_line + ' ' + word
                        if self.font_result.size(test_line)[0] <= rect.width - 10:
                            wrapped_line = test_line
                        else:
                            lines.append(wrapped_line)
                            wrapped_line = word
                    lines.append(wrapped_line)
            
            # Display the wrapped text
            for i, line in enumerate(lines[:8]):
                text_surf = self.font_result.render(line, True, (220, 220, 220))
                self.screen.blit(text_surf, (rect.x + 5, rect.y + 5 + i * 20))

    def _draw_main_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Main buttons
        self._draw_button(self.playlist_button, "PLAYLIST", COLORS['playlist'], 
                        self.playlist_button.collidepoint(mouse_pos), 
                        self.button_pressed == "playlist")
                        
        self._draw_button(self.caller_button, "ROLL CALLER", COLORS['caller'], 
                        self.caller_button.collidepoint(mouse_pos), 
                        self.button_pressed == "caller")
                        
        self._draw_button(self.subject_button, "SUBJECT", COLORS['subject'], 
                        self.subject_button.collidepoint(mouse_pos), 
                        self.button_pressed == "subject")
                        
        self._draw_button(self.request_button, "REQUEST", COLORS['request'], 
                        self.request_button.collidepoint(mouse_pos), 
                        self.button_pressed == "request")
        
        # Small recaller buttons
        self._draw_button(self.second_call_button, "2ND", COLORS['second_call'], 
                        self.second_call_button.collidepoint(mouse_pos),
                        self.button_pressed == "second_call")
        
        self._draw_button(self.third_call_button, "3RD", COLORS['third_call'], 
                        self.third_call_button.collidepoint(mouse_pos),
                        self.button_pressed == "third_call")
        
        self._draw_button(self.fourth_call_button, "4TH", COLORS['fourth_call'], 
                        self.fourth_call_button.collidepoint(mouse_pos),
                        self.button_pressed == "fourth_call")

    def _draw_button(self, rect, text, colors, is_hovered, is_pressed):
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
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=corner_radius)
        button_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(button_surface, draw_rect)
        
        pygame.draw.rect(self.screen, colors['border'], draw_rect, 3, border_radius=corner_radius)
        
        if is_hovered and not is_pressed:
            shine_height = draw_rect.height//4
            shine_surface = pygame.Surface((draw_rect.width, shine_height), pygame.SRCALPHA)
            pygame.draw.rect(shine_surface, BUTTON_SHINE, shine_surface.get_rect(), 
                        border_top_left_radius=corner_radius, 
                        border_top_right_radius=corner_radius)
            self.screen.blit(shine_surface, draw_rect)
        
        text_color = (240, 240, 240)
        text_surf = self.font_main.render(text, True, text_color)
        text_pos = (draw_rect.centerx - text_surf.get_width()//2, 
                draw_rect.centery - text_surf.get_height()//2 + (1 if is_pressed else 0))
        
        shadow_surf = self.font_main.render(text, True, (0, 0, 0, 255))
        self.screen.blit(shadow_surf, (text_pos[0]+1, text_pos[1]+1))
        self.screen.blit(text_surf, text_pos)
        
        if is_hovered and not is_pressed:
            glow_intensity = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 40
            glow_color = (*colors['border'], glow_intensity)
            glow_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=corner_radius)
            self.screen.blit(glow_surf, draw_rect)

    def _draw_result_boxes(self):
        # Result boxes
        self._draw_result_box(self.playlist_result_rect, self.playlist_result, 
                            COLORS['playlist']['result'], 
                            COLORS['playlist']['flash'] if self.flash_active and self.flash_target == "playlist" else None, 
                            COLORS['playlist']['border'])
                            
        self._draw_result_box(self.caller_result_rect, self.caller_result, 
                            COLORS['caller']['result'], 
                            COLORS['caller']['flash'] if self.flash_active and self.flash_target == "caller" else None, 
                            COLORS['caller']['border'])
                            
        self._draw_result_box(self.subject_result_rect, self.subject_result, 
                            COLORS['subject']['result'], 
                            COLORS['subject']['flash'] if self.flash_active and self.flash_target == "subject" else None, 
                            COLORS['subject']['border'])
                            
        self._draw_result_box(self.request_result_rect, self.request_result, 
                            COLORS['request']['result'], 
                            COLORS['request']['flash'] if self.flash_active and self.flash_target == "request" else None, 
                            COLORS['request']['border'])
        
        self._draw_result_box(self.multi_call_result_rect, self.multi_call_result,
                            COLORS['multi_call']['result'],
                            COLORS['multi_call']['flash'] if self.flash_active and self.flash_target in ["second_call", "third_call", "fourth_call"] else None,
                            COLORS['multi_call']['border'])

    def _draw_history_panel(self):
        pygame.draw.rect(self.screen, COLORS['history']['bg'], self.history_rect, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['history']['border'], self.history_rect, 1, border_radius=5)
        
        history_title = self.font_main.render("HISTORY", True, (200, 200, 220))
        self.screen.blit(history_title, (self.history_rect.x + 10, self.history_rect.y - 20))
        
        for i in range(MAX_VISIBLE_ENTRIES):
            entry_idx = self.history_scroll + i
            if entry_idx < len(self.history):
                entry = self.history_font.render(self.history[entry_idx], True, COLORS['history']['text'])
                self.screen.blit(entry, (self.history_rect.x + 5, self.history_rect.y + 5 + i * 15))

    def _draw_credits(self):
        credits_text = "Program by Matthew Wrisley | 'VOID 1680 AM' by Ken Lowery & © 2023 Bannerless Games"
        credits_surface = self.credits_font.render(credits_text, True, (80, 80, 80))
        self.screen.blit(credits_surface, (10, HEIGHT - 15))
        self.screen.blit(credits_surface, (10, HEIGHT - 15))

    def _draw_off_air_message(self):
        msg = self.font_other.render("Switch to \"ON AIR\" to interact", True, (255, 100, 100))
        self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 135))

    def _flash_result(self, target, value):
        self.flash_active = True
        self.flash_time = 0
        self.flash_target = target
        self.flash_value = value
        
        if target == "playlist":
            self.playlist_result = ""
        elif target == "caller":
            self.caller_result = ""
        elif target == "subject":
            self.subject_result = ""
        elif target == "request":
            self.request_result = ""
        elif target in ["second_call", "third_call", "fourth_call"]:
            self.multi_call_result = ""
            
    def _roll_playlist(self):
        # Get the current block's playlist
        block_names = ['clubs_1_block', 'diamonds_2_block', 'spades_3_block', 'hearts_4_block']
        current_block_name = block_names[self.current_block]
        playlist = PLAYLIST[current_block_name]
        
        # Get available prompts (2-10) that haven't been used
        available = [k for k in playlist.keys() if k not in self.used_playlist_prompts[current_block_name]]
        
        if not available:
            result = "All playlist prompts used!\nReshuffling..."
            self.used_playlist_prompts[current_block_name] = set()  # Reset used prompts
            self._flash_result("playlist", result)
            return
        
        # Select a random available prompt
        roll = random.choice(available)
        self.used_playlist_prompts[current_block_name].add(roll)
        prompt = playlist[roll]
        
        # Map roll to card rank
        rank_map = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
                    7: '7', 8: '8', 9: '9', 10: '10'}
        rank = rank_map.get(roll, str(roll))
        
        result = f"Playlist Prompt:\n{rank} of {SUITS[self.current_block]}\n{prompt}"
        self._flash_result("playlist", result)
        self.log_history("Playlist", f"Rolled {roll} in {current_block_name}")
        self.button_pressed = None

    def _draw_caller(self):
        card = self.caller_deck.draw()
        
        if card:
            try:
                rank, suit = card.split(' of ')
                suit = suit.strip()
                
                # Get basic info
                age_desc = CALLER_RULES['rank'].get(rank, "Unknown age")
                
                # Determine relationship to music
                current_suit = SUITS[self.current_block]
                next_suit = SUITS[(self.current_block + 1) % 4]
                
                music_relation = ""
                if suit == current_suit:
                    music_relation = "Calling about something you've played"
                elif suit == next_suit:
                    music_relation = "Calling to make a request"
                else:
                    music_relation = "Just wants to talk"
                
                result = f"{card}\nAge: {age_desc}\nSuit: {suit}\nRelation: {music_relation}"
                self._flash_result("caller", result)
                self.log_history("Caller", card)
            except:
                self._flash_result("caller", card)
                self.log_history("Caller", card)
        else:
            self._flash_result("caller", "Deck empty!")
            self.log_history("Caller", "Deck empty!")
        
        self.button_pressed = None

    def _roll_subject(self):
        if not self.caller_result:
            self._flash_result("subject", "Roll a caller first!")
            self.button_pressed = None
            return
            
        try:
            card = self.caller_result.split('\n')[0]
            suit = card.split(' of ')[1].strip()
            
            if suit not in CALLER_RULES['subject']:
                self._flash_result("subject", "Invalid suit!")
                return
                
            subject_roll = random.randint(1, 6)
            subject_info = CALLER_RULES['subject'][suit]
            mood = subject_info['mood']
            subject = subject_info[subject_roll]
            
            result = f"Mood: {mood}\nSubject: {subject}\n(Rolled {subject_roll})"
            self._flash_result("subject", result)
            self.log_history("Subject", f"{card}: {subject}")
        except:
            self._flash_result("subject", "Error generating subject")
            
        self.button_pressed = None

    def _roll_request(self):
        if not self.caller_result:
            self._flash_result("request", "Roll a caller first!")
            self.button_pressed = None
            return
            
        try:
            card = self.caller_result.split('\n')[0]
            suit = card.split(' of ')[1].strip()
            current_suit = SUITS[self.current_block]
            next_suit = SUITS[(self.current_block + 1) % 4]
            
            if suit != next_suit:
                self._flash_result("request", "Caller isn't making a request!")
                return
                
            request_roll = random.randint(1, 6)
            request = CALLER_RULES['request'][request_roll]
            
            result = f"Song Request:\n{request}\n(Rolled {request_roll})"
            self._flash_result("request", result)
            self.log_history("Request", f"{card}: {request}")
        except:
            self._flash_result("request", "Error generating request")
            
        self.button_pressed = None

    def _roll_second_call(self):
        roll = random.randint(1, 6)
        result = f"2nd Call Outcome:\n{CALLER_RULES['second_call'][roll]}\n(Rolled {roll})"
        self._flash_result("second_call", result)
        self.multi_call_result = result
        self.log_history("2nd Call", f"Rolled {roll}")
        self.button_pressed = None

    def _roll_third_call(self):
        roll = random.randint(1, 6)
        result = f"3rd Call Outcome:\n{CALLER_RULES['third_call'][roll]}\n(Rolled {roll})"
        self._flash_result("third_call", result)
        self.multi_call_result = result
        self.log_history("3rd Call", f"Rolled {roll}")
        self.button_pressed = None

    def _roll_fourth_call(self):
        roll = random.randint(1, 6)
        result = f"4th Call Outcome:\n{CALLER_RULES['fourth_call'][roll]}\n(Rolled {roll})"
        self._flash_result("fourth_call", result)
        self.multi_call_result = result
        self.log_history("4th Call", f"Rolled {roll}")
        self.button_pressed = None

    def _draw_antenna(self):
        center_x = WIDTH // 2
        tower_top = 360
        
        # Draw tower base and supports
        pygame.draw.line(self.screen, (136, 136, 136), (center_x, tower_top + 7), (center_x, tower_top - 45), 3)
        pygame.draw.line(self.screen, (68, 68, 68), (center_x - 10, tower_top + 7), (center_x + 10, tower_top + 7), 5)
        
        support_color = (127, 128, 159)
        pygame.draw.line(self.screen, support_color, (center_x - 38, tower_top + 7), (center_x, tower_top - 45), 1)
        pygame.draw.line(self.screen, support_color, (center_x + 38, tower_top + 7), (center_x, tower_top - 45), 1)
        pygame.draw.line(self.screen, support_color, (center_x - 20, tower_top + 7), (center_x, tower_top - 25), 1)
        pygame.draw.line(self.screen, support_color, (center_x + 20, tower_top + 7), (center_x, tower_top - 25), 1)
        
        # Only draw waves when on air
        if self.on_air:
            for i in range(3):
                offset = self.wave_position + (i * 20) + 10
                
                # Draw the wave arcs
                pygame.draw.arc(self.screen, (219, 222, 231), 
                            (center_x - offset + 3, tower_top - 65 - (i * 15), 
                            offset * 2, 30 + (i * 30)),
                            math.radians(155), math.radians(205), 1)
                
                pygame.draw.arc(self.screen, (219, 222, 231), 
                            (center_x - offset, tower_top - 65 - (i * 15), 
                            offset * 2, 30 + (i * 30)),
                            math.radians(-25), math.radians(25), 1)
                
                # Draw the red indicator light
                pygame.draw.circle(self.screen, (245, 35, 85), (center_x + 1, tower_top - 50), 6)
        else:
            # Draw gray indicator light when off air
            pygame.draw.circle(self.screen, support_color, (center_x + 1, tower_top - 50), 6)

    def _draw_clock(self):
        local_time = datetime.datetime.now().strftime("  %H:%M")
        utc_time = datetime.datetime.utcnow().strftime("  %H:%M")
        
        local_label = self.clock_font.render("LOCAL:", True, (200, 200, 220))
        local_time_surf = self.clock_font.render(local_time, True, (200, 200, 220))
        utc_label = self.clock_font.render("UTC:", True, (200, 200, 220))
        utc_time_surf = self.clock_font.render(utc_time, True, (200, 200, 220))

        clock_x = self.switch_rect.x - 250
        clock_y = self.switch_rect.y
        clock_width = 115
        clock_height = 40

        clock_rect = pygame.Rect(clock_x - 5, clock_y - 2, clock_width + 11, clock_height)
        pygame.draw.rect(self.screen, COLORS['history']['bg'], clock_rect, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['history']['border'], clock_rect, 1, border_radius=5)
        
        self.screen.blit(local_label, (clock_x, clock_y))
        self.screen.blit(local_time_surf, (clock_x + 60, clock_y))
        self.screen.blit(utc_label, (clock_x, clock_y + 20))
        self.screen.blit(utc_time_surf, (clock_x + 60, clock_y + 20))

    def _get_clock_rect(self):
        # Returns the rectangle area occupied by the clock
        clock_x = self.switch_rect.x + 250
        clock_y = self.switch_rect.y - 100
        return pygame.Rect(clock_x, clock_y, 200, 100)

if __name__ == "__main__":
    app = CallerRoller()
    app.run()
