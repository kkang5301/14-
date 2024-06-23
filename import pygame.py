import pygame, math, time, os, random

#게임 모듈 초기화
pygame.init()

#음악 경로 설정 및 재생
pygame.display.set_caption("import pygame.py")
sound = pygame.mixer.Sound("pupa.mp3")
sound.play(-1)

#시작 마우스 위치
from pynput.mouse import Controller
mouse = Controller()
mouse.position = (956, 450)

#창 크기 조절
w = 1200
#창 비율 조절
h = w * (3.5/5)

#창 키기
screen = pygame.display.set_mode((w, h))

#프레임 단위를 위한 시간구현
clock = pygame.time.Clock()

#불 형태로 창 입력
main = True
ingame = True

#스킨용
spin = 0

#4키
keys = [0, 0, 0, 0]
keyset = [0, 0, 0, 0]

#프레임 구현
maxframe = 60
fps = 0

#노트 속도 계산용
gst = time.time()
Time = time.time() - gst

ty = 0 #노트
tst = Time #노트 소환 간격

#4키 빈 리스트
t1 = []
t2 = []
t3 = []
t4 = []

Cpath = os.path.dirname(__file__)
Fpath = os.path.join("font")

#폰트
rate = "PERFECT"
#ingame_font_rate = pygame.font.Font(os.path.join(Fpath, "1.otf"), int(w / 23))
ingame_font_rate = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int(w / 50))
rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))

#노트 소환
def sum_note(n):
  if n == 1:
    ty = 0
    tst = Time + 2
    t1.append([ty, tst])
  if n == 2:
    ty = 0
    tst = Time + 2
    t2.append([ty, tst])
  if n == 3:
    ty = 0
    tst = Time + 2
    t3.append([ty, tst])
  if n == 4:
    ty = 0
    tst = Time + 2
    t4.append([ty, tst])

#노트 속도
speed = 3

#노트 자동 생성
notesumt = 0
a = 0
aa = 0

#인게임 판정용
combo = 0
combo_effect = 0
combo_effect2 = 0
last_combo = 0
miss_anim = 0
combo_time = Time + 1

#판정용
rate_data = [0, 0, 0, 0]

#판정
def rating(n):
  global combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate
  if abs((h/12.9) * 9 - rate_data[n - 1] < 300 * speed * (h/900) and (h/12.9) * 9 - rate_data[n - 1] >= 200 * speed * (h/900)):
    last_combo = combo
    miss_anim = 1
    combo = 0
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "WORST"
  if abs((h/12.9) * 9 - rate_data[n - 1] < 200 * speed * (h/900) and abs((h/12.9) * 9 - rate_data[n - 1]) >= 100 * speed * (h/900)):
    last_combo = combo
    miss_anim = 1
    combo = 0
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "BAD"
  if abs((h/12.9) * 9 - rate_data[n - 1] < 150 * speed * (h/900) and abs((h/12.9) * 9 - rate_data[n - 1]) >= 50 * speed * (h/900)):
    combo += 1
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "GOOD"
  if abs((h/12.9) * 9 - rate_data[n - 1] < 50 * speed * (h/900) and abs((h/12.9) * 9 - rate_data[n - 1]) >= 15 * speed * (h/900)):
    combo += 1
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "GREAT"
  if abs((h/12.9) * 9 - rate_data[n - 1] < 15 * speed * (h/900) and abs((h/12.9) * 9 - rate_data[n - 1]) >= 0 * speed * (h/900)):
    combo += 1
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "PERFECT"

#스파클 효과
sparks = []

class Spark():
    def __init__(self, loc, angle, speed, color, scale=1):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sign = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]


    #스파클 떨어짐 효과
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])

    #스파클 움직임
    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        #스파클 범위
        self.speed -= 0.005

        if self.speed <= 0:
            self.alive = False

    #스파클 그리기
    def draw(self, surf):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                ]
            pygame.draw.polygon(surf, self.color, points)

while main:
  while ingame:
    if len(t1) > 0:
      rate_data[0] = t1[0][0]
    if len(t2) > 0:
      rate_data[1] = t2[0][0]
    if len(t3) > 0:
      rate_data[2] = t3[0][0]
    if len(t4) > 0:
      rate_data[3] = t4[0][0]

    #소환딜레이
    if Time > 0.2 * notesumt:
      notesumt += 1
      while a == aa:
        a = random.randint(1, 4)
      sum_note(a)
      aa = a

    Time = time.time() - gst

    #프레임 구간 구현
    fps = clock.get_fps()

    #폰트 색,모양
    #ingame_font_combo = pygame.font.Font(os.path.join(Fpath, "1.otf"), int((w / 38) * combo_effect2))
    ingame_font_combo = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int((w / 50) * combo_effect2))
    combo_text = ingame_font_combo.render(str(combo), False, ( 255, 255, 255))

    #판정영어 색
    rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))
    rate_text = pygame.transform.scale(rate_text, (int(w / 110 * len(rate) * combo_effect2), int((w / 58 * combo_effect * combo_effect2))))

    #판정선에서 벗어난 미스
    #ingame_font_miss = pygame.font.Font(os.path.join(Fpath, "1.otf"), int((w / 38 * miss_anim)))
    ingame_font_miss = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int((w / 70 * miss_anim)))
    miss_text = ingame_font_miss.render(str(last_combo), False, (255, 0, 0))

    #프레임 0 에러 발생 방지
    if fps == 0:
      fps == maxframe

    #창 끄기
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      #조작키 입력 설정
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_a:
            keyset[0] = 1
            if len(t1) > 0:
              if t1[0][0] > h / 3:
                rating(1)
                del t1[0]
          if event.key == pygame.K_s:
            keyset[1] = 1
            if len(t2) > 0:
              if t2[0][0] > h / 3:
                rating(2)
                del t2[0]
          if event.key == pygame.K_d:
            keyset[2] = 1
            if len(t3) > 0:
              if t3[0][0] > h / 3:
                rating(3)
                del t3[0]
          if event.key == pygame.K_f:
            keyset[3] = 1
            if len(t4) > 0:
              if t4[0][0] > h / 3:
                rating(4)
                del t4[0]
      if event.type == pygame.KEYUP:
          if event.key == pygame.K_a:
            keyset[0] = 0
          if event.key == pygame.K_s:
            keyset[1] = 0
          if event.key == pygame.K_d:
            keyset[2] = 0
          if event.key == pygame.K_f:
            keyset[3] = 0

    #RGB로 바탕 색상 정하기
    screen.fill((0, 0, 0))

    if fps == 0:
      fps = 60

    #터치 이펙트 움직임 감속 (숫자랑 비례)
    keys[0] += (keyset[0] - keys[0]) / (2.5 * (maxframe / fps))
    keys[1] += (keyset[1] - keys[1]) / (2.5 * (maxframe / fps))
    keys[2] += (keyset[2] - keys[2]) / (2.5 * (maxframe / fps))
    keys[3] += (keyset[3] - keys[3]) / (2.5 * (maxframe / fps))

    #콤보 이펙트
    if Time > combo_time:
      combo_effect += (0 - combo_effect) / (7 * (maxframe / fps))
    if Time < combo_time:
      combo_effect += (1 - combo_effect) / (7 * (maxframe / fps))
    combo_effect2 += (2 - combo_effect2) / (7 * (maxframe / fps))
    miss_anim += (4 - miss_anim) / (14 * (maxframe / fps))

    #마우스 이펙트
    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(0.85)
        spark.draw(screen)
        if not spark.alive:
            sparks.pop(i)
    mx, my = pygame.mouse.get_pos()
    sparks.append(Spark([mx, my], math.radians(random.randint(0, 360)), random.randint(3, 6), (160, 160, 160), 2))

    #스킨================================================================================================================================================================================================================================================
    #다운노트 창 배경
    pygame.draw.rect(screen, (0, 0, 0), (w / 2 - w / 8, -int(w / 100), w / 4, h + int(w/50)))
    
    #세로 흰색 경계선
    pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, -int(w / 100), w / 4, h + int(w/50)), int(w / 100))

    #노트 구현
    #만들어 둔 노트 복제
    for tile_data in t1:#첫번째(h / number) = 판정위치
      tile_data[0] = (h /12.9) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900) #버퍼링에도 노트 일정하게 동작
      pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, tile_data[0] - h /100, w / 16, h / 50))
      
      #미스 노트 삭제
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t1.remove(tile_data)

    for tile_data in t2:
      tile_data[0] = (h /12.9) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900) 
      pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 16, tile_data[0] - h /100, w / 16, h / 50))
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t2.remove(tile_data)

    for tile_data in t3:
      tile_data[0] = (h /12.9) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900) 
      pygame.draw.rect(screen, (255, 255, 255), (w / 2, tile_data[0] - h /100, w / 16, h / 50))
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t3.remove(tile_data)

    for tile_data in t4:
      tile_data[0] = (h /12.9) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900) 
      pygame.draw.rect(screen, (255, 255, 255), (w / 2 + w / 16, tile_data[0] - h /100, w / 16, h / 50))
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t4.remove(tile_data)

    #인게임 키 입력 시 이펙트
    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 - w / 8 + w / 32 - (w / 32) * keys[0], (h / 12.7) * 9 - (h / 30) * keys[0] * i, w / 16 * keys[0], (h / 35) / i))
    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 - w / 16 + w / 32 - (w / 32) * keys[1], (h / 12.7) * 9 - (h / 30) * keys[1] * i, w / 16 * keys[1], (h / 35) / i))
    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 + w / 32 - (w / 32) * keys[2], (h / 12.7) * 9 - (h / 30) * keys[2] * i, w / 16 * keys[2], (h / 35) / i))
    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 + w / 16 + w / 32 - (w / 32) * keys[3], (h / 12.7) * 9 - (h / 30) * keys[3] * i, w / 16 * keys[3], (h / 35) / i))
   

    #판정선
    pygame.draw.rect(screen, (0, 0, 0), (w / 2 - w / 8, (h / 12.9) * 9, w / 4, h / 2))
    pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, (h / 12.9) * 9, w / 4, h / 2), int(h / 70))

    #디자인1
    pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, (h / 12) * 9, w / 4, h / 2), int(h / 150))
    pygame.draw.rect(screen, (0, 0, 0), (w / 2 - w / 8, (h / 12) * 9, w /4, h /2))
    pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, (h / 12) * 9, w / 4, h / 2), int(h / 100))
    #디자인2
    pygame.draw.rect(screen, (255 - 100 * keys[0],255 - 100 * keys[0], 255 - 100 * keys[0]), (w / 2 - w / 9, (h / 24) * 19 + (h / 48) * keys[0], w / 27, h / 8), int(h / 150))
    pygame.draw.rect(screen, (255 - 100 * keys[3],255 - 100 * keys[3], 255 - 100 * keys[3]), (w / 2 + w / 13.5, (h / 24) * 19 + (h / 48) * keys[3], w / 27, h / 8), int(h / 150))
    #디자인3
    pygame.draw.circle(screen, (150, 150, 150), (w / 2, (h / 24) * 21), (w / 20), int(h / 200))
    pygame.draw.line(screen, (150, 150, 150), (w / 2 - math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 - math.cos(spin) * 25 * (w / 1600)), (w / 2 + math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 + math.cos(spin) * 25 * (w / 1600)), int(w / 400))
    spin = Time * -2
    #디자인4
    pygame.draw.rect(screen, (255 - 100 * keys[1], 255 - 100 * keys[1], 255 - 100 * keys[1]), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8))
    pygame.draw.rect(screen, (0,0, 0), (w / 2 - w / 18, (h / 48) * 43 + (h / 48) * (keys[1] * 1.2), w / 27, h / 64), int(h / 150))
    pygame.draw.rect(screen, (50,50, 50), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8), int(h / 150))
    #디자인5
    pygame.draw.rect(screen, (255 - 100 * keys[2], 255 - 100 * keys[2], 255 - 100 * keys[2]), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8))
    pygame.draw.rect(screen, (0, 0, 0), (w / 2 + w / 58, (h / 48) * 43 + (h / 48) * (keys[2] * 1.2), w / 27, h / 64), int(h / 150))
    pygame.draw.rect(screen, (50, 50, 50), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8), int(h / 150))
    #====================================================================================================================================================================================================================================================

    #프레임 제한
    clock.tick(maxframe)

    #판정 글씨
    miss_text.set_alpha(255 - (255 / 5) * miss_anim)
    screen.blit(combo_text, (w / 2 - combo_text.get_width() / 2, (h / 12.9) * 4 - combo_text.get_height() / 2))
    screen.blit(rate_text, (w / 2 - rate_text.get_width() / 2, (h / 12.9) * 8 - rate_text.get_height() / 2))
    screen.blit(miss_text, (w / 2 - miss_text.get_width() / 2, (h / 12.9) * 4 - miss_text.get_height() / 2))

    #화면송출
    pygame.display.flip()