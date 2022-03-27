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

def reset_agent(agent, noise=NOISE, temperature=TEMPERATURE, decay=DECAY):
    agent.reset(False)
    agent.noise = noise
    agent.decay = decay
    agent.temperature = temperature
    agent.mismatch_penalty = MISMATCH_PENALTY


# we can have 2 agents but we need to rework the attack agent
# into the agent that evaluates safety and success attributes
# we can then also add coordinates associated with these positive
# attributes. From here the agent can decipher the enviornment
# Then the goal after this is succesful is to build a safe and succesful path when given coordinates
# there we can also add similarity. Once that is added we can add the validity agent
# this agent will take in commands from labeled command providers
# some trusted and some untrusted
def populate_agent(select, attack):
    select.populate(110, 0)
    select.populate(110, 1)
    attack.populate(-30, {"attack": False, "warning": 0})
    attack.populate(110, {"attack": True, "warning": 0})
    attack.populate(-55, {"attack": True, "warning": 0})
    select.instances()
    attack.instances()
    pyibl.similarity(lambda x, y: 1-abs(x-y), "warning")
    pyibl.similarity(lambda x, y: 1, "attack")
    return

 
# this is the creation of the attacker agent, it will first choose a box, then whether or not to attack
# the box given some feedback or "signal"
def run(rounds=ROUNDS, participants=PARTICIPANTS):
    agent_select = pyibl.Agent("SELECTION AGENT", default_utility=DEFAULT_UTILITY, optimized_learning=False)
    agent_attack = pyibl.Agent("ATTACK AGENT", ["attack", "warning"], default_utility=DEFAULT_UTILITY, optimized_learning=False)
    populate_agent(agent_select, agent_attack)
    info = {"attack" : 0, "covered" : 0, "uncovered": 0, "withdraw": 0}
    for p in tqdm(range(participants)):             # for every participant they will partake in a given number of rounds
        reset_agent(agent_select)
        reset_agent(agent_attack)
        COVERAGE = np.random.choice([0,1], size=(ROUNDS,), p=[0.25, 0.75])  # this is where the odds for the defender can be altered for picking boxes
        for r in range(rounds):
            selection = agent_select.choose(0, 1)
            warned = 1 if selection == COVERAGE[r] else 0 if random.random() > 0.25 else 1
            attack = agent_attack.choose({"attack": False, "warning": warned}, {"attack": True, "warning": warned})["attack"]
            covered = selection == COVERAGE[r]
            if attack:
                info["attack"] += 1
                payoff = -50 if covered else 100
                info["covered"] += 1 if payoff == -50 else 0
                info["uncovered"] += 1 if payoff == 100 else 0
            else:
                info["withdraw"] += 1
                payoff = 0
            
            agent_attack.respond(payoff)
            agent_select.respond(payoff)
    print(info)
    return [info["attack"] / (ROUNDS * PARTICIPANTS), info["covered"] / (ROUNDS * PARTICIPANTS), info["uncovered"] / (ROUNDS * PARTICIPANTS), info["withdraw"] / (ROUNDS * PARTICIPANTS)]



print(run())