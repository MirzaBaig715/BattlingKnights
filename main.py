import json


class Knight:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.status = "LIVE"
        self.attack = 1
        self.defense = 1
        self.item = None
        self.last_valid_position = position  # in case of dorwning the last position for an item to be placed.

    def move(self, direction):
        """ Moves the Knight in direction and set the status """
        if self.status != "LIVE":
            return

        x, y = self.position
        if direction == 'N':
            x -= 1
        elif direction == 'S':
            x += 1
        elif direction == 'E':
            y += 1
        elif direction == 'W':
            y -= 1
        else:
            raise f"Direction is incorrect: {direction}"
        # Check if knight has moved out of corners
        if not (0 <= x <= 7 and 0 <= y <= 7):
            # Drop the item on the last valid position before drowning
            if self.item:
                self.drop_item_on_last_valid_tile()

            # Update knight status to DROWNED
            self.status = "DROWNED"
            self.attack = 0
            self.defense = 0
            self.position = None
        else:
            # Update last valid position and position after valid move
            self.last_valid_position = self.position
            self.position = (x, y)

    def drop_item_on_last_valid_tile(self):
        """Drop the item on the last valid tile before drowning."""
        item, self.item = self.item, None  # Knight loses the item
        item.position = self.last_valid_position  # Place the item on the last valid tile
        item.equipped = False  # Item is no longer equipped

    def equip_item(self, items):
        # Equip the best item based on priority only if the knight doesn't already have an item
        if self.item is None:
            # Select the item with the highest priority
            best_item = max(items, key=lambda x: x.priority)
            # Update attack and defense based on the best item
            self.attack = 1 + best_item.attack_bonus  # base bonus + item bonus
            self.defense = 1 + best_item.defense_bonus
            self.item = best_item
            best_item.equipped = True  # Equip the best item

    def fight(self, defender):
        attacker_score = self.attack + 0.5  # Element of surprise
        defender_score = defender.defense

        if attacker_score > defender_score:
            defender.status = "DEAD"
            defender.attack = 0
            defender.defense = 0
            if defender.item:
                defender.item.equipped = False  # Defender loses item upon death
                defender.item = None  # Clear the reference to the item
        else:
            self.status = "DEAD"
            self.attack = 0
            self.defense = 0
            if self.item:
                self.item.equipped = False  # Item is no longer equipped upon death
                self.item = None  # Clear the reference to the item

    def get_state(self):
        return [self.position, self.status, self.item.name if self.item else None, self.attack, self.defense]


class Item:
    def __init__(self, name, position, attack_bonus, defense_bonus, priority):
        self.name = name
        self.position = position
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.priority = priority 
        self.equipped = False

    def get_state(self):
        return [self.position, self.equipped]


class Game:
    def __init__(self):
        self.knights = {
            "R": Knight("red", (0, 0)),
            "B": Knight("blue", (7, 0)),
            "G": Knight("green", (7, 7)),
            "Y": Knight("yellow", (0, 7))
        }
        self.items = {
            "A": Item("axe", (2, 2), attack_bonus=2, defense_bonus=0, priority=4),
            "D": Item("dagger", (2, 5), attack_bonus=1, defense_bonus=0, priority=2),
            "M": Item("magic_staff", (5, 2), attack_bonus=1, defense_bonus=1, priority=3),
            "H": Item("helmet", (5, 5), attack_bonus=0, defense_bonus=1, priority=1)
        }

    def move_knight(self, knight_id, direction):
        knight = self.knights[knight_id]
        knight.move(direction)

        if knight.status == "LIVE":
            self.handle_item_pickup(knight)
            self.check_for_battles(knight)

    def handle_item_pickup(self, knight):
        # If the knight already has an item, they ignore new items
        if knight.item is not None:
            return

        # Collect all items on the current tile
        items_on_tile = [item for item in self.items.values() if item.position == knight.position and not item.equipped]

        if items_on_tile:
            knight.equip_item(items_on_tile)  # Pass the list of items to the knight

    def check_for_battles(self, knight):
        for defender in self.knights.values():
            if knight != defender and knight.position == defender.position and defender.status == "LIVE":
                knight.fight(defender)

    def process_moves(self, moves):
        for move in moves:
            knight_id, direction = move.split(":")
            self.move_knight(knight_id, direction)

    def generate_final_state(self):
        final_state = {}
        for knight_id, knight in self.knights.items():
            final_state[knight.color] = knight.get_state()

        for item_id, item in self.items.items():
            final_state[item.name.lower()] = item.get_state()

        return final_state


def read_moves_file(file_path):
    valid_knights = ("R", "B", "G", "Y")
    valid_directions = ("N", "S", "E", "W")
    moves = []
    with open(file_path, 'r') as file:
        for line in file:
            move = line.strip()
            # Skip empty lines and GAME words
            if not move or "GAME" in move:
                continue

            # Validate move format
            if ':' not in move:
                raise ValueError(f"Invalid Move: {move}")

            knight_id, direction = move.split(":", 1)

            # Validate knight
            if knight_id not in valid_knights:
                raise ValueError(f"Invalid Knight: {knight_id}. VALID ONES: {valid_knights}")

            # Validate direction
            if direction not in valid_directions:
                raise ValueError(f"Invalid Direction: {direction}.VALID ONES: {valid_directions}")

            moves.append(move)
    return moves


def write_final_state(file_path, state):
    with open(file_path, 'w') as file:
        json.dump(state, file, indent=4)


if __name__ == "__main__":
    game = Game()

    moves = read_moves_file("moves.txt")
    game.process_moves(moves)
    final_state = game.generate_final_state()
    write_final_state("final_state.json", final_state)
