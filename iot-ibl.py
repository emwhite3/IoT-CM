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

def reset_agent(agent, noise=NOISE, temperature=TEMPERATURE, decay=DECAY):
    agent.reset(False)
    agent.noise = noise
    agent.decay = decay
    agent.temperature = temperature
    agent.mismatch_penalty = MISMATCH_PENALTY


# 
def populate_agent(movement):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            movement.populate(10, {"x": 0, "y": 0, "safe": False, "success": True, "trust": False})
            movement.populate(110, {"attack": True, "warning": 0})
            movement.populate(-55, {"attack": True, "warning": 0})
    pyibl.similarity(lambda x, y: 1, "movement")
    return

 
# this is the creation of the attacker agent, it will first choose a box, then whether or not to attack
# the box given some feedback or "signal"
def run(rounds=ROUNDS, participants=PARTICIPANTS):
    agent_movement = pyibl.Agent("ATTACK AGENT", ["movement", "warning"], default_utility=DEFAULT_UTILITY, optimized_learning=False)
    populate_agent(agent_select, agent_movement)
    info = {"attack" : 0, "covered" : 0, "uncovered": 0, "withdraw": 0}
    for p in tqdm(range(participants)):             # for every participant they will partake in a given number of rounds
        reset_agent(agent_select)
        reset_agent(agent_movement)
        COVERAGE = np.random.choice([0,1], size=(ROUNDS,), p=[0.25, 0.75])  # this is where the odds for the defender can be altered for picking boxes
        for r in range(rounds):
            selection = agent_select.choose(0, 1)
            warned = 1 if selection == COVERAGE[r] else 0 if random.random() > 0.25 else 1
            movement = agent_movement.choose({"attack": False, "warning": warned}, {"attack": True, "warning": warned})["attack"]
            covered = selection == COVERAGE[r]
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