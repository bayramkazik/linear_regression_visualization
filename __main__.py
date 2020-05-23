import pygame
from typing import Collection


def calc_lr_line_pos(point_data):
    x_list = []
    y_list = []

    for x, y in point_data:
        x_list.append(x)
        y_list.append(y)

    lr.fit(x_list, y_list)

    line_start = 0, lr.predict(0)
    line_end = WIDTH, lr.predict(WIDTH)

    return line_start, line_end


def average(l: Collection):
    return sum(l) / len(l) if l else 0


class LinearRegression:
    def __init__(self):
        self.is_fitted = False

        self.X: Collection = None  # y
        self.Y: Collection = None  # x
        self.avg_x: float = None  # y̅
        self.avg_y: float = None  # x̅
        self.slope: float = None  # m
        self.y_intercept: float = None  # b

    def fit(self, inputs, outputs):
        self.is_fitted = True

        self.X = inputs
        self.Y = outputs
        self.avg_x = average(self.X)
        self.avg_y = average(self.Y)
        self.slope = self._calc_slope()
        self.y_intercept = self._calc_y_intercept()

    def _calc_slope(self):
        if not self.is_fitted:
            return

        total_difference = 0
        total_x_difference_square = 0

        for x, y in zip(self.X, self.Y):
            x_difference = x - self.avg_x
            y_difference = y - self.avg_y

            total_difference += x_difference * y_difference
            total_x_difference_square += x_difference ** 2

        return total_difference / total_x_difference_square if total_x_difference_square else 0

    def _calc_y_intercept(self):
        if not self.is_fitted:
            return
        return self.avg_y - self.slope * self.avg_x

    def predict(self, input):
        if not self.is_fitted:
            return
        return self.slope * input + self.y_intercept


# CONSTS
WIDTH, HEIGHT = 600, 600
BACKGROUND = (20, 200, 70)
POINT_DEL_COOLDOWN_VALUE = 5

points = []

lr = LinearRegression()
lr_line_pos = None

pygame.font.init()
pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Linear Regression Visualization')

point_del_cooldown = POINT_DEL_COOLDOWN_VALUE

font = pygame.font.SysFont('Arial', 20)

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            points.append(pygame.mouse.get_pos())
            lr_line_pos = calc_lr_line_pos(points)
    
    if pygame.mouse.get_pressed()[2] and points and point_del_cooldown <= 0:
        points.pop()
        point_del_cooldown = POINT_DEL_COOLDOWN_VALUE
    
    if point_del_cooldown > 0:
        point_del_cooldown -= 1
    
    screen.fill(BACKGROUND)

    for point in points:
        pygame.draw.circle(screen, (255, 165, 0), point, 7)
        pygame.draw.circle(screen, (50, 50, 50), point, 7, 1)

    if lr_line_pos:
        pygame.draw.line(screen, (255, 0, 0), *lr_line_pos)

    if lr.is_fitted:
        formula_text = 'y = mx + b'
        textsurface = font.render(formula_text, True, (0, 0, 0))
        screen.blit(textsurface, (10, 0))
        
        m_text = f'm = {str(lr.slope)[:6]}'
        textsurface = font.render(m_text, True, (0, 0, 0))
        screen.blit(textsurface, (10, 30))
        
        b_text = f'b = {str(lr.y_intercept)[:6]}'
        textsurface = font.render(b_text, True, (0, 0, 0))
        screen.blit(textsurface, (10, 60))


    clock.tick(30)

    pygame.display.flip()
