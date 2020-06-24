import pygame as pg
import random
import math


def find_winner(bo, length=4):
    """
    it will show if a winner exist or not
    """
    rows = len(bo)
    columns = len(bo[0])
    global opp_player_marker

    for row in range(rows):
        for column in range(columns):
            if bo[row][column] == 0:
                continue

            if check_piece(bo, row, column, length)[0]:
                return True, opp_player_marker[str(bo[row][column])]

    return False, None


def check_piece(bo, row, column, length):
    """
    this will check all the part of board
    """
    rows = len(bo)
    columns = len(bo[0])

    for dr, dc in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1),):
        found_winner = True

        for i in range(1, length):
            r = row + dr * i
            c = column + dc * i

            if r not in range(rows) or c not in range(columns):
                found_winner = False
                break

            if bo[r][c] != bo[row][column]:
                found_winner = False
                break

        if found_winner:
            return True, (dr, dc)

    return False, (dr, dc)


def printBoard(bo):
    for i in range(len(bo)):
        if i == 0:
            print("- - - - - - - - - - - - - - -")
        for j in range(len(bo[0])):
            if j == 0:
                print("|", end="")

            if bo[i][j] == +1:
                print(" X |", end="")
            elif bo[i][j] == -1:
                print(" O |", end="")
            else:
                print("   |", end="")

        print("")
        print("- - - - - - - - - - - - - - -")
    print("")


def human_choose(bo, col):
    global turn
    global player_marker
    for i in reversed(range(len(bo))):
        if bo[i][col] == 0:
            bo[i][col] = player_marker["human"]
            turn = "ai"
            if find_winner(bo)[0]:
                return not True, "human"
            return not False, None


def all_possible_move(bo):
    possible = []
    for i in range(len(bo[0])):
        for j in range(len(bo)):
            if bo[j][i] == 0:
                possible.append(i)
                break
    return possible


def MIN(bo, max_depth, current_depth, hardness, alpha, beta):
    selected = 0
    global player_marker
    diff_depth = current_depth + 1
    all_possibles = all_possible_move(bo)

    v = +math.inf

    for i in all_possibles:
        chosen = None

        competing_value = 0

        for j in reversed(range(len(bo))):
            if bo[j][i] == 0:
                bo[j][i] = -1
                chosen = j
                break
        # printBoard(bo)
        end = find_winner(bo)
        if end[0]:
            board[chosen][i] = 0
            if end[1] == -1:
                competing_value = +math.inf, 0
            else:
                competing_value = -math.inf, 0
                board[chosen][i] = 0
                return competing_value[0], i
        elif not available(bo):
            competing_value = 0, 0
        elif current_depth == max_depth:
            if hardness == "hard":
                competing_value = competing_value + number_of_n_beside(bo, 1, +1, 1 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 2, +1, 2 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 3, +1, 3 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 1, -1, 4 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 2, -1, 8 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 3, -1, 12 * pow(10, diff_depth))
            competing_value = competing_value, 0
        else:
            competing_value = MAX(bo, max_depth, current_depth + 1, hardness, alpha, beta)

            if hardness == "hard":
                if current_depth != max_depth and current_depth >= 0:
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 1, +1, 1 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 2, +1, 2 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 3, +1, 3 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 1, -1, 4 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 2, -1, 8 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 3, -1, 12 * pow(20, diff_depth)),
                        competing_value[1])

        if competing_value[0] <= v:
            v = competing_value[0]
            selected = i
        board[chosen][i] = 0
        if v <= alpha:
            return v, selected

    return v, selected


def MAX(bo, max_depth, current_depth, hardness, alpha, beta):
    selected = 0
    global player_marker
    diff_depth = current_depth + 1
    all_possibles = all_possible_move(bo)

    v = -math.inf

    for i in all_possibles:
        chosen = None

        competing_value = 0

        for j in reversed(range(len(bo))):
            if bo[j][i] == 0:
                bo[j][i] = +1
                chosen = j
                break

        end = find_winner(bo)
        if end[0]:
            board[chosen][i] = 0
            if end[1] == +1:
                competing_value = -math.inf, 0
                board[chosen][i] = 0
                return competing_value[0], i
            else:
                competing_value = +math.inf, 0
        elif not available(bo):
            competing_value = 0, 0
        elif current_depth == max_depth:
            competing_value = 0

            if hardness == "hard":
                competing_value = competing_value + number_of_n_beside(bo, 1, +1, 4 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 2, +1, 8 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 3, +1, 12 * pow(10, diff_depth))

                competing_value = competing_value + number_of_n_beside(bo, 1, -1, 1 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 2, -1, 2 * pow(10, diff_depth))
                competing_value = competing_value + number_of_n_beside(bo, 3, -1, 3 * pow(10, diff_depth))

            competing_value = competing_value, 0
        else:
            competing_value = MIN(bo, max_depth, current_depth + 1, hardness, alpha, beta)
            if hardness == "hard":
                if current_depth != max_depth and current_depth >= 0:
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 1, +1, 4 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 2, +1, 8 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 3, +1, 12 * pow(20, diff_depth)),
                        competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 1, -1, 1 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 2, -1, 2 * pow(20, diff_depth)), competing_value[1])
                    competing_value = (
                        competing_value[0] + number_of_n_beside(bo, 3, -1, 3 * pow(20, diff_depth)), competing_value[1])

        if competing_value[0] >= v:
            v = competing_value[0]
            selected = i
        board[chosen][i] = 0
        if v >= beta:
            return v, selected

    return v, selected


def MiniMax(bo, fp, hardness):
    selected = None
    if fp:
        max1 = MAX(bo, 3, 0, hardness, -math.inf, math.inf)
        selected = max1[1]
    else:
        min1 = MIN(bo, 3, 0, hardness, -math.inf, math.inf)
        selected = min1[1]

    return selected


def ai_choose(bo, self, rival, hardness):
    global turn
    selected = None
    global player_marker
    selected = MiniMax(bo, first_player == self, hardness)
    for i in reversed(range(len(bo))):

        if bo[i][selected] == 0:
            bo[i][selected] = player_marker[self]
            turn = rival
            if find_winner(bo)[0]:
                return not True, self
            return not False, None


def available(bo):
    for i in range(len(bo[0])):
        for j in range(len(bo)):
            if bo[j][i] == 0:
                return True
    return False


def number_of_n_beside(bo, n, who, m):
    returned = 0
    for i in range(len(bo)):
        for j in range(len(bo[0]) - 3):
            check = bo[i][j:j + 4]

            number_of_who = 0
            number_of_zero = 0

            for p in check:
                if p == 0:
                    number_of_zero = number_of_zero + 1
                elif p == who:
                    number_of_who = number_of_who + 1

            if number_of_zero == 4 - n and number_of_who == n:
                returned = returned + (n * who * m)

    transpose_bo = rez = [[bo[j][i] for j in range(len(bo))] for i in range(len(bo[0]))]

    for i in range(len(transpose_bo)):
        for j in range(len(transpose_bo[0]) - 3):
            check = transpose_bo[i][j:j + 4]
            number_of_who = 0
            number_of_zero = 0

            for p in check:
                if p == 0:
                    number_of_zero = number_of_zero + 1
                elif p == who:
                    number_of_who = number_of_who + 1

            if number_of_zero == 4 - n and number_of_who == n:
                returned = returned + (n * who * m)

    for i in range(len(bo)):
        for j in reversed(range(len(bo[0]))):
            start_y = i
            start_x = j
            di = [bo[i][j]]
            while start_x - 1 >= 0 and start_y + 1 < len(bo) and len(di) < 4:
                start_y = start_y + 1
                start_x = start_x - 1
                di.append(bo[start_y][start_x])
            if len(di) >= 4:
                number_of_who = 0
                number_of_zero = 0

                for p in di:
                    if p == 0:
                        number_of_zero = number_of_zero + 1
                    elif p == who:
                        number_of_who = number_of_who + 1

                if number_of_zero == 4 - n and number_of_who == n:
                    returned = returned + (n * who * m)

    for i in range(len(bo)):
        for j in range(len(bo[0])):
            start_y = i
            start_x = j
            di = [bo[i][j]]
            while start_x + 1 < len(bo[0]) and start_y + 1 < len(bo) and len(di) < 4:
                start_y = start_y + 1
                start_x = start_x + 1
                di.append(bo[start_y][start_x])
            if len(di) >= 4:
                number_of_who = 0
                number_of_zero = 0

                for p in di:
                    if p == 0:
                        number_of_zero = number_of_zero + 1
                    elif p == who:
                        number_of_who = number_of_who + 1

                if number_of_zero == 4 - n and number_of_who == n:
                    returned = returned + (n * who * m)
    return returned


def find_pos_of_winner(bo, length=4):
    rows = len(bo)
    columns = len(bo[0])

    for row in range(rows):
        for column in range(columns):
            if bo[row][column] == 0:
                continue

            check = check_piece(bo, row, column, length)
            if check[0]:
                return (row, column), (row + check[1][0] * 3, column + check[1][1] * 3)

    return None


def playGame(bo):
    pg.init()
    win = pg.display.set_mode((715, 700))
    win.fill((255, 255, 255))
    pg.display.set_caption("4 Connect")

    action = None
    global first_player
    second_player = None
    run = True
    choose_first_one = False
    choose_ai_ai_hardness = False
    rival = None

    '''
    first menu that user will choose between (AI vs AI) or (Ai vs Human)
    '''
    while run:
        pg.time.delay(0)

        hover_pos = pg.mouse.get_pos()
        Rectangles = []

        if 450 > hover_pos[0] > 200 and 190 > hover_pos[1] > 130:
            rec = pg.draw.rect(win, (200, 200, 200), (250, 130, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (250, 130, 200, 60))
        Rectangles.append(rec)

        if 450 > hover_pos[0] > 200 and 360 > hover_pos[1] > 300:
            rec = pg.draw.rect(win, (200, 200, 200), (250, 300, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (250, 300, 200, 60))
        Rectangles.append(rec)

        pg.font.init()
        myFont = pg.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render("AI vs Human", False, (0, 0, 0))
        win.blit(textSurface, (290, 150))

        pg.font.init()
        myFont = pg.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render("AI vs AI", False, (0, 0, 0))
        win.blit(textSurface, (310, 320))

        textSurface = myFont.render("Choose Game Mode : ", False, (0, 0, 0))
        win.blit(textSurface, (50, 50))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                for i in range(len(Rectangles)):
                    if Rectangles[i].collidepoint(pos):
                        if i == 0:
                            run = False
                            choose_first_one = True
                            choose_ai_ai_hardness = False
                            rival = "human"
                        else:
                            run = False
                            choose_first_one = False
                            choose_ai_ai_hardness = True
                            rival = "ai2"

            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()

    if not choose_first_one:
        first_player = "ai"
        second_player = "ai2"

    win.fill((255, 255, 255))
    choose_hardness = False

    '''
    if user in last menu choose AI vs Human This menu gonna be up in order to choose the first player
        user will choose between (AI) or (Human)
    '''

    while choose_first_one:
        pg.time.delay(0)

        hover_pos = pg.mouse.get_pos()
        Rectangles = []

        if 450 > hover_pos[0] > 200 and 190 > hover_pos[1] > 130:
            rec = pg.draw.rect(win, (200, 200, 200), (250, 130, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (250, 130, 200, 60))
        Rectangles.append(rec)

        if 450 > hover_pos[0] > 200 and 360 > hover_pos[1] > 300:
            rec = pg.draw.rect(win, (200, 200, 200), (250, 300, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (250, 300, 200, 60))
        Rectangles.append(rec)

        pg.font.init()
        myFont = pg.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render("AI", False, (0, 0, 0))
        win.blit(textSurface, (340, 320))

        textSurface = myFont.render("Human", False, (0, 0, 0))
        win.blit(textSurface, (319, 150))

        textSurface = myFont.render("Choose First Player : ", False, (0, 0, 0))
        win.blit(textSurface, (50, 50))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                for i in range(len(Rectangles)):
                    if Rectangles[i].collidepoint(pos):
                        if i == 0:
                            first_player = "human"
                            second_player = "ai"
                            choose_first_one = False
                            choose_hardness = True
                        else:
                            first_player = "ai"
                            second_player = "human"
                            choose_first_one = False
                            choose_hardness = True

            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()

    win.fill((255, 255, 255))
    hardness = "hard"
    hardness2 = "hard"

    '''
    if user in last menu choose AI vs Human and after choosing first player This menu gonna be up 
    in order to choose the hardness of game
        user will choose between (Easy) or (Hard)
    '''

    while choose_hardness:
        pg.time.delay(0)

        hover_pos = pg.mouse.get_pos()
        Rectangles = []

        if 450 > hover_pos[0] > 200 and 190 > hover_pos[1] > 130:
            rec = pg.draw.rect(win, (200, 200, 200), (250, 130, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (250, 130, 200, 60))
        Rectangles.append(rec)

        if 450 > hover_pos[0] > 200 and 360 > hover_pos[1] > 300:
            rec = pg.draw.rect(win, (200, 200, 200), (250, 300, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (250, 300, 200, 60))
        Rectangles.append(rec)

        pg.font.init()
        myFont = pg.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render("Hard", False, (0, 0, 0))
        win.blit(textSurface, (340, 320))

        textSurface = myFont.render("Easy", False, (0, 0, 0))
        win.blit(textSurface, (319, 150))

        textSurface = myFont.render("Choose Hardness : ", False, (0, 0, 0))
        win.blit(textSurface, (50, 50))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                for i in range(len(Rectangles)):
                    if Rectangles[i].collidepoint(pos):
                        if i == 0:
                            hardness = "easy"
                            choose_hardness = False
                        else:
                            hardness = "hard"
                            choose_hardness = False

            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()

    '''
    if user in last menu choose AI vs AI
    in order to choose the hardness of each AI
        user will choose between (Easy) or (Hard)
    '''

    while choose_ai_ai_hardness:
        win.fill((255, 255, 255))
        pg.time.delay(0)

        hover_pos = pg.mouse.get_pos()
        Rectangles = []

        if 300 > hover_pos[0] > 100 and 310 > hover_pos[1] > 200:
            rec = pg.draw.rect(win, (200, 200, 200), (100, 250, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (100, 250, 200, 60))
        Rectangles.append(rec)

        if 300 > hover_pos[0] > 100 and 460 > hover_pos[1] > 400:
            rec = pg.draw.rect(win, (200, 200, 200), (100, 400, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (100, 400, 200, 60))
        Rectangles.append(rec)

        if 600 > hover_pos[0] > 400 and 310 > hover_pos[1] > 200:
            rec = pg.draw.rect(win, (200, 200, 200), (400, 250, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (400, 250, 200, 60))
        Rectangles.append(rec)

        if 600 > hover_pos[0] > 400 and 460 > hover_pos[1] > 400:
            rec = pg.draw.rect(win, (200, 200, 200), (400, 400, 200, 60))
        else:
            rec = pg.draw.rect(win, (100, 100, 100), (400, 400, 200, 60))
        Rectangles.append(rec)

        if 450 > hover_pos[0] > 250 and 610 > hover_pos[1] > 550:
            rec = pg.draw.rect(win, (200, 0, 0), (250, 550, 200, 60))
        else:
            rec = pg.draw.rect(win, (150, 0, 0), (250, 550, 200, 60))
        Rectangles.append(rec)

        pg.font.init()
        myFont = pg.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render("Hard", False, (0, 0, 0))
        win.blit(textSurface, (170, 420))

        textSurface = myFont.render("Easy", False, (0, 0, 0))
        win.blit(textSurface, (170, 270))

        textSurface = myFont.render("Hard", False, (0, 0, 0))
        win.blit(textSurface, (470, 420))

        textSurface = myFont.render("Easy", False, (0, 0, 0))
        win.blit(textSurface, (470, 270))

        textSurface = myFont.render("Start", False, (0, 0, 0))
        win.blit(textSurface, (320, 568))

        textSurface = myFont.render("Choose hardness of each AI : ", False, (0, 0, 0))
        win.blit(textSurface, (50, 50))

        textSurface = myFont.render("AI 1 : " + hardness, False, (0, 0, 0))
        win.blit(textSurface, (180, 200))

        textSurface = myFont.render("AI 2 : " + hardness2, False, (0, 0, 0))
        win.blit(textSurface, (480, 200))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                for i in range(len(Rectangles)):
                    if Rectangles[i].collidepoint(pos):
                        if i == 0:
                            hardness = "easy"
                        elif i == 1:
                            hardness = "hard"
                        elif i == 2:
                            hardness2 = "easy"
                        elif i == 3:
                            hardness2 = "hard"
                        elif i == 4:
                            choose_ai_ai_hardness = False

            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()

    global turn
    turn = first_player
    global player_marker
    global opp_player_marker

    player_marker[first_player] = 1
    player_marker[second_player] = -1

    opp_player_marker["1"] = first_player
    opp_player_marker["-1"] = second_player

    if first_player == "ai":
        ai_choose(bo, "ai", rival, hardness)
    if first_player == "ai2":
        ai_choose(bo, "ai2", rival, hardness2)

    win.fill((255, 255, 255))
    run = True
    winner = None

    '''
    Main game play:
    in this part board will be shown and the after every choosing the board will refresh
    '''

    while run:

        win.fill((255, 255, 255))
        pg.font.init()
        myFont = pg.font.SysFont('Comic Sans MS', 30)

        pg.draw.circle(win, (71, 172, 254), (40, 20), 15)
        textSurface = myFont.render(" : " + first_player, False, (0, 0, 0))
        win.blit(textSurface, (50, 10))

        pg.draw.circle(win, (251, 209, 35), (40, 55), 15)
        textSurface = myFont.render(" : " + second_player, False, (0, 0, 0))
        win.blit(textSurface, (50, 45))

        textSurface = myFont.render("turn : " + turn, False, (0, 0, 0))
        win.blit(textSurface, (30, 80))

        pg.draw.circle(win, (0, 0, 0), (40, 20), 15)
        pg.draw.circle(win, (255, 0, 0), (40, 55), 15)

        pg.time.delay(0)

        hover_pos = pg.mouse.get_pos()

        Rectangles = []

        for i in range(7):

            if 30 + (i * 100) + 60 > hover_pos[0] > 30 + (i * 100) and \
                    190 > hover_pos[1] > 130 and turn == "human" and rival == "human":
                rec = pg.draw.rect(win, (111, 137, 212), (30 + (i * 100), 130, 60, 60))
            else:
                rec = pg.draw.rect(win, (115, 137, 155), (30 + (i * 100), 130, 60, 60))
            Rectangles.append(rec)
            textSurface = myFont.render(str(i + 1), False, (0, 0, 0))
            win.blit(textSurface, ((30 + (i * 100) + 60) - 35, 150))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                for i in range(len(Rectangles)):
                    if Rectangles[i].collidepoint(pos) and turn == "human" and rival == "human":
                        if not available(bo):
                            run, winner = False, "No Person"
                        else:
                            run, winner = human_choose(bo, i)

            if event.type == pg.QUIT:
                run = False

        for i in range(len(bo[0])):
            for j in range(len(bo)):
                color = None
                if bo[j][i] == 1:
                    color = (0, 0, 0)
                elif bo[j][i] == -1:
                    color = (255, 0, 0)
                else:
                    color = (165, 167, 182)
                pg.draw.circle(win, color, (60 + (i * 100), 240 + (j * 80)), 30)
        if turn == "ai" and run:
            if not available(bo):
                run, winner = False, "No Person"
            else:
                myFont2 = pg.font.SysFont('Comic Sans MS', 40)
                textSurface = myFont2.render("Waiting... ", False, (0, 0, 0))
                win.blit(textSurface, (500, 50))
                pg.display.update()
                run, winner = ai_choose(bo, "ai", rival, hardness)

                textSurface = myFont2.render("Waiting... ", False, (255, 255, 255))
                win.blit(textSurface, (500, 50))

        elif turn == "ai2":
            if not available(bo):
                run, winner = False, "No Person"
            else:
                myFont2 = pg.font.SysFont('Comic Sans MS', 40)
                textSurface = myFont2.render("Waiting... ", False, (0, 0, 0))
                win.blit(textSurface, (500, 50))
                pg.display.update()
                run, winner = ai_choose(bo, "ai2", "ai", hardness2)

                textSurface = myFont2.render("Waiting... ", False, (255, 255, 255))
                win.blit(textSurface, (500, 50))
        else:
            pg.display.update()

    '''
    after Ending game this window gonna show the result
    it contain the name of winner (human , ai , ai2)
    and showing the winner place by drawing a line
    '''
    run = True
    while run:

        win.fill((255, 255, 255))
        pg.font.init()
        myFont = pg.font.SysFont('Comic Sans MS', 30)
        myFont2 = pg.font.SysFont('Comic Sans MS', 40)

        textSurface = myFont2.render("Winner is : " + str(winner), False, (0, 0, 0))
        win.blit(textSurface, (235, 50))

        pg.time.delay(0)

        for i in range(7):
            pg.draw.rect(win, (115, 137, 155), (30 + (i * 100), 130, 60, 60))
            textSurface = myFont.render(str(i + 1), False, (0, 0, 0))
            win.blit(textSurface, ((30 + (i * 100) + 60) - 35, 150))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        for i in range(len(bo[0])):
            for j in range(len(bo)):

                color = None
                if bo[j][i] == 1:
                    color = (0, 0, 0)
                elif bo[j][i] == -1:
                    color = (255, 0, 0)
                else:
                    color = (165, 167, 182)
                pg.draw.circle(win, color, (60 + (i * 100), 240 + (j * 80)), 30)

        winner_pos = find_pos_of_winner(bo)
        if winner_pos:
            l1 = None
            l2 = None
            for i in range(len(bo[0])):
                for j in range(len(bo)):
                    if i == winner_pos[0][1] and j == winner_pos[0][0]:
                        l1 = (i * 100 + 60, 240 + j * 80)
                    if i == winner_pos[1][1] and j == winner_pos[1][0]:
                        l2 = (i * 100 + 60, 240 + j * 80)
            pg.draw.line(win, (0, 0, 255), l1, l2)
        pg.display.update()

    pg.quit()
    print("Winner : " + winner)


player_marker = {
    "human": 0,
    "ai": 0,
    "ai2": 0
}

opp_player_marker = {
    "-1": "",
    "1": ""
}

first_player = None
turn = None

board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

playGame(board)