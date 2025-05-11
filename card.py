import random

class BingoCard:
    def __init__(self):
        self.card = self.generate_card()
        self.marked = [[False for _ in range(5)] for _ in range(5)]
        # Mark the FREE space as marked at the beginning
        self.marked[2][2] = True

    def generate_card(self):
        card = []
        ranges = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
        for i, (start, end) in enumerate(ranges):
            column = random.sample(range(start, end + 1), 5)
            card.append(column)
        # free space
        card[2][2] = "FREE"
        return [list(row) for row in zip(*card)]  # Transpose for 5x5

    def display(self):
        print("  B   I   N   G   O")
        for row_index in range(5):
            row_str = ""
            for col_index in range(5):
                value = self.card[row_index][col_index]
                if self.marked[row_index][col_index]:
                    row_str += f"[{str(value).center(2)}]"
                else:
                    row_str += f" {str(value).center(2)} "
            print(row_str)
        print()

    def mark_number(self, number):
        for row_index in range(5):
            for col_index in range(5):
                if self.card[row_index][col_index] == number:
                    self.marked[row_index][col_index] = True
                    return True
        return False

    def check_bingo(self):
        # Check rows
        for row in self.marked:
            if all(row):
                return True

        # Check columns
        for col_index in range(5):
            if all(self.marked[row_index][col_index] for row_index in range(5)):
                return True

        # Check diagonals
        if all(self.marked[i][i] for i in range(5)):
            return True
        if all(self.marked[i][4 - i] for i in range(5)):
            return True

        return False
