# Q-Learning Agent Usage Guide

## Quick Examples

### Basic Usage (Visual Game)
```python
from src.pacman.controllers.agents.q_learning_agent import QLearningAgent
from Executer import Executor
from pacman.controllers.examples.starter_ghosts import StarterGhosts

# Create executor and agents
executor = Executor()
pacman_agent = QLearningAgent()  # Trains automatically during creation
ghost_agent = StarterGhosts()

# Run visual game
score = executor.run_game_timed(pacman_agent, ghost_agent, visual=True)
print(f"Final Score: {score}")
```

### Console Mode (Faster)
```python
# Same setup but without visuals
score = executor.run_game_timed(pacman_agent, ghost_agent, visual=False)
```

### Custom Parameters
```python
# Create agent with custom parameters (modify after creation)
agent = QLearningAgent()
agent.episodes = 20    # More training
agent.alpha = 0.2      # Higher learning rate
agent.gamma = 0.95     # Higher discount factor
agent.epsilon = 0.05   # Lower exploration

# Clear old Q-table and retrain
agent.q_table.clear()
agent.train()
```

## Agent Parameters

- **episodes**: Number of training games (default: 5)
- **alpha**: Learning rate - how quickly new information overrides old (default: 0.1)
- **gamma**: Discount factor - how much future rewards matter (default: 0.9)
- **epsilon**: Exploration rate - how often to try random moves (default: 0.1)

## Training Process

1. Agent creates multiple game instances for training
2. Uses epsilon-greedy strategy: random moves (exploration) vs best known moves (exploitation)
3. Updates Q-table using: Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
4. After training, uses learned Q-table to play optimally

## Performance Tips

- More episodes = better performance but longer training
- Higher alpha = faster learning but potentially unstable
- Lower epsilon = more greedy, higher epsilon = more exploratory
- Agent can be reused without retraining for multiple games

## Integration with Game

The agent implements the `Controller` interface with a `_get_move(game, time_due)` method that:
1. Converts game state to GameState
2. Finds best action using Q-table
3. Returns the optimal move
