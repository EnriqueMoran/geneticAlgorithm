import random
import pygame
import math
import time
import geneticAlgorithm as GA


class Test():

    def __init__(self, display_width, display_heigth, fps, triangle_x, triangle_y, speed, objective_list, obstacle_list = None):
        self.display_width = display_width
        self.display_heigth = display_heigth
        self.fps = fps
        self.initial_x = triangle_x
        self.initial_y = triangle_y
        self.triangle_x = triangle_x    # Initial coordinates
        self.triangle_y = triangle_y
        self.triangle_image = pygame.image.load("triangle_image.png")
        self.objective_image1 = pygame.image.load("objective1_image.png")
        self.objective_image2 = pygame.image.load("objective2_image.png")
        self.speed = speed
        self.obstacle_list = obstacle_list
        self.objective_list = objective_list
        self.gameDisplay = None


    def triangle(self, x, y):
        self.gameDisplay.blit(self.triangle_image, (x, y))


    def objective(self, x, y, checked):
        if checked:
            self.gameDisplay.blit(self.objective_image1 , (x, y))
        else:
            self.gameDisplay.blit(self.objective_image2 , (x, y))


    def initialize(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_heigth))
        pygame.display.set_caption('Test')
        clock = pygame.time.Clock()
        clock.tick(self.fps)


    def move(self, angle):
        radian = angle * math.pi / 180
        x_mov = self.speed * math.cos(radian)
        y_mov = self.speed * math.sin(radian)
        self.triangle_x += x_mov
        self.triangle_y += y_mov
        rotate = pygame.transform.rotate
        rotated_image = rotate(pygame.image.load("triangle_image.png"), -angle)
        self.gameDisplay.blit(rotated_image, (self.triangle_x, self.triangle_y))
        return (x_mov, y_mov)


    def checkCollision(self, t_x, t_y, o_x, o_y):    # Check if there is a collision between triangle and objective
        if t_x - 25 >= o_x + 25 or t_y - 25  >= t_y + 25 or t_x + 25 <= o_x - 25 or t_y + 25 <= o_y - 25:
            return False
        return True


    def run(self, movement_list):
        self.triangle_x = self.initial_x
        self.triangle_y = self.initial_y
        for mov in movement_list:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()    # Press ESC to exit
            self.gameDisplay.fill((255, 255, 255))    # White background
            time.sleep(0.01)
            self.move(mov)
            for obj in self.objective_list:
                if self.checkCollision(self.triangle_x, self.triangle_y, obj[0], obj[1]):
                    objective_list[obj] = True
                self.objective(obj[0], obj[1], objective_list[obj])
            time.sleep(0.15)
            pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()    # Press ESC to exit



if __name__ == "__main__":

    # Declare test parameters
    initial_x = 15
    initial_y = 15
    objective_x = 620
    objective_y = 320
    display_width = 680
    display_heigth = 400
    fps = 30
    speed = 20

    def generateObjectives(n_obj):    # Generate a list of objectives placed randomly
        res = {}
        for i in range(0, n_obj):
            rand_x = random.randrange(0, display_width - 55)
            rand_y = random.randrange(0, display_heigth - 55)
            res[(rand_x, rand_y)] = False    # (x, y) : (has triangle pass?, by default is False)
        return res

    objective_list = generateObjectives(2)    # Generate two random objectives

    test = Test(display_width, display_heigth, fps, initial_x, initial_y, speed, objective_list)    # Instanciate test
    test.initialize()    # Load test parameters

    # Instanciate genetic solution
    genetic = GA.GACustom(50, 30, 0.5, 0.6, 80, 0.4, crossover_policy = "multi_crossover", mutation_policy = "scramble_mutation", chromosome_values = [i for i in range(0, 360)], gen_duplication = True)
    

    def fitness(chromosome):    # We build our own fitness function

        def distance(x1, y1, x2, y2):
            return int(math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))

        def emulateMovement(angle):    # Return next position after moving forward in angle (does not affect the test instance)
            radian = angle * math.pi / 180
            x_mov = test.speed * math.cos(radian)
            y_mov = test.speed * math.sin(radian)
            test.triangle_x += x_mov
            test.triangle_y += y_mov
            return (x_mov, y_mov)

        res = 0
        test.triangle_x = test.initial_x
        test.triangle_y = test.initial_y
        checked = []

        constant = test.display_width * test.display_heigth
        cont = 0
        for mov in chromosome:
            cont += 1
            emulateMovement(mov)
            if test.triangle_x <= 0 or test.triangle_x > test.display_width or test.triangle_y <= 0 or test.triangle_y > test.display_heigth:
                res = 0
            for objective in objective_list:
                if objective not in checked:
                    if test.checkCollision(test.triangle_x, test.triangle_y, objective[0], objective[1]):
                        res += (constant / (distance(test.triangle_x, test.triangle_y, objective[0], objective[1]) + 0.00000001)) * len(objective_list.keys())
                        checked.append(objective)
                    else:
                        res += (constant / (distance(test.triangle_x, test.triangle_y, objective[0], objective[1]) + 0.00000001)) / cont
        return res

    genetic.fitness = fitness
    t0 = time.time()
    movement_list = genetic.solve()
    t1 = time.time()

    print("\nSolution: ", movement_list, " fitness: ", str(genetic.fitness(movement_list)), " algorithm took ", str(t1 - t0), " seconds.")

    try:
        test.run(movement_list)    # Press ESC to exit and show fitness chart
    except:
        genetic.fitnessPlot()




