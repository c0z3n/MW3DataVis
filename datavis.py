
#=================================================================#
#  datavis.py - by c0z3n                                          #
#                                                                 #
#  a simple 3d viewer for MW3 killdata in .kdt pickle files.      #
#  click a point to view associated points (recorded kill paths)  #
#  point color tone varies by elevation, lower = darker.          #
#  use keys 'a', 's', 'q', 'w', 'z', and 'x' to rotate view       #
#  on each axis, and the arrow keys to translate the model.       #
#                                                                 #
#  requires pygame (www.pygame.org)                               #
#                                                                 #
#=================================================================#

import sys, math, pygame
import os.path
import cPickle as pickle
from collections import defaultdict
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_s, K_q, K_w, K_z, K_x
from killnode import KillNode

class Scene:
    def __init__(self, win_width = 640, win_height = 480):
        self.width = win_width
        self.height = win_height
        self.lastMouseStateLeft = False
        self.lastMouseStateRight = False
        self.lastMousePosX = 0
        self.lastMousePosY = 0
        self.zoom = 2000
        self.fov = 285
        self.killdata_table = defaultdict(list)
        self.pointradius = 0
        self.nodes = []
        self.angle_X, self.angle_Y, self.angle_Z = 180, 0, -90
        self.valid_filename = False
        self.trans_X = 0
        self.trans_Y = 0
        
    def setup_map(self):
        valid_filename = False
        while not valid_filename:
            self.filename = raw_input("Map Name:")
            self.filename = "data\\" + self.filename + ".kdt"
            if os.path.isfile(r"%s" %self.filename):
                valid_filename = True
                
        self.killdata_table = pickle.load(open(self.filename, "rb"))
        for point in self.killdata_table:
            temp_list = []
            for tp in self.killdata_table[point]:
                temp_list.append(KillNode(self, 0-tp[0], tp[1], tp[2]))#x gets flipped
            self.nodes.append(KillNode(self, 0-point[0], point[1], point[2], list(temp_list)))
            
        self.min_X = self.nodes[0].x
        self.max_X = self.nodes[0].x
        self.min_Y = self.nodes[0].y
        self.max_Y = self.nodes[0].y
        self.min_Z = self.nodes[0].z
        self.max_Z = self.nodes[0].z
        for p in self.nodes:
        #find the min and max X values
            if p.x > self.max_X: self.max_X = p.x
            if p.x < self.min_X: self.min_X = p.x
        #find the min and max Y values
            if p.y > self.max_Y: self.max_Y = p.y
            if p.y < self.min_Y: self.min_Y = p.y
        #find the min and max Z values
            if p.z > self.max_Z: self.max_Z = p.z
            if p.z < self.min_Z: self.min_Z = p.z
        #find the difference between the max and min on each axis for centering
        self.delta_X = self.max_X - self.min_X
        self.delta_Y = self.max_Y - self.min_Y
        self.delta_Z = self.max_Z - self.min_Z
        topo_Z = self.delta_Z/255
        #center the axis of all points
        for p in self.nodes:
            p.topo = (p.z-self.min_Z)/topo_Z
            p.x = (p.x-self.min_X)-(self.delta_X/2)
            p.y = (p.y-self.min_Y)-(self.delta_Y/2)
            p.z = (p.z-self.min_Z)-(self.delta_Z/2)
            for n in p.kills: #including the points in the kill lists
                n.x = (n.x-self.min_X)-(self.delta_X/2)
                n.y = (n.y-self.min_Y)-(self.delta_Y/2)
                n.z = (n.z-self.min_Z)-(self.delta_Z/2)

        
    def conform_point(self, (px, py, pz)):
        return ((px-self.min_X)-(self.delta_X/2), (py-self.min_Y)-(self.delta_Y/2), (px-self.min_Z)-(self.delta_Z/2))

    def select_point(self):
        node_index = self.get_point_on_screen(pygame.mouse.get_pos())
        idx=0
        for node in self.nodes:
            if(idx == node_index):
                node.selected = True
            else:
                node.selected = False
            idx += 1

     
    def get_point_on_screen(self, (mx, my)):
        dist = None
        index = 0
        n = 0
        for p in self.nodes:
            lx = mx-p.X_2d
            ly = my-p.Y_2d
            td = math.sqrt( (lx*lx)+(ly*ly) )
            if (dist is None) or (td < dist):
                dist=td
                index = n
            n += 1
        return index
    
    def project(self, (px, py, pz)):
        if (self.zoom + pz) == 0:
            factor = 0
        else: factor = self.fov / (self.zoom + pz)
        x = px * factor + self.width / 2
        y = -py * factor + self.height / 2
        return (int(x), int(y))

    
    def run(self):
        self.setup_map()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("c0z3n's Killdata Visualizer")
        self.clock = pygame.time.Clock()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and self.zoom > 1.5:
                    self.zoom -= 0.05 * self.zoom
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    self.zoom += 0.05 * self.zoom
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.select_point()
                    
            kbstate = pygame.key.get_pressed()
            if kbstate[K_UP]:
                self.trans_Y += 1
            if kbstate[K_DOWN]:
                self.trans_Y -= 1
            if kbstate[K_LEFT]:
                self.trans_X -= 1
            if kbstate[K_RIGHT]:
                self.trans_X += 1
            if kbstate[K_z]:
                self.angle_Z += 1
            if kbstate[K_x]:
                self.angle_Z -= 1
            if kbstate[K_q]:
                self.angle_X += 1
            if kbstate[K_w]:
                self.angle_X -= 1
            if kbstate[K_a]:
                self.angle_Y += 1
            if kbstate[K_s]:
                self.angle_Y -= 1
            
            self.clock.tick(50)
            self.screen.fill((0,0,0))
            
            for v in self.nodes:
                v.render()
            
            pygame.display.flip()

if __name__ == "__main__":
    Scene().run()
