import pyibl
import random
from tqdm import tqdm
import numpy as np
 
PARTICIPANTS = 1000
ROUNDS = 50
NOISE = 0.25
TEMPERATURE = 1.0
DECAY = 0.5
DEFAULT_UTILITY = 30
TARGET_COUNT = 2
MISMATCH_PENALTY = 2.5
GRID_SIZE = 200
MAZE = []
AGENT_MAZE = []


def reset_agent(agent, noise=NOISE, temperature=TEMPERATURE, decay=DECAY):
    agent.reset(False)
    agent.noise = noise
    agent.decay = decay
    agent.temperature = temperature
    agent.mismatch_penalty = MISMATCH_PENALTY


# since we know our starting point is safe, we set
# the utility to be the highest points possible
def populate_agent(movement):
    movement.populate(10, {"x": 0, "y": 0, "safe": True, "success": True, "trust": True})
    pyibl.similarity(lambda x, y: 1, "movement")
    return

 
# we create one agent, this agent is responsible for approving the movement
# to the specified direction
def run(rounds=ROUNDS, participants=PARTICIPANTS):
    agent_movement = pyibl.Agent("MOVEMENT AGENT", ["safe", "success", "trust"], optimized_learning=False)
    populate_agent(agent_movement)
    info = {"safe" : 0, "success" : 0, "unsafe": 0}
    for p in tqdm(range(participants)):             # for every participant they will partake in a given number of rounds
        reset_agent(agent_movement)
        for r in range(rounds):
            direction = agent_select.choose(0, 1)
            warned = 1 if direction == COVERAGE[r] else 0 if random.random() > 0.25 else 1
            movement = agent_movement.choose({"attack": False, "warning": warned}, {"attack": True, "warning": warned})["attack"]
            covered = direction == COVERAGE[r]
            if movement:
                info["attack"] += 1
                payoff = -50 if covered else 100
                info["covered"] += 1 if payoff == -50 else 0
                info["uncovered"] += 1 if payoff == 100 else 0
            else:
                info["withdraw"] += 1
                payoff = 0
            
            agent_movement.respond(payoff)
            agent_select.respond(payoff)
    print(info)
    return [info["attack"] / (ROUNDS * PARTICIPANTS), info["covered"] / (ROUNDS * PARTICIPANTS), info["uncovered"] / (ROUNDS * PARTICIPANTS), info["withdraw"] / (ROUNDS * PARTICIPANTS)]



print(run())