import torch
from torch.autograd import Variable
import torchvision.transforms as transforms
import torch.nn.functional as F

# Define a simple neural network
class SimpleNet(torch.nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = torch.nn.Linear(784, 128)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(128, 64)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Example usage
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
batch_size = 64
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

net = SimpleNet()
criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(net.parameters(), lr=0.001)

for epoch in range(3):
    running_loss = 0.0
    for data, target in train_loader:
        inputs, labels = data, target

        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    print(f'Epoch [{epoch+1}/{3}], Loss: {running_loss/len(train_loader)}')

# Define a function to visualize tensors in Jupyter notebook
def plot_tensor(tensor):
    import matplotlib.pyplot as plt
    import numpy as np
    import torch

    if tensor.dim() > 2:
        # Reduce the dimension for easier visualization
        if tensor.dim() == 3:
            tensor = tensor.squeeze(0)
        elif tensor.dim() == 4:
            tensor = tensor.permute(0, 2, 3, 1).squeeze(-1)

    if tensor.ndim == 1:
        plt.plot(tensor)
    else:
        plt.imshow(tensor.cpu().numpy(), cmap='viridis')

    plt.colorbar()
    plt.show()

# Example usage
inputs = next(iter(train_loader))[0].view(1, -1)
output = net(inputs)
plot_tensor(output)

obj['output']
