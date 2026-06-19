# Import necessary libraries
import matplotlib.pyplot as plt

def plot_reaction(reaction_data):
    # Create a new figure
    fig = plt.figure(figsize=(10, 5))
    
    # Plot the reaction data
    plt.plot(reaction_data['time'], reaction_data['reaction_value'])
    plt.title('Reaction Over Time')
    plt.xlabel('Time')
    plt.ylabel('Reaction Value')
    plt.grid(True)
    
    # Show the plot
    plt.show()

# Example data for demonstration
data = {
    'time': [1, 2, 3, 4, 5],
    'reaction_value': [0.1, 0.2, 0.3, 0.4, 0.5]
}

plot_reaction(data)
