def delLine():
    with open(r"klikacka/leaderboard.ini", 'r') as file:
        lines = file.readlines()

    # delete matching content
    content = "marek:140"
    with open(r"klikacka/leaderboard.ini", 'w') as file:
        for line in lines:
            # readlines() includes a newline character
            if line.strip("\n") != content:
                file.write(line)

delLine()




def delLine(full):
    with open(r"klikacka/leaderboard.ini", 'r') as file:
        lines = file.readlines()

    # delete matching content
    content = full
    with open(r"klikacka/leaderboard.ini", 'w') as file:
        for line in lines:
            # readlines() includes a newline character
            if line.strip("\n") != content:
                file.write(line)