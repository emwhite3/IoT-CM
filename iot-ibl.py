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
# safe is determined by how we award points, should not be an attribute
def populate_agent(movement):
    movement.populate(23, {"x": 0, "y": 0, "no_obstacle": True, "trust": True, "move", True})
    movement.populate(-20, {"x": GRID_SIZE, "y": GRID_SIZE, "no_obstacle": False, "trust": True, "move", True})
    pyibl.similarity(lambda x, y: 1, "movement")
    return


def choose_direction():
    return

# we create one agent, this agent is responsible for approving the movement
# to the specified direction
def run(rounds=ROUNDS, participants=PARTICIPANTS):
    agent_movement = pyibl.Agent("MOVEMENT AGENT", ["no_obstacle", "trust"], optimized_learning=False)
    populate_agent(agent_movement)
    info = {"safe" : 0, "success" : 0, "unsafe": 0, "no_movement" = 0}
    for p in tqdm(range(participants)):
        reset_agent(agent_movement)
        for r in range(rounds):
            direction, safe, no_obstacle, x, y = choose_direction()
            movement = agent_movement.choose({"x": x, "y": y, "no_obstacle": no_obstacle, "trust": True, "move" : True}, {"x": x, "y": y, "no_obstacle": no_obstacle, "trust": True, "move" : False})["move"]
            if movement:
                if no_obstacle:
                    info["safe"] += 1
                    info["success"] += 1
                    payoff = 23
                else:
                    info["unsafe"] += 1
                    payoff = -20
            else:
                info["no_movement"] += 1
                payoff = 0            
            agent_movement.respond(payoff)
    print(info)
    return [info["safe"] / (ROUNDS * PARTICIPANTS), info["success"] / (ROUNDS * PARTICIPANTS), info["unsafe"] / (ROUNDS * PARTICIPANTS), info["no_movement"] / (ROUNDS * PARTICIPANTS)]



print(run())