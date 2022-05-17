import pyibl
from tqdm import tqdm
from random import random

TRIALS = 50
PARTICIPANTS = 1
MISMATCH = 0.25
NOISE = 0.25
DECAY = 0.25
INFO = {"Deny": [0] * TRIALS, "Trust": [0] * TRIALS, "Fail": [0] * TRIALS}
BLACKLIST = ["192.168.1.17"]
IP = ["192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.1.17", "192.168.24.17", "192.168.24.17", "192.168.1.17", "192.168.24.18", "192.168.24.19", "192.168.24.20", "192.168.24.20", "192.168.24.20", "192.168.1.17", "192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.1.17", "192.168.1.17", "192.168.24.17", "192.168.24.200", "192.168.24.235", "192.168.24.8", "192.168.24.96", "192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.1.17", "192.168.24.17", "192.168.24.17", "192.168.1.17", "192.168.24.18", "192.168.24.19", "192.168.24.20", "192.168.24.20", "192.168.24.20", "192.168.1.17", "192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.24.17", "192.168.1.17", "192.168.1.17", "192.168.24.17", "192.168.24.200", "192.168.24.235", "192.168.24.8", "192.168.24.96"]
output = []

def ip_similarity(x, y):
    ip_x = x.split(".")
    ip_y = x.split(".")
    if ip_x[:3] == ip_y[:3]:
        return 1 - (abs(int(ip_x[3]) - int(ip_y[3])) /255) * 0.1
    elif ip_x[2] - ip_y[2] <= 1:
        return 0.10
    else:
        return 0

def verify_ip(ip):
    if ip not in BLACKLIST:
        return True
    return False

def payoff(score, choice, trial):
    if not choice["TRUST"]:
        score.update(10)
        INFO["Deny"][trial] += 1
        output.append(10)
    elif verify_ip(choice["IP"]):
        score.update(30)
        INFO["Trust"][trial] += 1
        output.append(30)
    else:
        score.update(-20)
        INFO["Fail"][trial] += 1
        output.append(-20)

def reset(agent):
    agent.reset()
    pyibl.similarity(lambda x, y: ip_similarity(x, y), "IP")
    agent.populate(40, {"IP": "192.168.24.17", "CRC": "PASS", "TRUST": True})   # accepting trusted IP
    agent.populate(-50, {"IP": "192.168.1.17", "CRC": "PASS", "TRUST": True})   # trusting blacklist IP
    agent.populate(10, {"IP": "192.168.1.17", "CRC": "PASS", "TRUST": False})   # denying blacklist IP


def run():
    trust_agent = pyibl.Agent("IoT", ["IP", "CRC", "TRUST"], noise=NOISE, decay=DECAY, mismatch_penalty=MISMATCH)
    for p in tqdm(range(PARTICIPANTS)):
        reset(trust_agent)
        for t in range(TRIALS):
            packet_pass = {"IP": IP[t], "CRC": "PASS", "TRUST": True}
            packet_block = {"IP": IP[t], "CRC": "PASS", "TRUST": False}
            choice = trust_agent.choose(packet_pass, packet_block)
            score = trust_agent.respond()
            payoff(score, choice, t)
    trust_agent.instances()     
    return [(sum(INFO["Trust"]) / (PARTICIPANTS * TRIALS)), (sum(INFO["Deny"]) / (PARTICIPANTS * TRIALS)), (sum(INFO["Fail"]) / (PARTICIPANTS * TRIALS))]

print(run())
print(output)