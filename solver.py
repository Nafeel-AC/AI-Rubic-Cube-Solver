import numpy as np
import random
from cube import RubiksCube

class CubeSolver:
    def __init__(self):
        # Initialize the possible moves for the Rubik's Cube
        self.moves = [(f, d) for f in range(6) for d in [-1, 1]]
        # Genetic Algorithm (GA) parameters
        self.population_size = 1000  # Number of individuals in the population
        self.max_generations = 200  # Increased maximum number of generations
        self.mutation_rate = 0.1  # Probability of mutation
        self.elite_size = 10  # Number of elite individuals to carry over to the next generation
        self.max_sequence_length = 50  # Maximum length of a sequence of moves
        # Reward parameters for evaluating fitness
        self.corner_weight = 4.0
        self.edge_weight = 2.0
        self.center_weight = 1.0
        self.cross_weight = 5.0
        self.corner_alignment_weight = 3.0
        self.edge_alignment_weight = 2.0
        self.solution = []
        
    def evaluate_fitness(self, cube_state):
        """Calculate fitness using weighted scoring"""
        score = 0
        for face in range(6):
            center = cube_state[face, 1, 1]
            
            # Score corners
            corners = [cube_state[face, i, j] for i, j in [(0,0), (0,2), (2,0), (2,2)]]
            score += sum(c == center for c in corners) * self.corner_weight
            
            # Score edges
            edges = [cube_state[face, i, j] for i, j in [(0,1), (1,0), (1,2), (2,1)]]
            score += sum(e == center for e in edges) * self.edge_weight
            
            # Score centers (should always match but include for completeness)
            score += (cube_state[face, 1, 1] == face) * self.center_weight

        # Additional scoring for cross, corner alignment, and edge alignment
        score += self.evaluate_cross(cube_state) * self.cross_weight
        score += self.evaluate_corner_alignment(cube_state) * self.corner_alignment_weight
        score += self.evaluate_edge_alignment(cube_state) * self.edge_alignment_weight
            
        return score

    def evaluate_cross(self, cube_state):
        """Evaluate the cross on the first layer"""
        cross_score = 0
        for face in range(6):
            center = cube_state[face, 1, 1]
            edges = [cube_state[face, i, j] for i, j in [(0,1), (1,0), (1,2), (2,1)]]
            cross_score += sum(e == center for e in edges)
        return cross_score

    def evaluate_corner_alignment(self, cube_state):
        """Evaluate the alignment of corner pieces"""
        alignment_score = 0
        for face in range(6):
            center = cube_state[face, 1, 1]
            corners = [cube_state[face, i, j] for i, j in [(0,0), (0,2), (2,0), (2,2)]]
            alignment_score += sum(c == center for c in corners)
        return alignment_score

    def evaluate_edge_alignment(self, cube_state):
        """Evaluate the alignment of edge pieces"""
        alignment_score = 0
        for face in range(6):
            center = cube_state[face, 1, 1]
            edges = [cube_state[face, i, j] for i, j in [(0,1), (1,0), (1,2), (2,1)]]
            alignment_score += sum(e == center for e in edges)
        return alignment_score

    def create_individual(self):
        """Create a random sequence of moves"""
        length = random.randint(1, self.max_sequence_length)
        
        return [random.choice(self.moves) for _ in range(length)]

    def mutate(self, individual):
        """Mutate a solution by changing, adding, or removing moves"""
        if random.random() < self.mutation_rate:
            mutation_type = random.choice(['change', 'add', 'remove'])
            if mutation_type == 'change' and len(individual) > 0:
                pos = random.randint(0, len(individual) - 1)
                individual[pos] = random.choice(self.moves)
            elif mutation_type == 'add' and len(individual) < self.max_sequence_length:
                pos = random.randint(0, len(individual))
                individual.insert(pos, random.choice(self.moves))
            elif mutation_type == 'remove' and len(individual) > 1:
                pos = random.randint(0, len(individual) - 1)
                individual.pop(pos)
        return individual

    def crossover(self, parent1, parent2):
        """Perform crossover between two parents"""
        if len(parent1) == 0 or len(parent2) == 0:
            return parent1.copy(), parent2.copy()
        
        point1 = random.randint(0, len(parent1))
        point2 = random.randint(0, len(parent2))
        
        child1 = parent1[:point1] + parent2[point2:]
        child2 = parent2[:point2] + parent1[point1:]
        
        return child1, child2

    def solve(self, cube):
        best_solution = None
        best_fitness = -1
        initial_state = cube.get_state()

        # Initialize population
        population = [self.create_individual() for _ in range(self.population_size)]
        
        for generation in range(self.max_generations):
            fitness_scores = []
            
            # Evaluate fitness
            for individual in population:
                test_cube = RubiksCube()
                test_cube.state = initial_state.copy()
                
                # Apply moves
                for move in individual:
                    test_cube.make_move(move)
                
                # Calculate fitness
                fitness = self.evaluate_fitness(test_cube.state)
                fitness_scores.append(fitness)
                
                # Check if solved
                if test_cube.is_solved():
                    print(f"Solution found in generation {generation}")
                    return self._optimize_solution(individual)
                
                # Update best solution
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_solution = individual.copy()
                    print(f"Generation {generation}: New best fitness = {best_fitness}")

            # Log the average fitness of the current generation
            avg_fitness = np.mean(fitness_scores)
            print(f"Generation {generation}: Average fitness = {avg_fitness}")

            # Select parents using tournament selection
            parents = []
            while len(parents) < self.population_size:
                tournament = random.sample(list(enumerate(fitness_scores)), 3)
                winner = max(tournament, key=lambda x: x[1])[0]
                parents.append(population[winner])

            # Create new generation
            new_population = []
            
            # Add elite solutions
            elite_indices = np.argsort(fitness_scores)[-self.elite_size:]
            new_population.extend([population[i] for i in elite_indices])
            
            # Create rest of population through crossover and mutation
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            
            population = new_population[:self.population_size]

        print("No solution found")
        return best_solution or []

    def _optimize_solution(self, solution):
        """Remove redundant moves from solution"""
        optimized = []
        i = 0
        while i < len(solution):
            if i + 1 < len(solution) and solution[i][0] == solution[i+1][0]:
                i += 2  # Skip canceling moves
            else:
                optimized.append(solution[i])
                i += 1
        return optimized