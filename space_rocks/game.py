import pygame
from pygame import Color
from models import Spaceship, Asteroid, Bullet
from utils import load_sprite , get_random_position, print_text

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    SPAWN_TIME = 120
    SHIELD_PULSE = 60

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.play_again = True
        self.setup_new_game()



    def setup_new_game(self):
        self.shield_pulse_time = 0
        self.time_to_spawn = 0
        self.destroyed_asteroids = 0
        self.message = ""
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)


        for _ in range(1):
            self.spawn_asteroid()


    def spawn_asteroid(self):
        while True:
            position = get_random_position(self.screen)
            if (
                position.distance_to(self.spaceship.position)
                > self.MIN_ASTEROID_DISTANCE
            ):
                break
        self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while self.play_again == True:
            self._handle_input()
            self._process_game_logic()
            self._draw()




    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and self.spaceship:
                self.spawn_asteroid()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and not self.spaceship :
                self.spaceship = Spaceship((400, 300), self.bullets.append)
                self.message = ""

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.setup_new_game()




        is_key_pressed = pygame.key.get_pressed()
        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.decelerate()
            if is_key_pressed[pygame.K_b]:
                self.spaceship.emergency_brake()



    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    if self.spaceship.shield == 0:
                        self.spaceship = None
                        self.message = "Przegrałeś!"
                        break
                    else:
                        self.asteroids.remove(asteroid)
                        self.spaceship.shield = 0
                        asteroid.split()
                        self.destroyed_asteroids += 1

        #self.asteroid.move()
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    self.destroyed_asteroids += 1
                    break

            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "Wygrałeś!"

        self.time_to_spawn += 1
        if self.time_to_spawn == self.SPAWN_TIME and self.spaceship:
            self.spawn_asteroid()
            self.time_to_spawn = 0

        self.shield_pulse_time += 1
        if self.shield_pulse_time == 60:
            self.shield_pulse_time = 0



    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.spaceship and self.spaceship.shield == 1 :
            color = (255, 100 + 155 * (self.shield_pulse_time/self.SHIELD_PULSE), 0+ 255 * (self.shield_pulse_time/self.SHIELD_PULSE))
            pygame.draw.circle(self.screen, color, self.spaceship.position, self.spaceship.radius+3, 2)

        if self.message:
            print_text(self.screen, self.message, self.font)

        print_text(self.screen, str(self.destroyed_asteroids), self.font, (770,30))
        # if self.spaceship:
        #     print_text(self.screen, str(self.spaceship.shield), self.font, (570,30))

        #print_text(self.screen, str(self.SPAWN_TIME - self.time_to_spawn), self.font, (570,30))

        print_text(self.screen, str(self.shield_pulse_time), self.font, (570,30))

        pygame.display.flip()
        self.clock.tick(60)



    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
