import math
import pygame

class KillNode:
    def __init__(self, env, x = 0, y = 0, z = 0, kills = [0], color = (0, 0, 0), topo = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.kills = kills
        self.topo = topo
        self.color = color
        self.env = env
        self.selected = False
        
        self.angle_X = self.env.angle_X
        self.angle_Y = self.env.angle_Y
        self.angle_Z = self.env.angle_Z
        self.fov = self.env.fov
        self.zoom = self.env.zoom
        self.pointradius = self.env.pointradius
        
        self.projected_X = 0
        self.projected_Y = 0
        self.X_2d = 0
        self.Y_2d = 0
        
        
 
    def rotate_X(self):
        rad = self.angle_X * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return KillNode(self.env, self.x, y, z, self.kills, self.color, self.topo)
 
    def rotate_Y(self):
        rad = self.angle_Y * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return KillNode(self.env, x, self.y, z, self.kills, self.color, self.topo)
 
    def rotate_Z(self):
        rad = self.angle_Z * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return KillNode(self.env, x, y, self.z, self.kills, self.color, self.topo)
        
    def project(self, win_width, win_height, fov, viewer_distance):
        if (viewer_distance + self.z) == 0:
            factor = 0
        else: factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return (int(x), int(y))
    
    def render(self):
        win_X = self.env.width
        win_Y = self.env.height
        self.zoom = self.env.zoom
        self.angle_X = self.env.angle_X
        self.angle_Y = self.env.angle_Y
        self.angle_Z = self.env.angle_Z
        self.trans_X = self.env.trans_X
        self.trans_Y = self.env.trans_Y
        
        rotated_point = self.rotate_X().rotate_Y().rotate_Z()
        projected_coords = rotated_point.project(win_X, win_Y, self.fov, self.zoom)
        
        self.X_2d = projected_coords[0] + self.trans_X
        self.Y_2d = projected_coords[1] + self.trans_Y
        
        for p in self.kills:
            p.angle_X = self.env.angle_X
            p.angle_Y = self.env.angle_Y
            p.angle_Z = self.env.angle_Z
            
        self.pointradius = self.env.pointradius
        
        
        
        color = (32+self.topo*.8, 32+self.topo*.8, 32+self.topo*.8)
        if self.selected:
            color = (0, 255, 0)
            self.pointradius = 2
            for p in self.kills:
                e = p.rotate_X().rotate_Y().rotate_Z().project(win_X, win_Y, self.fov, self.zoom)
                ep = (e[0] + self.trans_X, e[1] + self.trans_Y)
                try: pygame.draw.line(self.env.screen,  color, 
                                                        ep,
                                                        (self.X_2d, self.Y_2d),
                                                        1)
                except: pass
                
            
            
        try: pygame.draw.circle(self.env.screen,     color,
                                                     (self.X_2d, self.Y_2d),
                                                     self.pointradius, 0)
        except:
            pass
