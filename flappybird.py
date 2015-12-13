#! /usr/bin/env python3

"""Flappy Bird, implemented using Pygame."""

from collections import deque

import pygame
from pygame.locals import *

from game_state import GameState, Action, FPS, WIN_HEIGHT, WIN_WIDTH
from bird import Bird
from pipe import PipePair
from util import load_images, msec_to_frames, get_action_from_event

PICK_ACTION_EVERY = 20


def main():
    """The application's entry point.

    If someone executes this module (instead of importing it, for
    example), this function is called.
    """

    pygame.init()
    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pygame Flappy Bird')
    score_font = pygame.font.SysFont(None, 32, bold=True)  # default font
    images = load_images()
    scores = list()
    active = True

    while active:
        clock = pygame.time.Clock()
        bird = Bird(50, int(WIN_HEIGHT / 2 - Bird.HEIGHT / 2), 2,
                    (images['bird-wingup'], images['bird-wingdown']))
        pipes = deque()
        frame_clock = 0
        score = 0

        # Current state
        current_state = None
        action = None
        reward = 0
        collision = False
        while True:
            action_on_this_tick = frame_clock % PICK_ACTION_EVERY == 0

            clock.tick(FPS)

            if action_on_this_tick or collision:
                next_state = GameState(bird, pipes)

                # Update the values for the last state (current_state)
                if (current_state is not None and action is not None):
                    # Get the value for the reward
                    if collision:
                        reward = -10000
                    elif active and not collision:
                        reward = PICK_ACTION_EVERY

                    # Log current state
                    with current_state.take_action(action) as u:
                        u.update_utility_value(next_state, reward)

                    # Now that we have updated the state, quit the game after a
                    # collision
                    if collision:
                        break

                    # Reset the action
                    action = None

                # The "next" state will by the "current" state next time around
                current_state = next_state

            if not frame_clock % msec_to_frames(PipePair.ADD_INTERVAL):
                pp = PipePair(images['pipe-end'], images['pipe-body'])
                pipes.append(pp)

            # Handle the user quitting the game
            for event in pygame.event.get():
                action = get_action_from_event(event)
                if action is Action.quit:
                    exit()

            if not action and action_on_this_tick:
                action = current_state.max_value_action
                if action is Action.flap:
                    bird.flap()

            for x in (0, WIN_WIDTH / 2):
                display_surface.blit(images['background'], (x, 0))

            while pipes and not pipes[0].visible:
                pipes.popleft()

            for p in pipes:
                p.update()
                display_surface.blit(p.image, p.rect)

            bird.update()
            display_surface.blit(bird.image, bird.rect)

            if bird.check_collisions(pipes):
                collision = True

            # update and display score
            for p in pipes:
                if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
                    score += 1
                    p.score_counted = True

            score_surface = score_font.render(str(score), True,
                                              (255, 255, 255))
            score_x = WIN_WIDTH / 2 - score_surface.get_width() / 2
            display_surface.blit(score_surface,
                                 (score_x, PipePair.PIECE_HEIGHT))

            pygame.display.flip()
            frame_clock += 1
        scores.append(score)
        print('Game #{}:\t{}'.format(len(scores), score))
    print('Best score: %i' % max(scores))
    pygame.quit()


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'flappybird'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
