import pygame
import sys
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from pygame.locals import *

from threading import Thread
from tkinter import *
from tkinter import filedialog
from numpy import *
def datawindow():
    root= Tk()
    root.title('Rotate Testerv0.1')
    root.geometry('252x352')

    def selectx():
        global xa
        xtext = "X:" + str(vx.get())
        labelx.config(text = xtext)
        xa = float(vx.get())/100
    vx = DoubleVar()
    scale = Scale(root, variable = vx, from_ = -100, to = 100, orient = HORIZONTAL)
    scale.pack(anchor=CENTER)
    btnx = Button(root, text="X", command=selectx)
    btnx.pack(anchor=CENTER)
    labelx = Label(root)
    labelx.pack()

    def selecty():
        global ya
        ytext = "Y:" + str(vy.get())
        labely.config(text = ytext)
        ya = float(vy.get())/100
    vy = DoubleVar()
    scale = Scale(root, variable = vy, from_ = -100, to = 100, orient = HORIZONTAL)
    scale.pack(anchor=CENTER)
    btny = Button(root, text="Y", command=selecty)
    btny.pack(anchor=CENTER)
    labely = Label(root)
    labely.pack()

    def selectz():
        global za
        ztext = "X:" + str(vz.get())
        labelz.config(text = ztext)
        za = float(vz.get())/100
    vz = DoubleVar()
    scale = Scale(root, variable = vz, from_ = -100, to = 100, orient = HORIZONTAL)
    scale.pack(anchor=CENTER)
    btnz = Button(root, text="Z", command=selectz)
    btnz.pack(anchor=CENTER)
    labelz = Label(root)
    labelz.pack()

    def get_name():
        global matrix_name
        matrix_name = nameinput.get()
    def save_matrices():
        global go_to_save
        get_name()
        go_to_save = True

    def load_matrices():
        global go_to_load
        go_to_load = True

    nametext = Label(root,text='Input Save Name')
    nametext.pack()
    NAME=StringVar()
    nameinput = Entry(root,width=16,textvariable=NAME)
    nameinput.pack()
    s = Button(root, text='save matrix', command=save_matrices)
    s.pack()
    s = Button(root, text='load matrix', command=load_matrices)
    s.pack()

    root.mainloop()

def getFileContent(file):
    content = open(file, 'r').read()
    return content

def init():
    vertices = [-1, -1,
                -1, 1,
                1, 1,
                1, -1]
    texcoords = [0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0]
    pygame.init()
    screen_size = (1080, 720)
    window_title = "pyopengl rotate test"
    pygame.display.set_mode(screen_size, HWSURFACE | OPENGL | DOUBLEBUF)
    pygame.display.set_caption(window_title)

    glViewport(0, 0, screen_size[0], screen_size[1])

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    img = pygame.image.load("images/image.png")
    img_rect = img.get_rect(center = (screen_size[0]/2, screen_size[1]/2))
    screen = pygame.Surface(screen_size)
    screen.blit(img, img_rect)
    textureData = pygame.image.tostring(screen, "RGB", True)
    width = screen.get_width()
    height = screen.get_height()

    texID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    vertexShader = compileShader(getFileContent("shaders/sprite_vert.glsl"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContent("shaders/sprite_frag.glsl"), GL_FRAGMENT_SHADER)

    global shaderProgram
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)
    glLinkProgram(shaderProgram)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, vertices)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, texcoords)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    global texLocation
    texLocation = glGetUniformLocation(shaderProgram, "textureObj")
    glUseProgram(shaderProgram)
    glUniform1i(texLocation, 0)
    
def clear(color=(0, 0, 0)):
    pygame.display.flip()
    glClearColor(color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 255 if len(color) > 3 else 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def render():
    glDrawArrays(GL_QUADS, 0, 4)

def rotatewindow():
    init()
    # variables
    clock = pygame.time.Clock()
    fps = 240
    global move,angle,xa,ya,za
    move_z = False
    move_xz = False
    angle = 0

    test = False
    flip_twice = False
    flip_time = 0
    flip_direction = 1

    global go_to_save, go_to_load
    go_to_save = False
    go_to_load = False
    spd_collect = 0
    angle_spd = 1
    flip_spd = 10
    quick_save = False
    has_save = False
    global save_matrix
    correct_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    save_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

    def save_matrix_file():
        global matrix_name
        save_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        print(save_matrix)
        if matrix_name:
            save('matrices/' + matrix_name + '.npy', save_matrix)

    def load_matrix_file():
        save_path = filedialog.askopenfilename()
        if save_path:
            save_matrix = load(save_path)
            glLoadMatrixf(save_matrix)

    while True:
        clock.tick(fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    move = not(move)
                elif e.key == pygame.K_q:
                    spd_collect = 0
                    move_z = not(move_z)
                elif e.key == pygame.K_e:
                    spd_collect = 0
                    move_xz = not(move_xz)
                elif e.key == pygame.K_t:
                    spd_collect = 0
                    test = not(test)
                elif e.key == pygame.K_r:
                    spd_collect = 0
                    flip_time = 0
                    flip_direction = 1
                    flip_twice = not(flip_twice)

                elif e.key == pygame.K_w:
                    glRotatef(flip_spd, 1, 0, 0)
                elif e.key == pygame.K_s:
                    glRotatef(flip_spd, -1, 0, 0)
                elif e.key == pygame.K_a:
                    glRotatef(flip_spd, 0, 1, 0)
                elif e.key == pygame.K_d:
                    glRotatef(flip_spd, 0, -1, 0)
                elif e.key == pygame.K_z:
                    glRotatef(flip_spd, 0, 0, 1)
                elif e.key == pygame.K_x:
                    glRotatef(flip_spd, 0, 0, -1)

                
                elif e.key == pygame.K_0:
                    if not(quick_save):
                        glPushMatrix()
                        quick_save = True
                elif e.key == pygame.K_9:
                    if quick_save:
                        glPopMatrix()
                        quick_save = False
                elif e.key == pygame.K_2:
                    if not(has_save):
                        save_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
                        has_save = True
                elif e.key == pygame.K_3:
                    if has_save:
                        glLoadMatrixf(save_matrix)
                        has_save = False
                elif e.key == pygame.K_1:
                    glLoadMatrixf(correct_matrix)

        if go_to_save:
            go_to_save = False
            save_matrix_file()
        elif go_to_load:
            go_to_load = False
            load_matrix_file()
        if move:
            spd_collect += angle_spd
            glRotatef(angle_spd, xa, ya, za)
            if spd_collect >= 360:
                spd_collect = 0
                move = False
        if move_z:
            spd_collect += angle_spd
            glRotatef(angle_spd, 0, 0, 1)
            if spd_collect >= 360:
                spd_collect = 0
                move_z = False
        if move_xz:
            spd_collect += angle_spd
            glRotatef(angle_spd, 1, 0, 1)
            if spd_collect >= 360:
                spd_collect = 0
                move_xz = False
        if test:
            spd_collect += angle_spd
            glRotatef(angle_spd, 0.15, 0.5, 0.02)
            if spd_collect >= 360:
                spd_collect = 0
                test = False

        if flip_twice:
            spd_collect += angle_spd
            glRotatef(angle_spd, 1*flip_direction, 0, 1*flip_direction)
            if spd_collect >= 360:
                flip_direction *= -1
                flip_time+=1
                spd_collect = 0
                if flip_time >=2:
                    flip_twice = False
        glRotatef(angle, 0, 0, 0.5)
        glDrawArrays(GL_QUADS, 0, 4)
        render()
        clear()

if __name__ == '__main__':
    move = False
    angle = 0
    xa=ya=za=0.0
    
    thread1 = Thread(target=datawindow)
    thread1.setDaemon(True)
    thread1.start()
    rotatewindow()