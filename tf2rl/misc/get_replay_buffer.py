from gym.spaces.box import Box
from gym.spaces.discrete import Discrete
from gym.spaces.dict import Dict

from cpprb import ReplayBuffer, PrioritizedReplayBuffer
from cpprb import NstepReplayBuffer
from cpprb import NstepPrioritizedReplayBuffer

from tf2rl.algos.policy_base import OffPolicyAgent


def get_space_size(space):
    if isinstance(space, Box):
        return space.low.size
    elif isinstance(space, Discrete):
        return 1  # space.n
    else:
        raise NotImplementedError("Assuming to use Box or Discrete")


def get_replay_buffer(policy, env, args):
    kwargs = {
        "obs_dim": get_space_size(env.observation_space),
        "act_dim": get_space_size(env.action_space),
        "size": policy.update_interval
    }

    # on-policy policy
    if not issubclass(type(policy), OffPolicyAgent):
        return ReplayBuffer(**kwargs)

    # off-policy policy
    kwargs["size"] = policy.memory_capacity

    # N-step prioritized
    if args.use_prioritized_rb and args.use_nstep_rb:
        kwargs["n_step"] = args.n_step
        kwargs["discount"] = policy.discount
        return NstepPrioritizedReplayBuffer(**kwargs)

    # prioritized
    if args.use_prioritized_rb:
        return PrioritizedReplayBuffer(**kwargs)

    # N-step
    if args.use_nstep_rb:
        kwargs["n_step"] = args.n_step
        kwargs["discount"] = policy.discount
        return NstepReplayBuffer(**kwargs)

    return ReplayBuffer(**kwargs)


if __name__ == '__main__':
    from cpprb import ReplayBuffer
    import numpy as np

    rb = ReplayBuffer(obs_dim=3, act_dim=3, size=10)
    for i in range(10):
        obs_act = np.array([i for _ in range(3)], dtype=np.float64)
        print(obs_act)
        rb.add(obs=obs_act, act=obs_act, next_obs=obs_act, rew=float(i), done=False)
    print(rb.sample(10))