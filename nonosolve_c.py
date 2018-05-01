from bearlibterminal import terminal
import time


class Row:
    def __init__(self, length, blocks):
        """
        Params:
        length: int: the width of the puzzle/length of row
        blocks: list: the length of the individual blocks that will make up the row
        """
        # If the blocs + the whitespace between them is greater than the row's length it is impossible

        if sum(blocks) + len(blocks) - 1 > length:
            raise ValueError("Length of blocks exceeds length of row")
        self.length = length
        self.blocks = blocks
        # Whitespace is the gap to the left of each bock
        # The first block is agains the wall so it has no gap
        # The rest start with one space between them
        self.whiteSpace = [0] + [1] * (len(blocks) - 1)
        # Wiggle Room is the total whiteSpace in the row, NOT CURRENTLY USED?
        self.wiggleRoom = length - sum(blocks) - len(blocks) + 1
        # Target Block is the current block to be moved
        self.targetBlock = len(blocks) - 1

    def body(self):
        """
        Returns a visual representation of the row, where whitespace is . and blocks are #
        """
        strn = ""
        left = self.length - sum(self.whiteSpace) - sum(self.blocks)
        for block in range(len(self.blocks)):
            strn += "." * self.whiteSpace[block]
            strn += "#" * self.blocks[block]
        strn += "." * left
        return strn

    def move_one(self):
        """
        Puts the row into teh next possible stare by sliding the target block
        Returns True if there are combinations left, false otherwise
        """

        # If the last block on the left is as far right as it can go all blocks are moved back
        # This implies the row has gone through all possibilities

        if self.whiteSpace[0] == self.wiggleRoom or self.wiggleRoom == 0:
            self.reset()
            return False

            # left is how much room there is to move
        left = self.length - sum(self.whiteSpace) - sum(self.blocks)

        # if there is room to move, then the block will advance one spot
        if left != 0:
            self.whiteSpace[self.targetBlock] += 1

        # if there is no room the target block will change until it finds a block with room to move and advances it
        else:
            self.targetBlock -= 1
            while self.whiteSpace[self.targetBlock + 1] == 1:
                self.targetBlock -= 1
            self.whiteSpace[self.targetBlock] += 1

        # Honestly some 3:00am magic shit I did
        while self.targetBlock < len(self.blocks) - 1:
            self.targetBlock += 1
            self.whiteSpace[self.targetBlock] = 1

            # There are more possibilities
        return True

    def reset(self):
        self.whiteSpace = [0] + [1] * (len(self.blocks) - 1)


class Column:
    def __init__(self, length, blocks):
        """
        Params:
        length: int: the width of the puzzle/length of row
        blocks: list: the length of the individual blocks that will make up the row
        """
        # If the blocs + the whitespace between them is greater than the row's length it is impossible

        if sum(blocks) + len(blocks) - 1 > length:
            raise ValueError("Length of blocks exceeds length of column")
        self.length = length
        self.blocks = blocks
        # Whitespace is the gap to the left of each bock
        # The first block is agains the wall so it has no gap
        # The rest start with one space between them
        self.whiteSpace = [0] + [1] * (len(blocks) - 1)
        # Wiggle Room is the total whiteSpace in the row, NOT CURRENTLY USED?
        self.wiggleRoom = length - sum(blocks) - len(blocks) + 1
        # Target Block is the current block to be moved
        self.targetBlock = len(blocks) - 1

    def body(self):
        """
        Returns a visual representation of the row, where whitespace is . and blocks are #
        """
        strn = ""
        left = self.length - sum(self.whiteSpace) - sum(self.blocks)
        for block in range(len(self.blocks)):
            strn += "." * self.whiteSpace[block]
            strn += "#" * self.blocks[block]
        strn += "." * left
        return strn

    def reset(self):
        self.whiteSpace = [0] + [1] * (len(self.blocks) - 1)


def bad_rows(row_list, col_list):
    rows_to_change = []
    for r in range(len(row_list)):
        if not check_row(r, row_list, col_list, exact=True):
            rows_to_change.append(r)

    return rows_to_change


def check_row(r_id, row_list, col_list, exact=False):
    ro = row_list[r_id]
    r_body = ro.body()
    for x in range(len(col_list)):
        column = col_list[x]
        c_body = column.body()

        if r_body[x] == '#' and c_body[r_id] == '.' or exact and r_body[x] != c_body[r_id]:
            return False
    return True


def match_block(rn, w, b):
    block = 0
    sum_ = w[0] + b[0]
    while rn >= sum_:
        block += 1
        if block == len(b):
            block -= 1
            break
        sum_ += w[block] + b[block]
    return block


def squish_down_from(rn, column):
    start_block = match_block(rn, column.whiteSpace, column.blocks)
    start_space = column.whiteSpace[start_block]

    target = start_block
    while column.whiteSpace[start_block] == start_space:
        if target == len(column.blocks) - 1:
            left = column.length - sum(column.whiteSpace) - sum(column.blocks)
            if left > 0:
                column.whiteSpace[target] += 1
                target = start_block
            else:
                return False

        elif column.whiteSpace[target + 1] > 1:
            column.whiteSpace[target] += 1
            column.whiteSpace[target + 1] -= 1
            target = start_block
        else:
            target += 1

    return True


def move_up_from(rn, column):
    start_block = match_block(rn, column.whiteSpace, column.blocks)
    if column.whiteSpace[start_block] > 0:
        column.whiteSpace[start_block] -= 1

        target = start_block + 1
        while target < len(column.whiteSpace):
            column.whiteSpace[target] = 1
            target += 1
    else:
        return False


'''
# Input
# Test 10x10 nonogram:
# Rows:
r0 = Row(10, [3])
r1 = Row(10, [4, 1])
r2 = Row(10, [1, 1, 2, 1])
r3 = Row(10, [3, 1, 3])
r4 = Row(10, [1])
r5 = Row(10, [3, 3])
r6 = Row(10, [5, 3])
r7 = Row(10, [3, 1, 1, 1])
r8 = Row(10, [5, 3])
r9 = Row(10, [3, 3])

rows = [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9]

# Columns:
c0 = Column(10, [1])
c1 = Column(10, [2, 3])
c2 = Column(10, [1, 1, 5])
c3 = Column(10, [2, 5])
c4 = Column(10, [2, 2, 2, ])
c5 = Column(10, [5, 3])
c6 = Column(10, [1, 1, 1, 1])
c7 = Column(10, [1, 1, 5])
c8 = Column(10, [2, 2, 2])
c9 = Column(10, [1, 3])

cols = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]
# End of input
'''
'''
# Input
# 15 x 15
# Rows:
r00 = Row(15, [1])
r01 = Row(15, [3])
r02 = Row(15, [5])
r03 = Row(15, [7])
r04 = Row(15, [9])
r05 = Row(15, [11])
r06 = Row(15, [13])
r07 = Row(15, [13])
r08 = Row(15, [15])
r09 = Row(15, [15])
r10 = Row(15, [15])
r11 = Row(15, [6, 1, 6])
r12 = Row(15, [4, 1, 4])
r13 = Row(15, [3])
r14 = Row(15, [5])

rows = [r00, r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, r11, r12, r13, r14]

c00 = Column(15, [4])
c01 = Column(15, [7])
c02 = Column(15, [8])
c03 = Column(15, [9])
c04 = Column(15, [10])
c05 = Column(15, [10, 1])
c06 = Column(15, [10, 2])
c07 = Column(15, [15])
c08 = Column(15, [10, 2])
c09 = Column(15, [10, 1])
c10 = Column(15, [10])
c11 = Column(15, [9])
c12 = Column(15, [8])
c13 = Column(15, [7])
c14 = Column(15, [4])

cols = [c00, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12, c13, c14]
'''

r00 = Row(25, [3])
r01 = Row(25, [2, 2])
r02 = Row(25, [2, 2])
r03 = Row(25, [3, 2])
r04 = Row(25, [3, 2])
r05 = Row(25, [4, 2])
r06 = Row(25, [8])
r07 = Row(25, [3, 2])
r08 = Row(25, [1, 5, 3, 1, 2])
r09 = Row(25, [2, 13, 1, 1])
r10 = Row(25, [3, 7, 5])
r11 = Row(25, [1, 2])
r12 = Row(25, [1, 1, 1, 2, 3])
r13 = Row(25, [1, 2, 2, 1, 5])
r14 = Row(25, [1, 2, 8, 2, 1])
r15 = Row(25, [3, 2, 2, 2, 5])
r16 = Row(25, [2, 1, 2, 4, 9])
r17 = Row(25, [7, 6, 1])
r18 = Row(25, [7, 10])
r19 = Row(25, [1, 13])

rows = [r00, r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19]

c00 = Column(20, [2, 2])
c01 = Column(20, [2, 5])
c02 = Column(20, [2, 1, 2])
c03 = Column(20, [5, 2])
c04 = Column(20, [2, 2, 2])
c05 = Column(20, [2, 2, 4])
c06 = Column(20, [2, 2])
c07 = Column(20, [2, 2, 1])
c08 = Column(20, [2, 5, 2])
c09 = Column(20, [3, 3, 3])
c10 = Column(20, [3, 2, 1, 4])
c11 = Column(20, [5, 2, 1, 4])
c12 = Column(20, [1, 3, 2, 1, 4])
c13 = Column(20, [1, 3, 2, 1, 4])
c14 = Column(20, [1, 2, 2, 2, 3])
c15 = Column(20, [2, 2, 3, 4, 2])
c16 = Column(20, [2, 4, 2, 2])
c17 = Column(20, [2, 3, 1, 2])
c18 = Column(20, [4, 2, 3, 1, 1])
c19 = Column(20, [2, 3, 3, 1])
c20 = Column(20, [1, 1, 2, 1, 2])
c21 = Column(20, [1, 1, 2, 2])
c22 = Column(20, [2, 1, 2, 2])
c23 = Column(20, [2, 2, 2])
c24 = Column(20, [2, 2])

cols = [c00, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11,
        c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24]

# Creates terminal to display
terminal.open()
terminal.set("window: size={}x{}, cellsize=12x12".format(2*len(cols) + 2, len(rows) + 1))


r_i = 0


def draw_in_terminal():
    terminal.clear()
    terminal.printf(0, r_i, '>')
    for rw in range(len(rows)):
        terminal.printf(1, rw, rows[rw].body())
        for cl in range(len(cols)):
            terminal.printf(len(cols) + cl + 2, rw, cols[cl].body()[rw])
    time.sleep(0)
    terminal.refresh()


squished = [[] for rw in rows]
drop = True
advance = 1

while True:
    if r_i == len(rows):
        break
    draw_in_terminal()

    if not check_row(r_i, rows, cols):
        if not rows[r_i].move_one():
            advance = -1
            r_i += advance
            while True:
                for sq in squished[r_i]:
                    move_up_from(r_i, cols[sq])
                draw_in_terminal()
                if not rows[r_i].move_one():
                    r_i += advance
                else:
                    break
        draw_in_terminal()

    else:
        if not check_row(r_i, rows, cols, exact=True):
            squished[r_i] = []
            rbody = rows[r_i].body()
            for c in range(len(rbody)):
                if rbody[c] == '.' and cols[c].body()[r_i] == '#':
                    if squish_down_from(r_i, cols[c]):
                        squished[r_i].append(c)
            draw_in_terminal()

        if not check_row(r_i, rows, cols, exact=True):
            while True:
                for sq in squished[r_i]:
                    move_up_from(r_i, cols[sq])
                draw_in_terminal()
                if not rows[r_i].move_one():
                    advance = -1
                    r_i += advance
                else:
                    break
        else:
            advance = 1
            r_i += advance


for row in range(len(rows)):
    print(rows[row].body(), '|', end='')
    for col in range(len(cols)):
        print(cols[col].body()[row], end='')
    print('|')

draw_in_terminal()
terminal.printf(0, len(rows), 'Solved!')
terminal.refresh()
while terminal.read != terminal.TK_CLOSE:
    pass

terminal.close()
