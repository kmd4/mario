# 0 - None
# 1 - cloud
# 2 - big_cloud
# 3 - кирпичи
# 4 - ground
# 5 - bush
# 6 - big_bush
# 7 - hill
# 8 - big_hill
# 9 - ?
# 10 - tube_little
# 11 - tube_medium
# 12 - tube_big
# 13 - block
# 14 - little_castle
# 15 - stick
# 16 - turtle
# 17 - mushroom
# 18 = money
# 19 - mush_power
# 20 - mario


class World_1():

    map = [
        223 * [0],

        10 * [0] + [1] + 40 * [0] + [2] + 34 * [0] + [1] + 30 * [0] + [1] + 39 * [0] + [2] + 20 * [0] + [1] + 7 * [0] + [1] + 4 * [0] + [2] + 14 * [0] + [1] + 16 * [0],

        23 * [0] + [1] + 30 * [0] + [2] + 7 * [0] + [1] + 35 * [0] + [2] + 14 * [0] + [1] + 40 * [0] + [2] + 26 * [0] + [1] + 23 * [0] + [1] + 17 * [0],

        80 * [0] + [17, 0, 17] + 140 * [0],

        22 * [0] + [9] + 57 * [0] + 8 * [3] + 3 * [0] + 3 * [3] + [9] + 14 * [0] + [9] + 11 * [0] + 3 * [3] + 4 * [0] + [3, 9, 9, 3] + 57 * [0] + \
        2 * [13] + 32 * [0],

        188 * [0] + 3 * [13] + 32 * [0],

        187 * [0] + 4 * [13] + 32 * [0],

        186 * [0] + 5 * [13] + 32 * [0],

        16 * [0] + [9] + 3 * [0] + [3, 9, 3, 9, 3] + 52 * [0] + 3 * [3] + 14 * [0] + [3] + 5 * [0] + 2 * [3] + 4 * [0] + [9, 0, 0, 9, 0, 0, 9] + \
            5 * [0] + [3] + 10 * [0] + 2 * [3] + 6 * [0] + [13, 0, 0, 13] + 11 * [0] + 2 * [13] + [0, 0, 13] + 12 * [0] + \
            [3, 3, 9, 3] + 12 * [0] + 6 * [13] + 32 * [0],

        136 * [0] + 2 * [13] + 2 * [0] + 2 * [13] + 9 * [0] + 3 * [13] + 2 * [0] + 2 * [13] + 26 * [0] + 7 * [13] + 32 * [0],

        135 * [0] + 3 * [13] + 2 * [0] + 3 * [13] + 7 * [0] + 4 * [13] + 2 * [0] + 3 * [13] + 24 * [0] + 8 * [13] + 32 * [0],

        [8] + 2 * [0] + [20] + 8 * [0] + [6, 0, 0, 0, 7] + 2 * [0] + [17] + 3 * [0] + [16, 5] + 3 * [0] + [10] + 9 * [0] + [11, 0, 17, 0, 5] + 3 * [0] + [12, 0,  8] + 2 * [0] + 2 * [17] + 4 * [0] + [12, 0, 0, 6, 0, 0, 0, 7, 0, 0] + 5 * [0] +\
            [5] + 17 * [0] + [6] + 5 * [0] + [8] + [0, 17, 17] + 7 * [0] + [16, 6, 0, 0, 0, 7] + [0, 0, 17, 17] + 3 * [0] + [5] + 3 * [0] + [17, 17] + 4 * [0] + 2 * [17] + 2 * [0] + 4 * [13] + 2 * [0] + 4 * [13] + [8] + 4 * [0] + 5 * [13] + 2 * [0] + 4 * [13] +\
            [0, 7, 0, 0, 10] + 4 * [0] + [5] + 6 * [0] + 2 * [17] + 2 * [0] + [10, 0] + 9 * [13] + 2 * [0] + [8] + 5 * [0] + [20] + 3 * [0] + [14] + 5 * [0] + [7] + 7 * [0] + [5] + 5 * [0],

        69 * [4] + 2 * [0] + 15 * [4] + 3 * [0] + 65 * [4] + 2 * [0] + 67 * [4],

        69 * [4] + 2 * [0] + 15 * [4] + 3 * [0] + 65 * [4] + 2 * [0] + 67 * [4]
    ]
    for i in range(len(map)):
        map[i] = map[i][190:]
    bonuses = [[18], [18], [19], [18], [18], [18], [19], [18], [19], [18], [18], [18]]

class World_2:
    map = [
        205 * [0],

        10 * [0] + [1] + 40 * [0] + [2] + 34 * [0] + [1] + 30 * [0] + [1] + 39 * [0] + [2] + 20 * [0] + [1] + 7 * [
            0] + [1] + 4 * [0] + [2] + 13 * [0],

        23 * [0] + [1] + 30 * [0] + [2] + 7 * [0] + [1] + 35 * [0] + [2] + 14 * [0] + [1] + 40 * [0] + [2] + 26 * [
            0] + [1] + 23 * [0],

        205 * [0],

        205 * [0],

        205 * [0],
        56 * [0] + [9] + 2 * [3] + 70 * [0] + [9] + 25 * [0] + 4 * [3] + 46 * [0],
        205 * [0],

        205 * [0],

        205 * [0],

        205 * [0],

        [0, 20] + 7 * [0] + [8] + 8 * [0] + [16] + 6 * [0] + [11] + 4 * [0] + [5] + 5 * [0] + [17] + 3 * [0] + [6] + 10 * [0] + \
            2 * [17] + 9 * [0] + [10] + 4 *[0] + [11] + 5 * [0] + 2 * [17] + 5 * [0] + [7] + 6 * [0] + [6] + 8 * [0] + [11] +\
            8 * [0] + [17] + 3 * [0] + [6] + 14 * [0] + [16] + 9 * [0] + 2 * [17] + 7 * [0] + [11] + 7 * [0] + [5] + 9 * [0] + \
            [17] + 4 * [0] + [8] + 10 * [0] + [14] + 8 * [0] + [6] + 7 * [0] + [7] + 10 * [0],

        117 * [4] + 2 * [0] + 86 * [4],

        117 * [4] + 2 * [0] + 86 * [4]
    ]

    bonuses = [[18], [18], [19], [18], [18], [18], [19], [18], [19], [18], [18], [18], [18], [18], [19], [18], [18], [18], [19], [18], [19], [18], [18], [18]]




