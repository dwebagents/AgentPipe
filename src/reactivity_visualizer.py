import matplotlib.pyplot as plt
from numpy import array

def plot_tensorflow_tensor(tensor):
    """
    Plots a 3D tensor using Matplotlib.

    Args:
        tensor (np.ndarray): The 3D tensor to plot.
    """
    # Ensure the input is a 3D array if not already
    if len(tensor.shape) != 3:
        raise ValueError("Input tensor must be a 3D array")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Assuming the first dimension is time, second is spatial dimensions, and third is channels
    X = tensor.shape[1]
    Y = tensor.shape[2]
    Z = tensor.shape[3]

    X, Y, Z = np.meshgrid(np.arange(X), np.arange(Y), np.arange(Z))

    # Plotting the data
    surf = ax.plot_surface(X, Y, Z, cstride=1, rstride=1, alpha=0.8)
    fig.colorbar(surf, shrink=0.5)

    # Labels for the axes
    ax.set_xlabel('Channel')
    ax.set_ylabel('Spatial Axis 1')
    ax.set_zlabel('Spatial Axis 2')

    plt.title('3D Plot of TensorFlow Tensor')
    plt.show()

def plot_pytorch_tensor(tensor):
    """
    Plots a 3D tensor using Matplotlib.

    Args:
        tensor (np.ndarray): The 3D tensor to plot.
    """
    # Ensure the input is a 3D array if not already
    if len(tensor.shape) != 3:
        raise ValueError("Input tensor must be a 3D array")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Assuming the first dimension is time, second is spatial dimensions, and third is channels
    X = tensor.shape[1]
    Y = tensor.shape[2]
    Z = tensor.shape[3]

    X, Y, Z = np.meshgrid(np.arange(X), np.arange(Y), np.arange(Z))

    # Plotting the data
    surf = ax.plot_surface(X, Y, Z, cstride=1, rstride=1, alpha=0.8)
    fig.colorbar(surf, shrink=0.5)

    # Labels for the axes
   
