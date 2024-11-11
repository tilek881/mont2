from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.health} damage: {self.damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if type(hero) == Berserk and self.__defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    @property
    def defence(self):
        return self.__defence

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes):
        crit = self.damage * randint(2, 5)
        boss.health -= crit
        print(f'Warrior {self.name} hit critically {crit} to boss.')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')

    def apply_super_power(self, boss, heroes):
        pass


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_DAMAGE_AND_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} to boss.')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


round_number = 0


def show_statistics(boss, heroes):
    print(f'ROUND - {round_number} ------------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def start_game():
    boss = Boss(name='Dragon', health=1000, damage=50)
    warrior_1 = Warrior(name='Mario', health=270, damage=10)
    warrior_2 = Warrior(name='Ben', health=280, damage=15)
    magic = Magic(name='Merlin', health=290, damage=10)
    berserk = Berserk(name='Guts', health=260, damage=5)
    doc = Medic(name='Aibolit', health=250, damage=5, heal_points=15)
    assistant = Medic(name='Kristin', health=300, damage=5, heal_points=5)
    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
