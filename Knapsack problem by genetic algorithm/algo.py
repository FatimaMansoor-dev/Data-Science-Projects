import random
import json
import matplotlib.pyplot as plt

# Budget options
budget = [35000, 20000, 15000, 25000, 10000]

# Load items data from JSON file
with open('objects.json', 'r') as file:
    data = json.load(file)


class KnapSack:
    def __init__(self, pop_size, budget):
        items = list(range(1, 51)) 
        self.population_size = pop_size
        self.selected_items = random.sample(items, self.population_size)  # Select unique items
        self.budget = budget

    def generate_population(self):
        chromo = []
        for i in self.selected_items:
            chromo.append(data[str(i)]['quantity'])
        self.population = []
        for _ in range(self.population_size):
            chromosome = []
            for qty in chromo:
                chromosome.append(random.randint(0, qty))  # Random quantity within bounds
            self.population.append(chromosome)
        self.check_fitness()

    def check_fitness(self):
        self.values_of_each_chromosome = []  # Stores the fitness (value)
        self.prices_of_each_chromosome = []  # Stores total price (weight)

        for chromosome in self.population:
            chromosome_price = 0
            chromosome_value = 0
            for i in range(self.population_size):
                item = self.selected_items[i]
                item_price = chromosome[i] * data[str(item)]['price']  # Quantity * Price
                item_value = chromosome[i] * data[str(item)]['value']  # Quantity * Value
                chromosome_price += item_price
                chromosome_value += item_value

            # Fitness is value only if within budget; otherwise, it's invalid (0 fitness)
            if chromosome_price <= self.budget:
                self.values_of_each_chromosome.append(chromosome_value)
            else:
                self.values_of_each_chromosome.append(0)
            self.prices_of_each_chromosome.append(chromosome_price)

    def selection(self):
        total_value = sum(self.values_of_each_chromosome)
        if total_value == 0:
            print("All chromosomes invalid. Regenerating population.")
            self.generate_population()
            self.check_fitness()
            return

        probabilities = [val / total_value for val in self.values_of_each_chromosome]
        cumulative_probabilities = []
        current_sum = 0
        for p in probabilities:
            current_sum += p
            cumulative_probabilities.append(current_sum)

        parents = []
        for _ in range(self.population_size):  # Select as many parents as population size
            r = random.random()
            for i, cumulative_probability in enumerate(cumulative_probabilities):
                if r <= cumulative_probability:
                    parents.append(self.population[i])
                    break

        self.crossover(parents)

    def crossover(self, parents):
        offspring = []
        for i in range(0, len(parents), 2):  # Pair up parents
            if i + 1 < len(parents):  # Ensure we have a pair
                parent1 = parents[i]
                parent2 = parents[i + 1]

                # Random crossover point
                crossover_point = random.randint(1, self.population_size - 1)
                print(f"Crossover point: {crossover_point}")

                # Create offspring
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
                offspring.extend([child1, child2])
            else:
                # If odd number, add last parent directly
                offspring.append(parents[i])

        self.population = offspring

    def mutation(self, mutation_rate=0.05):
        for i in range(self.population_size):
            chromosome = self.population[i]
            for j in range(len(chromosome)):  # Iterate over the genes
                if random.random() < mutation_rate:  # Mutation happens
                    max_qty = data[str(self.selected_items[j])]['quantity']
                    current_qty = chromosome[j]
                    # Randomly increase or decrease the quantity
                    if random.random() < 0.5:
                        chromosome[j] = min(current_qty + 1, max_qty)
                    else:
                        chromosome[j] = max(current_qty - 1, 0)

    def print_solution(self, solution):
        total_price = 0
        total_value = 0
        print("\nSelected Items:")
        print("{:<20} {:<10} {:<10} {:<10}".format("Item Name", "Quantity", "Price", "Total Price"))
        print("-" * 50)
        for i, qty in enumerate(solution):
            item_id = self.selected_items[i]
            item_name = data[str(item_id)]['name']
            item_price = data[str(item_id)]['price']
            total_item_price = qty * item_price
            total_price += total_item_price
            total_value += qty * data[str(item_id)]['value']
            print(f"{item_name:<20} {qty:<10} {item_price:<10} {total_item_price:<10}")
        print("-" * 50)
        print(f"Total Price: {total_price}, Total Value: {total_value}, Budget: {self.budget}")

    def run_algorithm(self, generations):
        best_solution = None
        best_value = 0
        values_over_generations = []  # Track values over generations

        for generation in range(generations):
            print(f"Generation {generation + 1}:")
            self.check_fitness()

            max_value = max(self.values_of_each_chromosome)
            values_over_generations.append(max_value)  # Track max value
            if max_value > best_value:
                best_value = max_value
                best_solution = self.population[self.values_of_each_chromosome.index(max_value)]

            print(f"Best Value in Generation {generation + 1}: {best_value}")
            self.selection()  # Create next generation
            self.mutation()  # Apply mutation

        # Plot the graph
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, generations + 1), values_over_generations, marker='o', color='b')
        plt.title("Best Value Over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Value")
        plt.grid(True)
        plt.savefig("best_value_over_generations.png")  # Save graph to file
        print("Graph saved as 'best_value_over_generations.png'.")

        print("Final Best Solution:")
        self.print_solution(best_solution)
        return best_solution, best_value
    
    def get_item_details(self):
        """Return a list of items with details for GUI display."""
        item_details = []
        for item_id in self.selected_items:
            item = data[str(item_id)]
            item_details.append({
                "name": item['name'],
                "price": item['price'],
                "quantity": item['quantity'],
                "value": item['value']
            })
        return item_details



# Initialize and run the algorithm
ks = KnapSack(10, random.choice(budget))
ks.generate_population()
best_solution, best_value = ks.run_algorithm(generations=50)
