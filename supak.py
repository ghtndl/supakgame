import pygame
import pymunk
import pymunk.pygame_util
import random
import os

# 파이게임 초기화
pygame.init()


# 게임 창 초기화 및 설정
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)  # 스코어 표시용 글꼴

# 배경 이미지 로드
def load_bg_image():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "/Users/ohuseel/Desktop/imgame", "bgimg.png")
    image = pygame.image.load(image_path)

    new_width = 1200
    new_height = 800
    image = pygame.transform.scale(image, (new_width, new_height))

    return image

background_image = load_bg_image()

# Pymunk의 공간(물리공간)을 설정
space = pymunk.Space()
space.gravity = (0, 900)

# 바닥과 벽을 추가
def add_walls_and_floor(space, width, height):
    # 바닥추가
    floor = pymunk.Segment(space.static_body, (0, height - 50), (width, height - 50), 1)
    floor.elasticity = 0.8
    floor.friction = 1
    space.add(floor)

    # 왼쪽벽 추가
    left_wall = pymunk.Segment(space.static_body, (0, 0), (0, height), 1)
    left_wall.elasticity = 0.8
    left_wall.friction = 1
    space.add(left_wall)

    # 오른쪽 벽 추가
    right_wall = pymunk.Segment(space.static_body, (width, 0), (width, height), 1)
    right_wall.elasticity = 0.8
    right_wall.friction = 1
    space.add(right_wall)

# 바닥과 벽 추가
add_walls_and_floor(space, width, height)

# draw_options 정의
draw_options = pymunk.pygame_util.DrawOptions(screen)

# 과일 클래스의 정의
class Fruit:
    def __init__(self, position, size, evolution, space):
        self.body = pymunk.Body(1, float('inf'))
        self.body.position = position
        radius = size / 2
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        self.evolution = evolution
        self.space = space
        self.space.add(self.body, self.shape)
    

fruit_images = {
    'image1': '/Users/ohuseel/Desktop/imgame/output/F1_result.jpeg_1.png',
    'image2': '/Users/ohuseel/Desktop/imgame/output/F2_result.jpeg_1.png',
    'image3': '/Users/ohuseel/Desktop/imgame/output/F3_result.jpeg_1.png',
    'image4': '/Users/ohuseel/Desktop/imgame/output/F4_result.jpeg_1.png',
    'image5': '/Users/ohuseel/Desktop/imgame/output/F5_result.jpeg_1.png',
    'image6': '/Users/ohuseel/Desktop/imgame/output/F6_result.jpeg_1.png',
    'image7': '/Users/ohuseel/Desktop/imgame/output/F7_result.jpeg_1.png',
    'image8': '/Users/ohuseel/Desktop/imgame/output/F8_result.jpeg_1.png',
    'image9': '/Users/ohuseel/Desktop/imgame/output/F9_result.jpeg_1.png',
    'image10': '/Users/ohuseel/Desktop/imgame/output/F10_result.jpeg_1.png',
}

fruit_positions = [(100, -30), (200, -30), (300, -30), (400, -30), (500, -30)]

# 과일크기사전

fruit_sizes = {
    'image1': 70,
    'image2': 85,
    'image3': 95,
    'image4': 105,
    'image5': 125,
    'image6': 140,
    'image7': 155,
    'image8': 170,
    'image9': 185,
    'image10': 200
}


# 과일 진화 규칙
evolution_rules = {
    'image1': ('image2', 1),
    'image2': ('image3', 3),
    'image3': ('image4', 6),
    'image4': ('image5', 10),
    'image5': ('image6', 15),
    'image6': ('image7', 21),
    'image7': ('image8', 28),
    'image8': ('image9', 36),
    'image9': ('image10', 45),
    'image10': (None, 55)  # 수박은 진화안됨
}

# 점수변수
score = 0

# 과일 생성 함수(클릭으로 생성되는 과일)
def generate_fruit(space, mouse_position, fruit_name):
    # 사용자가 클릭한 위치를 기반으로 과일 생성
    # x좌표를 0에서 730 사이의 값으로 제한
    x = max(0, min(mouse_position[0], 730))
    fruit = Fruit((x, mouse_position[1]), fruit_sizes[fruit_name], fruit_name, space)
    return fruit

# 충돌 콜백 함수 업데이트
def collision_handler(arbiter, space, data):
    global score, fruits
    fruit_shape1, fruit_shape2 = arbiter.shapes
    fruit1, fruit2 = fruit_shape1.body, fruit_shape2.body

    # Identify the Fruit instances from the shapes.
    fruit1_instance = next((f for f in fruits if f.body == fruit1), None)
    fruit2_instance = next((f for f in fruits if f.body == fruit2), None)

    # Check if both are fruits and have the same evolution state.
    if fruit1_instance and fruit2_instance and fruit1_instance.evolution == fruit2_instance.evolution:
        # Get the slower fruit.
        slower_fruit = fruit1_instance if fruit1.velocity.length < fruit2.velocity.length else fruit2_instance
        faster_fruit = fruit2_instance if slower_fruit == fruit1_instance else fruit1_instance

        # Evolve the slower fruit.
        next_evolution, points = evolution_rules[slower_fruit.evolution]
        if next_evolution:
            # Update the score.
            score += points
            # Create a new fruit with the next evolution.
            new_fruit = Fruit(slower_fruit.body.position, fruit_sizes[next_evolution], next_evolution, space)
            new_fruit.body.velocity = slower_fruit.body.velocity  # Maintain the velocity after evolution.
            fruits.append(new_fruit)
            # Remove the old fruits.
            space.remove(fruit_shape1, fruit1)
            space.remove(fruit_shape2, fruit2)
            fruits.remove(fruit1_instance)
            fruits.remove(fruit2_instance)

            # Apply a small random impulse to the new fruit to avoid stacking
            impulse_x = random.uniform(-1, 1) * 100  # Randomize the direction
            impulse_y = -80  # Apply a small upward force
            new_fruit.body.apply_impulse_at_local_point((impulse_x, impulse_y))

            # If fruits are stacked, apply a stronger horizontal impulse
            if abs(fruit1.position.y - fruit2.position.y) < (fruit1_instance.shape.radius + fruit2_instance.shape.radius):
                direction = 1 if fruit1.position.x > width / 2 else -1
                horizontal_impulse = direction * 200  # Apply a stronger impulse to move fruits apart
                new_fruit.body.apply_impulse_at_local_point((horizontal_impulse, 0))

    # Check and correct the position of fruits
    for fruit in fruits:
        fruit_x = max(0, min(fruit.body.position.x, 730))
        fruit.body.position = (fruit_x, fruit.body.position.y)

    return True

# 충돌핸들러 설정
handler = space.add_default_collision_handler()
handler.begin = collision_handler

# 과일 생성
fruits = []

# 이미지를 화면에 표시하는 함수 추가
def draw_fruit(screen, fruit):
    fruit_image = pygame.image.load(fruit_images[fruit.evolution])
    fruit_image = pygame.transform.scale(fruit_image,(fruit_sizes[fruit.evolution],fruit_sizes[fruit.evolution]))
    fruit_rect = fruit_image.get_rect(center=(int(fruit.body.position.x), int(fruit.body.position.y)))
    screen.blit(fruit_image, fruit_rect)

# 다음 과일을 표시하는 함수 수정
def show_score_and_next_fruit(screen, font, score, next_fruit_name, next_fruit_size):
    # 스코어 텍스트를 중앙에서 오른쪽으로 약간 이동하여 표시
    score_text = font.render(f'{score}', True, (255, 255, 204))
    score_text_pos_x = (width // 2) + 350  # 화면 폭의 절반에서 오른쪽으로 100 픽셀 이동
    score_text_pos_y = 355  # 상단에서 10 픽셀 위치
    screen.blit(score_text, (score_text_pos_x, score_text_pos_y))

    # 다음 과일 이미지를 텍스트 아래에 표시
    next_fruit_image = pygame.image.load(fruit_images[next_fruit_name])
    next_fruit_image = pygame.transform.scale(next_fruit_image, (next_fruit_size * 1, next_fruit_size * 1))
    next_fruit_image_pos_x = score_text_pos_x + score_text.get_width() + 5
    next_fruit_image_pos_y = score_text_pos_y + score_text.get_height() - 250  # 다음 과일 텍스트 아래
    screen.blit(next_fruit_image, (next_fruit_image_pos_x, next_fruit_image_pos_y))


game_over = False
game_over_text = font.render('Game Over!', True, (255,0,0))




####################
# 게임 메인루프 돌리기  #
###################
running = True
# 다음 과일 선택
next_fruit_name = random.choice(list(fruit_images.keys())[0:5])  # 이미지의 이름으로 랜덤 선택
next_fruit_size = fruit_sizes[next_fruit_name]

start_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
FPS = 60




running = True
while running and not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if mouse_position[1] < height // 9:
                mouse_position = pygame.mouse.get_pos()
                fruit = generate_fruit(space, mouse_position, next_fruit_name)
                fruits.append(fruit)

                next_fruit_name = random.choice(list(fruit_images.keys())[0:5])
                next_fruit_size = fruit_sizes[next_fruit_name]

    # 물리 연산 진행
    space.step(1/60)

    # 배경 이미지 그리기
    screen.blit(background_image, (0, 0))

    # 배경 이미지 그리기 (물체들보다 먼저 그리기)
    screen.blit(background_image, (0, 0))

  # 과일과 물리적 공간을 그리는 그림
   


    # 과일 & 물리 공간 그리기

    for fruit in fruits:
        if 0 < fruit.body.position.y < height - 50:  # 화면 내에 있는 경우에만 그립니다
            draw_fruit(screen,fruit)

    # 스코어와 다음 과일을 화면에 표시합니다
    show_score_and_next_fruit(screen, font, score, next_fruit_name, next_fruit_size)

    line_over_fruit = [fruit for fruit in fruits if fruit.body.position.y < height // 9]
    if len(line_over_fruit) >=7:    
        game_over = True
    
    if game_over:
        screen.blit(game_over_text, (width // 2 - 100, height // 2))
        score_text = font.render(f'Final Score: {score}', True, (0, 0, 0))
        score_text_pos_x = (width // 2) - 100
        score_text_pos_y = (height // 2) + 50
        screen.blit(score_text, (score_text_pos_x, score_text_pos_y))


    # 화면갱신
    pygame.display.flip()
    clock.tick(60)

    # Pygame 종료
#pygame.quit()


# 게임 종료 텍스트와 스코어 표시
if game_over:
    screen.blit(game_over_text, (width // 2 - 100, height // 2))
    score_text = font.render(f'Final Score: {score}', True, (0, 0, 0))
    score_text_pos_x = (width // 2) - 100
    score_text_pos_y = (height // 2) + 50
    screen.blit(score_text, (score_text_pos_x, score_text_pos_y))
    pygame.image.save(screen, '/Users/ohuseel/Desktop/imgame/gameover.png')



# 화면 갱신
pygame.display.flip()

# 게임 루프를 종료하지 않도록 설정
# running = False

# FPS 설정
clock.tick(60)

# 이 부분이 없으면 창이 닫히지 않습니다.
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

        
