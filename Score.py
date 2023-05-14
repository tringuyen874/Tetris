def last_score():
    with open("Tetris/score.txt", 'r', encoding='utf8') as f:
        lines = f.readline().split()
        last_score = int(lines[0])
        # player = lines[1]
        
    return last_score

def update_score(newScore = 0):
    with open("Tetris/score.txt", 'w') as f:
        f.write((str(newScore)))

def high_score():
    with open("Tetris/highscore.txt", 'r') as f:
        lines = f.readlines()
        high_score = lines[0].strip()
        high_score_name = lines[1].strip()
    return high_score, high_score_name 

def update_high_score(lastScore, user_text):
    highScore, high_score_name = high_score()
    with open("Tetris/highscore.txt", 'w') as f:
        if (int(highScore) > int(lastScore)):
            f.write(str(highScore))
            f.write('\n')
            f.write(high_score_name)
        else:
            f.write(str(lastScore))
            f.write('\n')
            f.write(user_text)