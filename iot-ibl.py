import pyibl
from random import random as rand
from tqdm import tqdm
import numpy as np
 
PARTICIPANTS = 100
ROUNDS = 50
NOISE = 0.25
TEMPERATURE = 1.0
DECAY = 0.5
DEFAULT_UTILITY = 30
TARGET_COUNT = 2
MISMATCH_PENALTY = 2.5
GRID_SIZE = 10
ARM = [10, 0]
GOAL = [0, 1]
MAZE = [[0, -1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]        # -1 is the goal, 1 is an obstacle and 0 is an open cell
AGENT_MAZE = [0*len(MAZE)] * len(MAZE[0])
VISITED = []
TRUST = [30, 10, 30, 30, -20, 30, 30, -20, 30, 30, 30, 30, 30, -20, 30, 30, 30, 30, -20, -20, 10, 30, 10, 30, 30, 30, 30, 30, 30, -20, 30, 30, 10, 30, 30, 30, 30, 30, -20, 30, 30, 30, 30, -20, -20, 10, 10, 10, 30, 30]
collision = [0] # collision

def dfs_maze():
    stack = []
    stack.append([0,0])
    visited = [[False for j in range(len(MAZE))] for i in range(len(MAZE[0]))]
    while len(stack) > 0:
        curr = stack.pop()
        visited[curr[0]][curr[1]] = True
        
    return

def trust_model_output(movement, t):
    if movement:
        return TRUST[t]
    else:
        return 0

def move_maze():
    VISITED.append(ARM)
    if ARM[0] > GOAL[0]:        # if the GOAL is above then move up
        if MAZE[(ARM[0] - 1)][ARM[1]] == 0:   # if an obstacle is not present then move here
            if rand() > 0.9:
                ARM[0] -= 1
                return False
            else:
                ARM[0] -= 1
                collision[0] += 1
                return False
        else:
            ARM[1] += 1
            return False
    if ARM[1] > GOAL[1]:
        ARM[1] -= 1
        return False
    return True


def reset_agent(agent, noise=NOISE, temperature=TEMPERATURE, decay=DECAY):
    agent.reset(False)
    agent.noise = noise
    agent.decay = decay
    agent.temperature = temperature
    agent.mismatch_penalty = MISMATCH_PENALTY
    populate_agent(agent)


# since we know our starting point is safe, we set
# the utility to be the highest points possible
# safe is determined by how we award points, should not be an attribute
def populate_agent(movement):
    movement.populate(23, {"move": True, "x": 0, "y": 0, "no_obstacle": True, "trust": True})
    movement.populate(5, {"move": True, "x": GRID_SIZE+1, "y": GRID_SIZE+1, "no_obstacle": True, "trust": False})
    movement.populate(23, {"move": False, "x": GRID_SIZE+2, "y": GRID_SIZE+2, "no_obstacle": True, "trust": False})
    movement.populate(-20, {"move": True, "x": GRID_SIZE, "y": GRID_SIZE, "no_obstacle": False, "trust": True})
    pyibl.similarity(lambda x, y: 1, "x")
    pyibl.similarity(lambda x, y: 1, "y")
    pyibl.similarity(lambda x, y: 1, "move")
    pyibl.similarity(lambda x, y: 1, "no_obstacle")
    pyibl.similarity(lambda x, y: 1, "trust")
    return


def choose_direction():
    return move_maze(), True, True, ARM[0], ARM[1]

# we create one agent, this agent is responsible for approving the movement
# to the specified direction
def run(rounds=ROUNDS, participants=PARTICIPANTS):
    agent_movement = pyibl.Agent("MOVEMENT AGENT", ["move", "x", "y", "no_obstacle", "trust"])
    info = {"safe" : 0, "success" : 0, "unsafe": 0, "no_movement": 0, "goal_moves": 0}
    for p in tqdm(range(participants)):
        reset_agent(agent_movement)
        for r in range(rounds):
            goal_met = False
            while not goal_met:
                goal_met, safe, no_obstacle, x, y = choose_direction()
                movement = agent_movement.choose({"move" : True, "x": x, "y": y, "no_obstacle": no_obstacle, "trust": True if TRUST[r]> 0 else False}, {"move" : False, "x": x, "y": y, "no_obstacle": no_obstacle, "trust": True if TRUST[r]> 0 else False})["move"]
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
                agent_movement.respond(payoff + trust_model_output(movement, r))
                info["goal_moves"] += 1
    print(info)
    return [info["safe"] / (ROUNDS * PARTICIPANTS), info["success"] / (ROUNDS * PARTICIPANTS), info["unsafe"] / (ROUNDS * PARTICIPANTS), info["no_movement"] / (ROUNDS * PARTICIPANTS)]



print(run())
print(collision[0] / (ROUNDS * PARTICIPANTS))