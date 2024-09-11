import random

from functions import div_by_zero, singleton
from typing import Generator


@singleton
class Game(object):
    def __init__(self) -> None:
        """
        Initializes a new game instance.

        Attributes:
        counter (int): A counter for game ticks.
        paused (bool): Indicates if the game is paused.
        fps_animate (int): Frames per second for animations.
        fps (int): General frames per second for the game.
        animate_divider (float): Divider for animation frames.
        player (FightUnit): The player's character.
        npcs (list): A list of non-player characters (NPCs).
        enviroment (list): A list representing the game environment.
        """
        self.counter = 0
        self.paused = True
        self.fps_animate = 10
        self.fps = 30
        self.animate_divider = self.fps / self.fps_animate
        self.player = FightUnit("4", x=120, y=130, speed=20)
        self.npcs = [
            FightUnit("1", x=20, y=30, speed=4.4),
            FightUnit("2", x=20, y=30, speed=3.4),
            FightUnit("3", x=20, y=30, speed=2.4),
        ]
        self.enviroment = []

    def step(self) -> None:
        """
        Executes a single step in the game, updating NPC movements.
        """
        for npc in self.npcs:
            npc.step()


class FightUnit(object):
    neighbour = [
        (-1, 0), (-1, 1),
        (0, 1), (1, 1),
        (1, 0), (1, -1),
        (0, -1), (-1, -1)
    ]

    def __init__(self, name: str, **args) -> None:
        """
        Initializes a fight unit (player or NPC).

        Parameters:
        name (str): The name of the unit.
        **args: Additional attributes such as position and speed.
        """
        self.name = name
        self.speed = 1
        self.x = 0.0
        self.y = 0.0
        self.program = self.program_go_to(1500, 1500)
        self.active_target = None
        self.last_enemy = None
        for k, v in args.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        """
        Returns a string representation of the fight unit's attributes.
        """
        return '\n'.join(["%s: %s" % (k, v) for k, v in self.__dict__.items()])

    def step(self) -> None:
        """
        Advances the unit's program by one step.
        """
        self.program.next()

    def program_stay(self, ticks: int) -> Generator:
        """
        Keeps the unit in place for a specified number of ticks.

        Parameters:
        ticks (int): The number of ticks to stay in place.
        """
        while True:
            for i in range(1, ticks):
                yield None
            self.program = self.program_walking()

    def program_walking(self) -> Generator:
        """
        Moves the unit randomly within its environment.
        """
        while True:
            dx, dy = random.choice(self.neighbour)
            s = random.randrange(100)
            for i in range(1, s):
                self.x += dx * self.speed
                self.y += dy * self.speed
                yield None
            if not 0 < self.x < 600:
                self.program = self.program_go_to(1300, 1300)
            if not 0 < self.y < 600:
                self.program = self.program_go_to(1300, 1300)

    def program_go_to(self, x, y) -> Generator:
        """
        Moves the unit towards a specified target position.

        Parameters:
        x (int): The target X coordinate.
        y (int): The target Y coordinate.
        """
        while True:
            dy = div_by_zero(y - self.y, abs(y - self.y))
            dx = div_by_zero(x - self.x, abs(x - self.x))

            if abs(y - self.y) < 2 and abs(x - self.x) < 1:
                self.program = self.program_stay(300)

            self.x += dx * self.speed
            self.y += dy * self.speed
            yield None

    def order_to_go(self, dx: float, dy: float) -> None:
        """
        Orders the unit to move by specified deltas.

        Parameters:
        dx (float): Change in X.
        dy (float): Change in Y.
        """
        self.x += dx * self.speed
        self.y += dy * self.speed

    def get_stats(self):
        """
        Placeholder for getting unit statistics.
        """
        pass

    def get_pos(self) -> tuple:
        """
        Returns the current position of the unit.

        Returns:
        tuple: The current (x, y) position of the unit.
        """
        return (self.x, self.y)

    def attack(self) -> None:
        """
        Executes an attack by the unit, targeting its active target.
        """
        print(self.name, ": arrgh!!!")
        if self.active_target is not None:
            self.active_target.be_attacked(self, Damage())
        else:
            print("I have no target")
            self.fight.remove_fighter(self)

    def be_attacked(self, enemy: "FightUnit", damage: "Damage"):
        """
        Processes an attack against the unit.

        Parameters:
        enemy (FightUnit): The attacking unit.
        damage (Damage): The damage inflicted.
        """
        self.hp -= damage.power * (100 - self.armor) / 100
        self.last_enemy = enemy
        print(self.name, ": I got %i %s damage" % (damage.power,
              damage.type), "my hp = ", self.hp)
        if self.hp <= 0:
            self.fight.remove_fighter(self)
            print(self.name, "is dead")

    def select_active_target(self) -> None:
        """
        Selects the last enemy as the active target if still valid.
        """
        if self.last_enemy in self.fight.fighters:
            self.active_target = self.last_enemy
        else:
            self.active_target = None

    def set_active_target(self, target: "FightUnit") -> None:
        """
        Sets the active target for the unit.

        Parameters:
        target (FightUnit): The target to attack.
        """
        self.active_target = target

    def begin_fight(self, target: "FightUnit") -> None:
        """
        Initiates a fight with the specified target.

        Parameters:
        target (FightUnit): The target to fight against.

        Returns:
        Fight: A new fight instance with the unit and target.
        """
        self.set_active_target(target)
        target.set_active_target(self)
        return Fight([self, target])


class Damage(object):
    def __init__(self) -> None:
        """
        Initializes damage attributes.

        Attributes:
        type (str): The type of damage (default is "physical").
        power (int): The power of the damage (default is 30).
        """
        self.type = "physical"
        self.power = 30


class Fight(object):
    def __init__(self, fighters: list) -> None:
        """
        Initializes a fight instance with the specified fighters.

        Parameters:
        fighters (list): A list of fighters participating in the fight.
        """
        self.fighters = fighters
        self._iterator = 0
        for fighter in fighters:
            fighter.fight = self

    def __repr__(self) -> str:
        """
        Returns a string representation of the fight.
        """
        return "In fight:" + ' '.join(
            [fighter.name for fighter in self.fighters])

    def step(self) -> None:
        """
        Executes a single step in the fight,
        allowing the current fighter to attack.
        """
        self.fighters[self._iterator].attack()
        self._iterator += 1
        self._iterator = self._iterator % len(self.fighters)

    def add_fighter(self, fighter: FightUnit) -> None:
        """
        Adds a fighter to the fight.

        Parameters:
        fighter (FightUnit): The fighter to add.
        """
        self.fighters.append(fighter)
        fighter.fight = self

    def remove_fighter(self, fighter: FightUnit) -> None:
        """
        Removes a fighter from the fighters list.

        Parameters:
        fighter (FightUnit): The fighter to remove.
        """
        i = self.fighters.index(fighter)
        if i <= self._iterator:
            self._iterator -= 1
        del self.fighters[i]

        fighter.fight = None
        fighter.last_enemy = None

    def is_active(self) -> bool:
        """
        Checks if the fight is still active.

        Returns:
        bool: True if there is more than one fighter in the fight,
              indicating that the fight can continue;
              otherwise, returns False.
        """
        if len(self.fighters) > 1:
            return True
        else:
            return False
