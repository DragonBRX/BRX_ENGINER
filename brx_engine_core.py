import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Vector3:
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

    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def normalize(self):
        l = self.length()
        if l > 0:
            return Vector3(self.x / l, self.y / l, self.z / l)
        return Vector3()

class BRXNode:
    """Classe base para todos os objetos na árvore de cena."""
    def __init__(self, name="BRXNode"):
        self.name = name
        self.parent = None
        self.children = []
        self.position = Vector3()
        self.rotation = Vector3()
        self.scale = Vector3(1.0, 1.0, 1.0)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

    def _update(self, delta_time):
        pass

    def _on_render(self):
        pass

class BRXSpatialNode(BRXNode):
    """Nó para objetos com transformações 3D."""
    def __init__(self, name="BRXSpatial"):
        super().__init__(name)

    def _on_render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation.x, 1, 0, 0)
        glRotatef(self.rotation.y, 0, 1, 0)
        glRotatef(self.rotation.z, 0, 0, 1)
        glScalef(self.scale.x, self.scale.y, self.scale.z)
        super()._on_render()
        for child in self.children:
            child._on_render()
        glPopMatrix()

class BRXCamera(BRXSpatialNode):
    """Câmera para visualização 3D."""
    def __init__(self, name="BRXCamera"):
        super().__init__(name)
        self.fov = 45.0
        self.aspect = 800 / 600  # Será atualizado no loop principal
        self.near = 0.1
        self.far = 100.0

    def _on_render(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.aspect, self.near, self.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(-self.rotation.x, 1, 0, 0)
        glRotatef(-self.rotation.y, 0, 1, 0)
        glRotatef(-self.rotation.z, 0, 0, 1)
        glTranslatef(-self.position.x, -self.position.y, -self.position.z)

class BRXCube(BRXSpatialNode):
    """Um simples cubo 3D para teste."""
    def _on_render(self):
        glBegin(GL_QUADS)
        # Frente
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        # Trás
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        # Cima
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        # Baixo
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        # Direita
        glColor3f(0.0, 1.0, 1.0)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)
        # Esquerda
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glEnd()

class BRXOrchestrator:
    """Classe principal da BRX Engine."""
    def __init__(self, width=800, height=600, title="BRX Engine"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)
        
        glEnable(GL_DEPTH_TEST)
        
        self.root = BRXNode("Root")
        self.camera = BRXCamera("MainCamera")
        self.camera.position.z = 5.0
        self.root.add_child(self.camera)
        
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

            # Lógica de atualização (ex: mover câmera, objetos)
            # self.root._update(delta_time)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            self.camera._on_render() # Configura a visão da câmera
            
            # Renderiza a cena a partir do nó raiz
            for child in self.root.children:
                child._on_render()

            pygame.display.flip()
            pygame.time.wait(10)
        
        pygame.quit()

if __name__ == "__main__":
    engine = BRXOrchestrator()
    
    # Adicionar alguns cubos para testar a perspectiva 3D
    cube1 = BRXCube("Cube1")
    cube1.position.x = -1.5
    engine.root.add_child(cube1)
    
    cube2 = BRXCube("Cube2")
    cube2.position.x = 1.5
    cube2.rotation.y = 45
    engine.root.add_child(cube2)
    
    cube3 = BRXCube("Cube3")
    cube3.position.y = 2.0
    cube3.scale = Vector3(0.5, 0.5, 0.5)
    engine.root.add_child(cube3)
    
    engine.run()
