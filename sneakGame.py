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
global dirX
global dirY
dirX = 1
dirY = 0
#사과 위치
appleX = 0
appleY = 0
 
#화면 그리기
def draw():
    screen = ''
    for _y in range(0, screenY):
        for _x in range(0, screenX):
            if (_x, _y) in tails:
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
   
    if keyboard.is_pressed("w") and dirY != 1:
        dirX = 0
        dirY = -1
    if keyboard.is_pressed("s") and dirY != -1:
        dirX = 0
        dirY = 1
    if keyboard.is_pressed("a") and dirX != 1:
        dirX = -1
        dirY = 0
    if keyboard.is_pressed("d") and dirX != -1:
        dirX = 1
        dirY = 0
       
       
#움직임 처리
def move():
    global headX
    global headY
    global length
   
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
        randomApple()
       
#사과 위치 이동
def randomApple():
    global appleX
    global appleY
   
    appleX = random.randint(0, screenX - 1)
    appleY = random.randint(0, screenY - 1)

#머리 - 꼬리 충돌 감
def collide():
    global tails
    global headX
    global headY
   
    for pos in tails:
        if pos == (headX, headY):
            return True
   
    return False

randomApple()
goal = screenX * screenY - 1
nextUpdateTick = time.thread_time() + updateTick

while(True):
    #키보드 입력 감지
    turn()
   
    #업데이트 틱 확인
    if(time.thread_time() >= nextUpdateTick):
        move()
        nextUpdateTick = time.thread_time() + updateTick
       
    #게임 종료 감지
    if length >= goal:
        print("\n\nyou are win!\n")
        break
    elif collide():
        print("\n\ngame over\n")
        break
    else:
        draw()
