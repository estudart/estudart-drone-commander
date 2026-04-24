import pygame
import sys

class KeyboardListener:
    def __init__(self):
        pygame.init()
        self.running = False
        self.screen = pygame.display.set_mode((800, 600))

    async def handle_keydown(self, event: event.key):
        return event.key

    async def start_loop(self):
        self.running = True
        pygame.display.set_caption("Keyboard Events Boilerplate")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    await self.handle_keydown(event.key)