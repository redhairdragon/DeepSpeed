# just to prove the concept of computing fwd and bwd on two different machine
# not used in the system
if self.global_rank == from_rank:
    # Test
    import torch
    import torch.nn as nn
    linear = nn.Linear(4, 5).to(self.device)
    optimizer = torch.optim.SGD(
        linear.parameters(), lr=0.1, momentum=0.9)
    optimizer.zero_grad()
    x = torch.tensor(
        [[1, 2, 3, 4.]], requires_grad=True).to(self.device)
    y = linear(x)

    print(f"rank xx:{from_rank},{y}")
    self.coord_com.setStateDict('y', y)
    # p2p.send(y, to_rank)

    self.coord_com.setStateDict("linear", linear.state_dict())

    z = torch.tensor([2, 3, 4, 5., 6],
                     requires_grad=True).to(self.device)
    loss = (z-y).sum()/5
    loss.backward(retain_graph=True)
    print(f'rank 1 {y.grad}')
    optimizer.step()
    print(f"rank: 1, {list(linear.parameters())}")
    exit()

if self.global_rank == to_rank:
    # Test
    linear = nn.Linear(4, 5).to(self.device)
    optimizer = torch.optim.SGD(
        linear.parameters(), lr=0.1, momentum=0.9)
    optimizer.zero_grad()

    y = torch.zeros(1, 5).to(self.device)
    y = self.coord_com.getStateDict('y')

    state_dict = self.coord_com.getStateDict("linear")
    linear.load_state_dict(state_dict)

    # p2p.recv(y, from_rank)
    print(f'rank:{to_rank},{y}')

    z = torch.tensor([2, 3, 4, 5., 6],
                     requires_grad=True).to(self.device)
    loss = (z-y).sum()/5
    loss.backward()
    print(f"rank: 0, before {list(linear.parameters())}")

    optimizer.step()
    print(f"rank: 0, {list(linear.parameters())}")
    exit()
