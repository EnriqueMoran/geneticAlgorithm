import random
import math
import matplotlib.pyplot as plt


class GA():

    __author__: "EnriqueMoran"

    def __init__(self, population_size,  chromosome_len, mutation_prob, crossover_prob, max_generations, tournament_elements = None, **kwargs):
        self.population_size = population_size
        self.chromosome_len = chromosome_len
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.max_generations = max_generations
        self.fitness_function = None
        self.tournament_elements = tournament_elements    # K for tournament selection (value between 0.1 and 1)
        self.crossover_policy = kwargs.get('crossover_policy')    # Values: "point_crossover", "multi_crossover", "uniform_crossover"
        self.mutation_policy = kwargs.get('mutation_policy')    # Values "swap_mutation", "scramble_mutation", "inversion_mutation"
        self.fitness_registration = []    # List used for show fitness per generation chart
        self.bestChromosome_ever = []    # Register best chromosome over generations

        if self.tournament_elements == None or self.tournament_elements <= 0.4 or self.tournament_elements > 1:    # Tournament elements must be between (0.4 and 1)
            self.tournament_elements = 0.4
        if self.crossover_policy == None:
            self.crossover_policy = "point_crossover"    # Default policy
        if self.mutation_policy == None:
            self.mutation_policy = "flip"


    def initialPopulation(self): 
        pass


    def fitness(self, chromosome):
        pass


    def getBestChromosome(self, list_of_chromosomes):
        best = ([], -math.inf)
        for chromosome in list_of_chromosomes:
            chromosome_fitness = self.fitness(chromosome)
            if chromosome_fitness > best[1]:
                best = (chromosome, chromosome_fitness)
        return best[0]


    def getParents(self, population):    # Parent selection by tournament
        parents = []  
        k = self.tournament_elements
        if k == None:
            k = 0.25    # Select 1/4 of population for tournament
        n_individuals = int(round(len(population) * k))
        if len(population) > 2:
            while len(parents) < 2:
                selected = random.sample(population, n_individuals)
                if len(parents) > 0:
                    if parents[0] in selected:
                        selected.remove(parents[0])
                parent = self.getBestChromosome(selected)
                parents.append(parent)              
        else:
            parents = population
        return parents


    def crossover(self, parent1, parent2):
        if self.crossover_policy == "point_crossover":
            index = random.randint(0, len(parent1) - 1)
            return (parent1[:index] + parent2[index:], parent1[index:] + parent2[:index])

        elif self.crossover_policy == "multi_crossover":
            index1 = random.randint(0, len(parent1) - 1)
            index2 = random.randint(0, len(parent1) - 1)
            while index2 == index1 or index1 > index2:
                index1 = random.randint(0, len(parent1) - 1)
                index2 = random.randint(0, len(parent1) - 1)
            return (parent1[:index1] + parent2[index1:index2] + parent1[index2:], parent2[:index1] + parent1[index1:index2] + parent2[index2:])

        elif self.crossover_policy == "uniform_crossover":
            children = [(parent1[x], parent2[x]) if random.random() >= 0.5 else (parent2[x], parent1[x])  for x in range(0, len(parent1))]
            return ([x[0] for x in children], [x[1] for x in children])

        elif self.crossover_policy == "cyclical_crossover":
            index = random.randint(0, len(parent1) - 1)
            child1 = parent1[:-index]
            for gen in parent2:
                if gen not in child1:
                    child1 += [gen]
            child2 = parent2[:-index]
            for gen in parent1:
                if gen not in child2:
                    child2 += [gen]
            return (child1, child2)


    def mutate(self, chromosome):
        chromosome_copy = chromosome.copy()
        if self.mutation_policy == "swap_mutation":
            index1 = random.randint(0, len(chromosome) - 1)
            index2 = random.randint(0, len(chromosome) - 1)
            while index2 == index1:
                index2 = random.randint(0, len(chromosome) - 1)
            gen_a = chromosome_copy[index1]
            gen_b = chromosome_copy[index2]
            chromosome_copy[index1] = gen_b
            chromosome_copy[index2] = gen_a
            return chromosome_copy
            
        elif self.mutation_policy == "scramble_mutation":
            index1 = random.randint(0, len(chromosome) - 1)
            index2 = random.randint(0, len(chromosome) - 1)
            while index2 == index1 or index1 > index2:
                index1 = random.randint(0, len(chromosome) - 1)
                index2 = random.randint(0, len(chromosome) - 1)
            genes = chromosome_copy[index1:index2]
            random.shuffle(genes)
            return chromosome[:index1] + genes + chromosome[index2:]

        elif self.mutation_policy == "inversion_mutation":
            index1 = random.randint(0, len(chromosome) - 1)
            index2 = random.randint(0, len(chromosome) - 1)
            while index2 == index1 or index1 > index2:
                index1 = random.randint(0, len(chromosome) - 1)
                index2 = random.randint(0, len(chromosome) - 1)
            genes = chromosome_copy[index1:index2]
            genes = genes[::-1]
            return chromosome[:index1] + genes + chromosome[index2:]


    def getAverageFitness(self, population):
        res = 0
        for chromosome in population:
            res += self.fitness(chromosome)
        return round((res / len(population)), 3)


    def nextGeneration(self, population):
        new_population = []
        population_copy = population.copy()
        while len(new_population) < self.population_size:     # Get the X best chromosomes
            sorted(population_copy, key=self.fitness)
            new = population_copy[0]
            new_population.append(new)
            population_copy.remove(new)
        return new_population


    def solve(self):
        initial_population = self.initialPopulation()
        current_population = initial_population
        for i in range(0, self.max_generations):
            population_copy = current_population.copy()
            new_population = []
            mutated_population = []
            for j in range(0, int(self.population_size / 2)):
                parents = self.getParents(population_copy)
                a = parents[0]
                b = parents[1]
                population_copy.remove(a)
                try:
                    population_copy.remove(b)
                except ValueError:
                    print("Error, please re-run the algorithm")
                if random.random() <= self.crossover_prob:
                    child1, child2 = self.crossover(a, b)
                    new_population.append(child1)
                    new_population.append(child2)
                new_population.append(a)
                new_population.append(b)
            for chromosome in new_population:
                if random.random() <= self.mutation_prob:
                    mutated_chromosome = self.mutate(chromosome)
                    mutated_population.append(mutated_chromosome)
                else:
                    mutated_population.append(chromosome)
            current_population = self.nextGeneration(mutated_population)
            self.fitness_registration.append(self.getAverageFitness(current_population))    # Register fitness
            if len(self.bestChromosome_ever) == 0:
                self.bestChromosome_ever = self.getBestChromosome(current_population)
            else:
                if self.fitness(self.bestChromosome_ever) <= self.fitness(self.getBestChromosome(current_population)):
                    self.bestChromosome_ever = self.getBestChromosome(current_population)
            print("Generation: ", i, " Average fitness: ", self.getAverageFitness(current_population), "  best chromosome: ", self.getBestChromosome(current_population), " fitness: ", self.fitness(self.getBestChromosome(current_population)))
            #print("Generation: ", i, " Average fitness: ", self.getAverageFitness(current_population), " fitness: ", self.fitness(self.getBestChromosome(current_population)))
        return self.bestChromosome_ever


    def fitnessPlot(self):
        generations = [i for i in range(0, len(self.fitness_registration))]
        plt.plot(generations, self.fitness_registration)
        plt.show()



class GABinary(GA):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def initialPopulation(self): 
        population = []
        for i in range(0, self.population_size):
            population.append([1 if random.random() >= 0.5 else 0 for x in range(0, self.population_size)])
        return population            



class GACustom(GA):
    def __init__(self, *args, **kwargs):
        self.chromosome_values = kwargs.get('chromosome_values')    # List of possible values that solution can take
        self.gen_duplication = kwargs.get('gen_duplication')    # Wether different genes can take the same value (values: True / False)
        super().__init__(*args, **kwargs)
        if self.chromosome_values == None:
            self.chromosome_values = [x for x in range(0, self.chromosome_len - 1)]
        if self.gen_duplication == None:
            self.gen_duplication = True


    def initialPopulation(self):
        population = []
        if self.gen_duplication:           
            for i in range(0, self.population_size):
                population.append([random.choice(self.chromosome_values) for x in range(0, self.chromosome_len)])
            return population

        elif not self.gen_duplication and self.chromosome_len <= len(self.chromosome_values):
            for i in range(0, self.population_size):
                population.append(random.sample(self.chromosome_values, self.chromosome_len))
            return population

        elif not self.gen_duplication and self.chromosome_len > len(self.chromosome_values):
            pass # raise error