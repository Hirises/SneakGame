import keyboard
import time
import random

#스크린 크기
screenX = 10
screenY = 10
#스크린 구성요소
ceil = '□ '
tail = '■ '
apple = '● '
#스크린 업데이트 틱
updateTick = 0.3
nextUpdateTick = 0
#현위치
headX = 0
headY = 0
#현재 길이
length = 3
#이전 위치
tails = []
#이동 방향 (기본 우측)
dirX = 1
dirY = 0
nextDirX = 1
nextDirY = 0
#사과 위치
appleX = 0
appleY = 0
#최고 점수
highscores = []
highscoreCount = 5
#게임 시작시 시간
startTime = 0

#화면 지우기
def clear_console():
    print("\n" * 30)
 
#화면 그리기
def draw():
    global headX
    global headY

    #clear_console()
    print("\n\n\n")
   
    screen = ''
    for _y in range(0, screenY):
        for _x in range(0, screenX):
            if (_x, _y) == (headX, headY):
                screen += tail
            elif (_x, _y) in tails:
                screen += tail
            elif (_x, _y) == (appleX, appleY):
                screen += apple
            else:
                screen += ceil
        screen += '\n'
    print(screen)
   
#키보드 입력 처리
def turn():
    global dirX
    global dirY
    global nextDirX
    global nextDirY
       
    if ( keyboard.is_pressed("w") or keyboard.is_pressed("up") ) and dirY != 1:
        nextDirX = 0
        nextDirY = -1
    if ( keyboard.is_pressed("s") or keyboard.is_pressed("down") ) and dirY != -1:
        nextDirX = 0
        nextDirY = 1
    if ( keyboard.is_pressed("a") or keyboard.is_pressed("left") ) and dirX != 1:
        nextDirX = -1
        nextDirY = 0
    if ( keyboard.is_pressed("d") or keyboard.is_pressed("right") ) and dirX != -1:
        nextDirX = 1
        nextDirY = 0
       
#움직임 처리
def move():
    global headX
    global headY
    global length
    global dirX
    global dirY
    global nextDirX
    global nextDirY
   
    #방향 변경
    dirX = nextDirX
    dirY = nextDirY
   
    #꼬리 처리
    if(len(tails) >= length):
        tails.remove(tails[0])
    tails.append((headX, headY))
   
    #머리 처리
    headX += dirX
    headY += dirY
   
    #월드 보더 처리
    if(headX < 0):
        headX = screenX - 1
    if(headY < 0):
        headY = screenY - 1
    if(headX >= screenX):
        headX = 0
    if(headY >= screenY):
        headY = 0
       
    #사과 처리
    if((headX, headY) == (appleX, appleY)):
        length += 1
        random_apple()
       
#사과 위치 이동
def random_apple():
    global appleX
    global appleY
   
    appleX = random.randint(0, screenX - 1)
    appleY = random.randint(0, screenY - 1)
   
    #현재 뱀의 위치에 생성되지 않도록
    while(is_collide(appleX, appleY) or (appleX, appleY) == (headX, headY)):
        appleX = random.randint(0, screenX - 1)
        appleY = random.randint(0, screenY - 1)

#꼬리와 충돌 여부 감지
def is_collide(_x, _y):
    global tails
   
    for pos in tails:
        if pos == (_x, _y):
            return True
   
    return False

#잘못된 입력값 에러 출력
def print_control_error():
    print("unsupported control\n")

#게임 리셋
def reset_game():
    global length
    global tails
    global headX
    global headY
    global dirX
    global dirY
    global nextDirX
    global nextDirY
    
    random_apple()
    length = 2
    tails.clear()
    headX = 0
    headY = 0
    dirX = 1
    dirY = 0
    nextDirX = 1
    nextDirY = 0

#게임 실행
def run_game():
    global nextUpdateTick

    nextUpdateTick = time.thread_time() + updateTick
   
    #게임 루프
    while(True):
        #게임 정지 확인
        if keyboard.is_pressed("q"):
            print_pause_menu()
            break
        
        #키보드 입력 감지
        turn()
       
        #업데이트 틱 확인
        if(nextUpdateTick <= time.thread_time()):
            #이동 처리
            move()
           
            #게임 종료 감지
            if length >= goal:
                print("\n\nyou are win!")
                compare_highscore(length)
                break
            elif is_collide(headX, headY):
                print("\n\ngame over")
                print("score : " + str(length))
                compare_highscore(length)
                break
           
            #화면 업데이트
            draw()
           
            #다음 업데이트 틱 설정
            nextUpdateTick = time.thread_time() + updateTick

#게임 정지 메뉴 출력
def print_pause_menu():
    clear_console()
    print("""
------------------------------

paused

""")
    print("score : " + str(length))
    print("""\

1 : continue
2 : restart
3 : back to menu

------------------------------\n""")

    while(True):
        control = input("control : ")
       
        if(control == "1"):
            #계속하기
            run_game()
            break
        elif(control == "2"):
            #다시하기
            reset_game()
            time.sleep(1)
            run_game()
            break
        elif(control == "3"):
            #뒤로가기
            break
        else:
            #오류
            print_control_error()

#설명서 출력
def print_help():
    clear_console()
    print("""
------------------------------

help

Use 'wasd' or 'arrows'
to move the sneak
press 'q' to pause game

Eat apple to grow up
Don`t hit your tail

1 : quit

------------------------------\n""")
   
    while(True):
        control = input("control : ")
       
        if(control == "1"):
            return
        else:
            print_control_error()
           
#하이스코어 확인
def compare_highscore(score):
    global highscores
   
    for i in range(1 - 1, highscoreCount):
        if highscores[i][1] <= score:
            name = input("\nyour name : ")
            highscores.insert(i, (name, score))
            highscores.pop(-1)
            return
       
#점수판 출력
def print_scoreboard():
    clear_console()
    print("""
------------------------------

scoreboard

""")
    surfix = "th"
    for i in range(1 - 1, highscoreCount):
        if i + 1 == 1:
            surfix = "st"
        elif i + 1 == 2:
            surfix = "nd"
        elif i + 1 == 3:
            surfix = "rd"
        else:
            surfix = "th"
        print(str(i + 1) + surfix + " : " + str(highscores[i][1]) + " " + str(highscores[i][0]))
    print("""\
         
1 : quit
         
------------------------------\n""")

    while(True):
        control = input("control : ")
       
        if(control == "1"):
            return
        else:
            print_control_error()

#씬 초기화
goal = screenX * screenY - 1
for i in range(1, highscoreCount + 1):
    highscores.append(("-", 0))

print("""\
------------------------------

Python Simple Sneak Game

            - made by Hirises

------------------------------""")

#약간 로딩되는 느낌을 주기 위한 대기
time.sleep(2)

#메인 루프
while(True):
    clear_console()
    print("""
------------------------------

1 : new game
2 : scoreboard
3 : help
4 : quit

------------------------------\n""")
       
    #메뉴 실행
    while(True):
        control = input("control : ")
       
        if(control == "1"):
            #게임 실행
            reset_game()
            time.sleep(1)
            run_game()
            break
        elif(control == "2"):
            #점수판
            print_scoreboard()
            break
        elif(control == "3"):
            #설명
            print_help()
            break
        elif(control == "4"):
            #나가기
            quit(0)
            break
        else:
            #오류
            print_control_error()
