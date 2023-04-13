import torch
import pystk
from torch.distributions import Bernoulli
from state_agent.planner import network_features


class Player:
    def __init__(self, action_net):
        self.action_net = action_net.cpu().eval()

    def __call__(self, player_state, opponent_state, soccer_state, **kwargs):
        f = network_features(player_state, opponent_state, soccer_state)
        input_tensor = torch.tensor(torch.as_tensor(f).view(1, -1), dtype=torch.float)
        output = self.action_net(input_tensor)[0]

        action = pystk.Action()
        action.acceleration = 1
        steer_dist = Bernoulli(logits=output[0])
        action.steer = steer_dist.sample() * 2 - 1
        return action

class GreedyActor:
    def __init__(self, action_net):
        self.action_net = action_net.cpu().eval()

    def __call__(self, player_state, opponent_state, soccer_state, **kwargs):
        f = network_features(player_state, opponent_state, soccer_state)
        input_tensor = torch.tensor(torch.as_tensor(f).view(1, -1), dtype=torch.float)
        output = self.action_net(input_tensor)[0]

        action = pystk.Action()
        action.acceleration = 1
        action.steer = output[0]
        return action


def normalize_positions(positions):
    min_values = positions.min(axis=0)
    max_values = positions.max(axis=0)
    normalized_positions = 2 * (positions - min_values) / (max_values - min_values) - 1
    return normalized_positions