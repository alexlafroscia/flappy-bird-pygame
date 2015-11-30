ANIMATION_SPEED = 0.18  # pixels per millisecond
FPS = 60
WIN_HEIGHT = 512
WIN_WIDTH = 284 * 2     # BG image size: 284x512 px; tiled twice


def get_pipe_middle(pipe):
    """
    Find the height of the middle of the gap in a pair of pipes
    """
    gap_height = WIN_HEIGHT - pipe.bottom_height_px - pipe.top_height_px
    return pipe.top_height_px + (gap_height / 2)


class Action(object):
    pass


class GameState(object):
    """
    The state of the game during one "tick"

    Attibutes:
        bird_state_x (int): the bird's x-coordinate
        bird_state_y (int): the bird's y-coordinate
    """

    def __init__(self, bird, pipe):
        self.bird_state_y = bird.y_coord
        self.pipe_middle = get_pipe_middle(pipe)
        self.pipe_distance = pipe.x - bird.x_coord

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return (hash(self.bird_state_y) << 2) ^ (
                hash(self.pipe_middle) << 1) ^ (
                hash(self.pipe_distance))


class GameStates(dict):
    """
    List of Game States

    Attributes:
        last_state (GameState): the last state to be added
    """

    def __init__(self):
        super().__init__(self)
        self.last_state = None

    def new_state(self, bird, pipe):
        if pipe or pipe.x < 0:
            state = GameState(bird, pipe)
            if state not in self:
                self[state] = list()
            self.last_state = state

    @property
    def should_jump(self):
        """
        Whether or not the bird should jump on the current tick
        """
        return False

    def add_result(self):
        pass
