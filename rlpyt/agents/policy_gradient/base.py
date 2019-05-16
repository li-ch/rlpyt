
import torch

from rlpyt.utils.collections import namedarraytuple
from rlpyt.agents.base import BaseAgent, BaseRecurrentAgent


AgentInfo = namedarraytuple("AgentInfo", ["dist_info", "value"])


class BasePgAgent(BaseAgent):

    distribution = None  # type: Distribution

    def initialize(self, env_spec, share_memory=False):
        env_model_kwargs = self.make_env_to_model_kwargs(env_spec)
        self.model = self.ModelCls(**env_model_kwargs, **self.model_kwargs)
        if share_memory:
            self.model.share_memory()
            self.shared_memory = share_memory
        if self.initial_state_dict is not None:
            self.model.load_state_dict(self.initial_state_dict)
        self.env_spec = env_spec
        self.env_model_kwargs = env_model_kwargs

    @torch.no_grad()  # Hint: apply this decorator on overriding method.
    def step(self, observation, prev_action, prev_reward):
        raise NotImplementedError  # return types: action, AgentInfo

    def make_env_to_model_kwargs(self, env_spec):
        return {}


RecurrentAgentInfo = namedarraytuple("AgentInfo",
    ["dist_info", "value", "prev_rnn_state"])


class BaseRecurrentPgAgent(BasePgAgent, BaseRecurrentAgent):

    pass