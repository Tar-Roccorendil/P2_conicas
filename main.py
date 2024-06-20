import pygame
import pygame.locals
import math

def mat_mult(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    m, n, p = len(A), len(B), len(B[0])
    C = [[None for _ in range(p)] for _ in A]
    for i in range(m):
        for j in range(p):
            C[i][j] = sum(A[i][k]*B[k][j] for k in range(n))
    return C

def dot(v: tuple[float], u: tuple[float]) -> float:
    return sum(a*b for a,b in zip(v,u))

def qr_gram_schmidt(A: list[list[float]]) -> tuple[list[list[float]],list[list[float]]]:
    # n = len(A)
    # Q = [[0 for _ in A] for _ in A]
    # R = [[0 for _ in A] for _ in A]
    # R[0][0] = sqrt(dot(A[0],A[0]))
    # Q[0] = [a/R[0][0] for a in A[0]]
    
    # for k in range(1,n):
    #     R[k]


    pass

def qr_reflect():
    pass

def determinant(matrix: list[list[float]]) -> float:
    Q, R = qr_reflect(matrix)

    return math.prod(R[i][i] for i in range(len(R)))
    

def conic_coefficients(Points:list[tuple[int, int]]) -> list[int]:
    '''
    Gets a list of 5 2-tuples and outputs the coefficients of the terms
    Output in the order [x^2, xy, y^2, x, y, 1]
    '''
    matrix = [
        [p[0]**2 for p in Points],
        [p[0]*p[1] for p in Points],
        [p[1]**2 for p in Points],
        [p[0] for p in Points],
        [p[1] for p in Points],
        [1 for p in Points]
    ]

    coefficients = [determinant(matrix[:i]+matrix[i+1:]) * (-1)**i for i in range(matrix)]

    return coefficients

def conic_value(x: int, y: int,c: list[int]) -> int:
    return c[0] * x*x + c[1] * x*y + c[2] * y*y + c[3] * x + c[4] * y + c[5]

def test_value(x: int, y: int,points: list[tuple[int,int]]) -> float:
    return min((x-p[0])**2 + (y-p[1])**2 for p in points)


def draw_graph(surface: pygame.Surface,values: list[list[float]]) -> None:
    white = max((max(row,key=abs) for row in values))
    
    for y, row in enumerate(values):
        for x, color in enumerate(row):
            c = int(255*(color/white))
            surface.set_at((x,y), pygame.Color(c,c,c))

def draw_points(surface: pygame.Surface, points: list[tuple[int,int]]) -> None:
    for p in points:
        if p: 
            pygame.draw.circle(surface,0xcc3333,p,5)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((512,512))
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

    
    mouse_pressed:list[tuple[int,int]] = [None]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    running = False
                # if event.key == pygame.locals.K_f:
                #     pygame.display.toggle_fullscreen()
            elif event.type == pygame.locals.QUIT:
                running = False
            elif event.type == pygame.constants.MOUSEBUTTONDOWN:
                # screen.fill(0xdddddd)
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]

                new_point = (mouse_x, mouse_y)
                mouse_pressed.append(new_point)
                if len(mouse_pressed) == 6:
                    mouse_pressed.remove(mouse_pressed[0])

                    # conic_matrix = [[conic_value(x,y,conic_coefficients(mouse_pressed)) for x in screen.get_width] for y in screen.get_height()]
                    graph_matrix = [[test_value(x,y,mouse_pressed) for x in range(screen.get_width())] for y in range(screen.get_height())]
                    draw_graph(screen,graph_matrix)
                draw_points(screen,mouse_pressed)
                
                pygame.display.flip()

    
    pygame.quit()