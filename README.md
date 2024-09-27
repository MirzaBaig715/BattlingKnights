# Knights Game

## Overview

The Knights Game on a 8x8 grid Chess like board. Each knight can move in four directions (North, South, East, West), collect items that enhance their attack and defense, and engage in battles with other knights. The game tracks the state of each knight and item, including their position, status, and equipped items.

## Features (Based on Rules provided)

- **Knight Movement**: Knights can move in four directions and will drown if they attempt to move out of corners.
- **Item Pickup**: Knights can pick up items from their current position based on priority. A knight can only pick up an item if they do not already possess one.
- **Battle**: Knights can engage in battle when they land on the same tile of another Knight/Defender position. The outcome of the battle is determined by their attack and defense scores.
- **DEAD | DROWNED**: Attack and Defense scores would be 0. In case of DROWNED, Item would be placed on last valid tile.
- **Final State Generation**: The game generates a final state of all knights and items after all moves have been processed.

## Classes

- **Knight**: Represents a knight in the game, with attributes for color, position, status, attack, defense, and equipped item.
- **Item**: Represents an item that knights can equip to gain bonuses to their attack and defense.
- **Game**: Manages the state of the game, including knight movements, item pickups, and battles.

## File Structure

- `main.py`: The main Python script containing the game/movements/battles logic.
- `final_state.json`: The output file where the final state of the game is saved after processing the moves.
- `moves.txt`: Input file for moves.
## How to Run

   ```
   python3 main.py