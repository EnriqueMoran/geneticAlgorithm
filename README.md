# geneticAlgorithm
Genetic algorithm library for binary and custom chromosome

**matplotlib library is needed**


## Chromosome attributes

The atributes of a GeneticAlgorithm object are: _population size_, _chromosome len_, _mutation probability_, _crossover probability_, _max number of generations_, _tournament elements_, _crossover policy_,  _mutation policy_.

**tournament elements:** Its default value is a random number between 0.1 and 1, indicates the percentage of population that will joint the tournament for parent selection.

**crossover_policy:** Values: _point_crossover_, _multi_crossover_, _uniform_crossover_

**mutation_policy:** Values: _swap_mutation_, _scramble_mutation_, _inversion_mutation_

mutation and crossover policy must be introduced as _key, value_ pair 


## Types of chromosome

There are two different types of avaliable chromosome: _binary_ and _custom_.
Custom chromosome has two additional attributes: _chromosome_values_ and _gen_duplication_, first one is a list with the possible values for the chromosome, second one is a boolean argument to allow chromosome's gen duplicate.


## Creating an instance

The simplest instance has _population size_, _chromosome len_, _mutation probability_, _crossover probability_ and _max generations_ arguments. The rest are will take their default values:

```
genetic1 = GA.GA(10, 6, 0.3, 0.1, 500)
```
To set mutation and crossover policy follow the next example:

```
genetic6 = GA.GA(10, 6, 0.3, 0.1, 500, crossover_policy = "multi_crossover", mutation_policy = "swap_mutation")
```

To create a binary chromosome instance, use GA.Binary:

```
genetic5 = GA.GABinary(10, 6, 0.3, 0.1, 500, crossover_policy = "uniform_crossover") 
```

To create a custom chromosome instance use GA.Custom:

```
genetic10 = GA.GACustom(5, 5, 0.2, 0.6, 500, crossover_policy = "multi_crossover", mutation_policy = "inversion_mutation", chromosome_values = ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"], gen_duplication = True)
```


## Defining the fitness function

To define and add the fitness function to a instance, first we define the function:

```
def fitness_example(chromosome):
        res = 0
        for a, b in zip(chromosome, chromosome[1:]):
            if b >= a:
                res += b
            else:
                res -= (a - b) * a
        return res
```

Next we update original fitness function (that is _None_) for our new function:

```
genetic5.fitness = fitness_example
```


## Using the algorithm

For using the algorithm and show fitness value chart, use **.solve()** and **.fitnessPlot()** methods:

```
sol = genetic5.solve()
print("\nSolution: ", sol, " fitness: ", str(genetic5.fitness(sol)))
genetic5.fitnessPlot()
```


## Output

![alt tag](https://i.gyazo.com/1204645be38f2845dac137b70f19d6ed.png)


## Errors

There is a couple of errors related to randomized generation of initial population and parent selection. If any of this errors occurs, just rerun the algorithm
