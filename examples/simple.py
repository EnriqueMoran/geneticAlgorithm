import geneticAlgorithm as GA
import time

if __name__ == "__main__":   

    # Simple instances, with default values

    genetic1 = GA.GA(10, 6, 0.3, 0.1, 500)    # Population size = 10, chromosome len = 6, mutation probability = 0.3, crossover probability = 0.1, max generations = 500
    genetic2 = GA.GA(10, 6, 0.3, 0.1, 500, 0.4)    # Tournament elements = 40% of population

    #print("Instance 1: ", vars(genetic1))
    #print("Instance 2: ", vars(genetic2))


    # Setting crossover and mutation policy

    genetic3 = GA.GA(10, 6, 0.3, 0.1, 500, 0.1, crossover_policy = "multi_crossover")    # Crossover values: "point_crossover", "multi_crossover", "uniform_crossover"
    genetic4 = GA.GABinary(10, 6, 0.3, 0.1, 500, mutation_policy = "swap_mutation")    # Mutation values: "swap_mutation", "scramble_mutation", "inversion_mutation"
    genetic5 = GA.GABinary(10, 6, 0.3, 0.1, 500, crossover_policy = "uniform_crossover", mutation_policy = "scramble_mutation") 
    genetic6 = GA.GA(10, 6, 0.3, 0.1, 500, crossover_policy = "multi_crossover", mutation_policy = "inversion_mutation")

    #print("\nInstance 3: ", vars(genetic3))
    #print("Instance 5: ", vars(genetic5))


    # Using custom values for chromosomes

    genetic7 = GA.GACustom(5, 6, 0.3, 0.1, 500, crossover_policy = "multi_crossover", mutation_policy = "inversion_mutation", chromosome_values = [i for i in range(0, 10)], gen_duplication = True)
    genetic8 = GA.GACustom(10, 10, 0.3, 0.2, 200, crossover_policy = "cyclical_crossover", mutation_policy = "swap_mutation", chromosome_values = [i for i in range(0, 10)], gen_duplication = False)
    genetic9 = GA.GACustom(10, 11, 0.3, 0.1, 500, crossover_policy = "multi_crossover", mutation_policy = "inversion_mutation", chromosome_values = [i for i in range(0, 10)], gen_duplication = False)
    genetic10 = GA.GACustom(5, 5, 0.2, 0.6, 500, crossover_policy = "multi_crossover", mutation_policy = "inversion_mutation", chromosome_values = ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"], gen_duplication = True)

    #print("\nInstance 7 initial population: ", genetic7.initialPopulation())
    #print("Instance 10 initial population: ", genetic10.initialPopulation(),  str("\n"))
    

    # Example of usage

    # The alrogithm will sort a list of 25 numbers
    example = GA.GACustom(200, 30, 0.2, 0.4, 150, 0.5, crossover_policy = "cyclical_crossover", mutation_policy = "swap_mutation", chromosome_values = [i for i in range(0, 30)], gen_duplication = False)


    # Definning fitness function

    def fitness_example(chromosome):
        res = 0
        for a, b in zip(chromosome, chromosome[1:]):
            if b >= a:
                res += b
            else:
                res -= (a - b) * a
        return res

    example.fitness = fitness_example    # Adding our fitness function to class methods

    print("To see the result uncomment next lines.\n")
    t0 = time.time()
    sol = example.solve()
    t1 = time.time()
    print("\nSolution: ", sol, " fitness: ", str(example.fitness(sol)), " algorithm took ", str(t1 - t0), " seconds.")
    example.fitnessPlot()
