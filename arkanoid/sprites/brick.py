import itertools
import logging

import pygame

from arkanoid.util import load_png
from arkanoid.util import load_png_sequence

LOG = logging.getLogger(__name__)


class Brick(pygame.sprite.Sprite):
    """A Brick is hit and destroyed by the ball."""

    def __init__(self, colour, value, destroy_after=1, powerup_cls=None):
        """Initialise a new Brick in the specified colour.

        When a Brick is initialised with the specified colour, a file named
        'brick_<colour>.png' will be loaded from the graphics folder and must
        exist. In addition, a Brick will also attempt to load a file called
        'brick_<colour>_anim.png' from the graphics folder which will be used
        to animate the brick when Brick.animate() is called. This file is
        optional, and if it does not exist, then Brick.animate() will have no
        effect.

        Optionally specify the number of strikes by the ball that it takes to
        destroy the brick (default 1) via the destroy_after attribute. Also
        optionally specify the class of a powerup which will fall from the
        brick when the brick is destroyed by the ball - via the powerup_cls
        attribute.

        Args:
            colour:
                The colour of the brick. Note that a png file named
                'brick_<colour>.png' must exist in the graphics folder.
            value:
                The amount to add to the score when this brick is destroyed.
            destroy_after:
                The number of strikes by the ball necessary to destroy the
                brick (default 1).
            powerup_cls:
                Optional class of a PowerUp that will be used when the ball
                destroys this brick (default None).
        """
        super().__init__()
        self.colour = colour
        self.value = value
        # Load the brick graphic.
        self.image, self.rect = load_png('brick_{}'.format(colour))

        # Load the images/rects required for the shimmering animation.
        self._image_sequence = [image for image, _ in
                                load_png_sequence('brick_silver')]
        self._image_sequence.append(self.image)
        self._animation = None

        # The number of ball collisions after which the brick is destroyed.
        self._destroy_after = destroy_after

        # The number of ball collisions with this brick.
        self.collision_count = 0

        # The class of the powerup.
        self.powerup_cls = powerup_cls

        # Whether to animate the brick.
        self._animate = False

    def update(self):
        if self._animate:
            if not self._animation:
                self._animation = iter(self._image_sequence)
            try:
                self.image = next(self._animation)
            except StopIteration:
                self._animate = None

    @property
    def visible(self):
        """Whether the brick is still visible based on its collision count,
        or whether it is destroyed and no longer visible.

        Returns:
            True if the brick is visible. False otherwise.
        """
        return self.collision_count < self._destroy_after

    def animate(self):
        """Trigger animation of this brick."""
        self._animate = True
