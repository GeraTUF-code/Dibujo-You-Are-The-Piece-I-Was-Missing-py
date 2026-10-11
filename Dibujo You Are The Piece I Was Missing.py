import pygame
import cv2
import numpy as np
import random
import math


pygame.init()
W, H = 700, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("coded.by.adri | Love in Code")
clock = pygame.time.Clock()

BG = (8, 5, 15)
FPS = 60
random.seed(42)

COLORS = [
    (255, 165, 205),
    (205, 165, 255),
    (145, 210, 255),
    (255, 215, 175),
    (255, 190, 225)
]

IMAGE_PATH = "puzzle.jpg"
img = cv2.imread(IMAGE_PATH)

if img is None:
    raise FileNotFoundError(f"Imagen '{IMAGE_PATH}' no encontrada. Colócala en la misma carpeta.")

ih, iw = img.shape[:2]
oy = 100
scale = min((W - 60) / iw, (H - oy - 20) / ih)
nw, nh = int(iw * scale), int(ih * scale)
img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)

gray_raw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray_raw, (3, 3), 0)
edges = cv2.Canny(gray, 40, 120)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
color_mask = (hsv[..., 2] > 80) & (gray_raw > 40)

img_x = (W - nw) // 2
img_y = oy

points = []

y_indices, x_indices = np.where(edges > 0)
for y, x in zip(y_indices[::2], x_indices[::2]):
    target_x = img_x + x
    target_y = img_y + y
    start_x = random.randint(0, W)
    start_y = random.randint(0, H)
    color = random.choice(COLORS)
    points.append({
        'sx': start_x, 'sy': start_y,
        'tx': target_x, 'ty': target_y,
        'x': start_x, 'y': start_y,
        'color': color
    })

y_indices, x_indices = np.where(color_mask)
for y, x in zip(y_indices, x_indices):
    if x % 8 == 0 and y % 8 == 0:
        target_x = img_x + x
        target_y = img_y + y
        start_x = random.randint(0, W)
        start_y = random.randint(0, H)
        color = random.choice(COLORS)
        points.append({
            'sx': start_x, 'sy': start_y,
            'tx': target_x, 'ty': target_y,
            'x': start_x, 'y': start_y,
            'color': color
        })

for _ in range(200):
    target_x = random.randint(img_x, img_x + nw)
    target_y = random.randint(img_y, img_y + nh)
    start_x = random.randint(0, W)
    start_y = random.randint(0, H)
    color = (140, 140, 170)
    points.append({
        'sx': start_x, 'sy': start_y,
        'tx': target_x, 'ty': target_y,
        'x': start_x, 'y': start_y,
        'color': color
    })

try:
    font = pygame.font.SysFont("Segoe UI", 22)
except:
    font = pygame.font.Font(None, 24)

progress = 0.0
anim_speed = 0.025 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG)

    if progress < 1.0:
        progress += anim_speed
        if progress > 1.0:
            progress = 1.0

    for p in points:
        p['x'] = p['sx'] + (p['tx'] - p['sx']) * progress
        p['y'] = p['sy'] + (p['ty'] - p['sy']) * progress
        pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 1)

    if progress > 0.5:
        alpha_progress = min(255, int((progress - 0.5) / 0.4 * 255))
        title_text = font.render("You Are The Piece I Was Missing.", True, (200, 200, 225))
        title_text.set_alpha(alpha_progress)
        screen.blit(title_text, (W // 2 - title_text.get_width() // 2, 35))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()





