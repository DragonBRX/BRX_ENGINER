import sys
import math
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Vector3:
    """Classe para representar vetores 3D e operações básicas."""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        l = self.length()
        if l > 0:
            return Vector3(self.x / l, self.y / l, self.z / l)
        return Vector3()

class Node:
    """Classe base para todos os objetos na árvore de cena."""
    def __init__(self, name="Node"):
        self.name = name
        self.parent = None
        self.children = []
        self.position = Vector3()
        self.rotation = Vector3()
        self.scale = Vector3(1.0, 1.0, 1.0)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def update(self, delta_time):
        for child in self.children:
            child.update(delta_time)

    def render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation.x, 1, 0, 0)
        glRotatef(self.rotation.y, 0, 1, 0)
        glRotatef(self.rotation.z, 0, 0, 1)
        glScalef(self.scale.x, self.scale.y, self.scale.z)
        
        self._on_render()
        
        for child in self.children:
            child.render()
        glPopMatrix()

    def _on_render(self):
        pass

class SpatialNode(Node):
    """Nó para objetos com transformações 3D."""
    def __init__(self, name="Spatial"):
        super().__init__(name)

class Camera(SpatialNode):
    """Câmera para visualização 3D."""
    def __init__(self, name="Camera"):
        super().__init__(name)
        self.fov = 45.0
        self.aspect = 800 / 600
        self.near = 0.1
        self.far = 100.0

    def apply(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.aspect, self.near, self.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # A câmera em OpenGL é o inverso da transformação do objeto
        glRotatef(-self.rotation.x, 1, 0, 0)
        glRotatef(-self.rotation.y, 0, 1, 0)
        glRotatef(-self.rotation.z, 0, 0, 1)
        glTranslatef(-self.position.x, -self.position.y, -self.position.z)

class Cube(SpatialNode):
    """Um simples cubo 3D para teste."""
    def _on_render(self):
        glBegin(GL_QUADS)
        # Frente
        glColor3f(1, 0, 0)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Trás
        glColor3f(0, 1, 0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        # Cima
        glColor3f(0, 0, 1)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        # Baixo
        glColor3f(1, 1, 0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        # Direita
        glColor3f(1, 0, 1)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        # Esquerda
        glColor3f(0, 1, 1)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glEnd()

class BRXEngine:
    """Classe principal da BRX Engine."""
    def __init__(self, width=800, height=600, title="BRX Engine"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)
        
        glEnable(GL_DEPTH_TEST)
        
        self.root = Node("Root")
        self.camera = Camera("MainCamera")
        self.camera.position.z = 5.0
        self.root.add_child(self.camera)
        
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Input básico para mover a câmera (WASD + QE para cima/baixo)
            keys = pygame.key.get_pressed()
            speed = 5.0 * delta_time
            if keys[K_w]: self.camera.position.z -= speed
            if keys[K_s]: self.camera.position.z += speed
            if keys[K_a]: self.camera.position.x -= speed
            if keys[K_d]: self.camera.position.x += speed
            if keys[K_q]: self.camera.position.y += speed
            if keys[K_e]: self.camera.position.y -= speed
            
            # Rotação da câmera com setas
            rot_speed = 50.0 * delta_time
            if keys[K_LEFT]: self.camera.rotation.y -= rot_speed
            if keys[K_RIGHT]: self.camera.rotation.y += rot_speed
            if keys[K_UP]: self.camera.rotation.x -= rot_speed
            if keys[K_DOWN]: self.camera.rotation.x += rot_speed

            self.root.update(delta_time)
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.camera.apply()
            self.root.render()
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    engine = BRXEngine()
    
    # Adicionar alguns cubos para testar a perspectiva 3D
    cube1 = Cube("Cube1")
    cube1.position.x = -1.5
    engine.root.add_child(cube1)
    
    cube2 = Cube("Cube2")
    cube2.position.x = 1.5
    cube2.rotation.y = 45
    engine.root.add_child(cube2)
    
    cube3 = Cube("Cube3")
    cube3.position.y = 2.0
    cube3.scale = Vector3(0.5, 0.5, 0.5)
    engine.root.add_child(cube3)
    
    print("Iniciando BRX Engine...")
    print("Controles:")
    print("  WASD: Mover Câmera (Frente, Trás, Esquerda, Direita)")
    print("  QE: Mover Câmera (Cima, Baixo)")
    print("  Setas: Rotacionar Câmera")
    engine.run()
