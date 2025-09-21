import sys
sys.dont_write_bytecode = True
import pygame
import cmath
import slider
pygame.init()
screen = pygame.display.set_mode((1610, 800))
pygame.display.set_caption('Fourier drawing')
running = True
black = (0,0,0)
white = (255,255,255)
import load_svg


def lerp(a, b, t, t_min=0, t_max=100):
    return int(a + (b - a) * (t - t_min) / (t_max - t_min))

def add_tuple(tuple1, tuple2):
    return tuple(map(lambda x, y: x + y, tuple1, tuple2))

def coordinate(x,y, mode="normal"):
    if mode == "normal":
        return (1210+x, 400-y)
    elif mode == "draw":
        return ((x-400), (400-y))


def DFS(k, N, points):
    output = 0+0j
    for n in range(N):
        output += points[n]*cmath.exp((-2j*cmath.pi*k*n)/N)
    output /= N
    return output

class Vector:
    def __init__(self, coefficient, index, N):
        self.polar = cmath.polar(coefficient)
        self.current = self.polar
        self.speed = (2*cmath.pi*index)/N
    def update(self, t):
        self.current = (self.polar[0], self.polar[1] + self.speed*t)

def draw_vector(screen, base, vector):
    modulus, angle = vector.current
    rect = cmath.rect(modulus, angle)
    tip = add_tuple(base,(rect.real, rect.imag))
    pygame.draw.line(screen, white, coordinate(*base), coordinate(*tip), 2)
    pygame.draw.circle(screen, (0,0,255), coordinate(*base), int(abs(modulus)/2), 1)
    return tip

def compute_fourier(points):
    coefficients = []
    N = len(points)
    for k in range(N):
        coefficients.append(DFS(k, N, points))
    vectors = []
    for k in range(N):
        vectors.append(Vector(coefficients[k], k, N))
    return coefficients, vectors


clock = pygame.time.Clock()
t = 0
path = []
pen = False
drawing = []
coefficients = []
vectors = []
full_vectors = []
speed_slider = slider.Slider(835, 750, 350, 20, 10, 500, 60)
resolution_slider = slider.Slider(1235, 750, 350, 20, 1, 100, 100, percent=True)
resolution = 100
update_vectors = False
draw_colour = (0,255,0)

mode = "draw"
#mode = "plot"
#points = [complex(i[0], -i[1]) for i in load_svg.load_svg("svg/humberger-svgrepo-com.svg")]
#points = [complex(i[0], -i[1]) for i in load_svg.load_svg("svg/svg-svgrepo-com.svg", density=0.1, scale=0.5, offset=(-100,-100))]
#points = [complex(i[0], -i[1]) for i in load_svg.load_svg("svg/clash-mini-svgrepo-com.svg", density=1, scale=5)]
#coefficients, full_vectors = compute_fourier(points)
#vectors = full_vectors


while running:
    screen.fill(black)
    pygame.draw.line(screen, white, (805,0), (805,800), 10)
    speed_slider.draw(screen)
    resolution_slider.draw(screen)

    if mode == "plot":
        base = (0,0)
        if update_vectors:
            draw_colour = (
                lerp(255, 0, resolution),
                lerp(0, 255, resolution),
                0)
            vectors = sorted(full_vectors, key=lambda v: abs(v.polar[0]), 
                                     reverse=True)[:int(len(full_vectors)*resolution/100)]
            path = []
            update_vectors = False
        for vector in vectors:
            vector.update(t)
            base = draw_vector(screen, base, vector)

        path.append(coordinate(*base))
        if len(path) > 2:
            pygame.draw.lines(screen, draw_colour, False, path, 1)
        
        t += 1

    elif mode == "draw" and pen:
        drawing.append(pygame.mouse.get_pos())
    if len(drawing) > 2:
        pygame.draw.lines(screen, white, False, drawing, 1)

    for event in pygame.event.get():
        speed_slider.handle_event(event)
        resolution_slider.handle_event(event)
        if resolution_slider.value != resolution:
            resolution = resolution_slider.value
            update_vectors = True
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            exit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not pen and pygame.mouse.get_pos()[0] <= 800:
                    mode = "draw"
                    pen = True
                    drawing = []
                    coefficients = []
                    full_vectors = []
                    vectors = []
                    path = []
                elif pygame.mouse.get_pos()[0] <= 800:
                    pen = False
                    mode = "plot"
                    points = [complex(*(coordinate(*i, mode="draw"))) for i in drawing]
                    coefficients, full_vectors = compute_fourier(points)
                    vectors = sorted(full_vectors, key=lambda v: abs(v.polar[0]), 
                                     reverse=True)[:int(len(full_vectors)*resolution/100)]

    pygame.display.update()
    clock.tick(speed_slider.value)

    
