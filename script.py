import mdl
from display import *
from matrix import *
from draw import *

ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for command in commands:
        print command

        temp = command[0];
        if temp == 'sphere':
            add_sphere(tmp,
                       float(command[1]), float(command[2]), float(command[3]),
                       float(command[4]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif temp == 'torus':
            add_torus(tmp,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif temp == 'box':
            add_box(tmp,
                    float(command[1]), float(command[2]), float(command[3]),
                    float(command[4]), float(command[5]), float(command[6]))
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []

        elif temp == 'circle':
            add_circle(tmp,
                       float(command[1]), float(command[2]), float(command[3]),
                       float(command[4]), step)
        elif temp == 'hermite' or temp == 'bezier':
            add_curve(tmp,
                      float(command[1]), float(command[2]),
                      float(command[3]), float(command[4]),
                      float(command[5]), float(command[6]),
                      float(command[7]), float(command[8]),
                      step, temp)
        elif temp == 'line':
            add_edge( tmp,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), float(command[6]) )

        elif temp == 'scale':
            t = make_scale(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif temp == 'move':
            t = make_translate(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif temp == 'rotate':
            theta = float(command[2]) * (math.pi / 180)
            if command[1] == 'x':
                t = make_rotX(theta)
            elif command[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif temp == 'clear':
            tmp = []
        elif temp == 'ident':
            ident(transform)
        elif temp == 'apply':
            matrix_mult( transform, tmp )
        elif temp == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        elif temp == 'pop':
            stack.pop()
        elif temp == 'display' or temp == 'save':
            if temp == 'display':
                display(screen)
            else:
                save_extension(screen, command[1])