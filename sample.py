import simpy
import random
import statistics
import time
from skopt import gp_minimize
from skopt.space import Integer

wait_times = []

class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 5))


def go_to_movies(env, moviegoer, theater):
    arrival_time = env.now

    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))

    with theater.usher.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))

    if random.choice([True, False]):
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))

    wait_times.append(env.now - arrival_time)

def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)

    for moviegoer in range(3):
        env.process(go_to_movies(env, moviegoer, theater))

    while True:
        yield env.timeout(0.20)
        moviegoer += 1
        env.process(go_to_movies(env, moviegoer, theater))

def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def get_user_input():
    num_cashiers = input("Input # of cashiers working: ")
    num_servers = input("Input # of servers working: ")
    num_ushers = input("Input # of ushers working: ")
    params = [num_cashiers, num_servers, num_ushers]
    if all(str(i).isdigit() for i in params):
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:",
            "\n1 cashier, 1 server, 1 usher.",
        )
        params = [1, 1, 1]
    return params

def run_simulation(num_cashiers, num_servers, num_ushers):
    global wait_times
    wait_times = []
    random.seed(42)
    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
    env.run(until=90)
    return get_average_wait_time(wait_times)

def find_optimal_combination():
    best_combination = None
    best_wait_time = float('inf')

    for num_cashiers in range(1, 10):
        for num_servers in range(1, 10):
            for num_ushers in range(1, 10):
                mins, secs = run_simulation(num_cashiers, num_servers, num_ushers)
                total_wait_time = mins * 60 + secs
                if total_wait_time < best_wait_time:
                    best_wait_time = total_wait_time
                    best_combination = (num_cashiers, num_servers, num_ushers)

    return best_combination, best_wait_time
def objective(params):
    num_cashiers, num_servers, num_ushers = params
    mins, secs = run_simulation(num_cashiers, num_servers, num_ushers)
    total_wait_time = mins * 60 + secs
    return total_wait_time

def find_optimal_combination_bayes():
    space = [
        Integer(1, 10, name='num_cashiers'),
        Integer(1, 10, name='num_servers'),
        Integer(1, 10, name='num_ushers')
    ]
    res = gp_minimize(objective, space, n_calls=50, random_state=42)
    best_combination = res.x
    best_wait_time = res.fun
    return best_combination, best_wait_time

def main():
    best_combination, best_wait_time = find_optimal_combination_bayes()
    print(
        "Optimal combination:",
        f"\nCashiers: {best_combination[0]}, Servers: {best_combination[1]}, Ushers: {best_combination[2]}",
        f"\nWith an average wait time of {best_wait_time // 60} minutes and {best_wait_time % 60} seconds.",
    )

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))