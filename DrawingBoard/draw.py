import pygame
from pygame.locals import *
import math


# 笔刷类
class Brush:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 1
        self.drawing = False
        self.last_pos = None

        self.style = False
        self.brush = pygame.image.load('images/brush.png').convert_alpha()
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))
   
    # 开始绘制，并记录坐标
    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos
    
    # 结束绘制
    def end_draw(self):
        self.drawing = False
    # 设置笔刷样式
    def set_brush_style(self, style):
        print("* set brush style to", style)
        self.style = style
   
    # 获取笔刷样式
    def get_brush_style(self):
        return self.style
   
    # 获取当前的笔刷
    def get_current_style(self):
        return self.brush_now
    
    # 设置笔刷大小
    def set_size(self, size):
        if size < 1:
            size = 1
        elif size > 32:
            size = 32
        print("* set brush size to", size)
        self.size = size
        self.brush_now = self.brush.subsurface((0, 0), (size*2, size*2))
    
    # 获取笔刷大小
    def get_size(self):
        return self.size
   
    # 设置笔刷颜色
    def set_color(self, color):
        self.color = color
        for i in range(self.brush.get_width()):
            for j in range(self.brush.get_height()):
                self.brush.set_at((i, j), color + (self.brush.get_at((i, j)).a,))
    
    # 获取笔刷颜色
    def get_color(self):
        return self.color
    
    # 绘制
    def draw(self, pos):
        if self.drawing:
            for p in self._get_points(pos):
                if self.style:
                    self.screen.blit(self.brush_now, p)
                else:
                    pygame.draw.circle(self.screen, self.color, p, self.size)
            self.last_pos = pos
    
    # 为了平滑线条，获取当前点和前一个点之前所有需要绘制的点
    def _get_points(self, pos):
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x**2 + len_y**2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append((points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points))


# 图形类
class Shape:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        # self.size = 1
        self.start_pos = None
        self.last_pos = None
        self.drawing = False
        self.style = False
    
    def start_draw(self, pos):
        self.start_pos = pos
        self.drawing = True

    def end_draw(self):
        self.drawing = False

    def set_shapes_style(self, style):
        print("* set shape style to", style)
        self.style = style
    
    def get_shapes_style(self):
        return self.style
    
    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    # 根据开始绘画位置和当前位置来画圆或者矩形
    def draw(self, start_pos, end_pos):
        '''
        pygame.draw.circle(self.screen, (255, 0, 0), 
        (int((start_pos[0]+end_pos[0])/2), int((start_pos[1]+end_pos[1])/2)),
        int(math.sqrt((end_pos[0]-start_pos[0])**2+(end_pos[1]-start_pos[1])**2)/2), 
        0)
        '''
        if self.drawing:
            for p in self._get_points(end_pos):
                if self.style:
                    pygame.draw.rect(self.screen, self.color,
                    (start_pos[0], start_pos[1], end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]),
                    0)
                else:
                    pygame.draw.circle(self.screen, self.color, 
                    (int((start_pos[0]+end_pos[0])/2), int((start_pos[1]+end_pos[1])/2)),
                    int(math.sqrt((end_pos[0]-start_pos[0])**2+(end_pos[1]-start_pos[1])**2)/2), 
                     0)

    # 为了平滑线条，获取当前点和起始点之前所有需要绘制的点        
    def _get_points(self, pos):
        points = [(self.start_pos[0], self.start_pos[1])]
        len_x = pos[0] - self.start_pos[0]
        len_y = pos[1] - self.start_pos[1]
        length = math.sqrt(len_x**2 + len_y**2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append((points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points))


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        self.cle = None
        # 笔刷类或是图形类
        self.style = True
        # 画板预定义的颜色值
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]
        # 计算每个色块在画板中的坐标位置
        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 254 + int(i / 2) * 32, 32, 32)
            self.colors_rect.append(rect)
        self.pens = [
            pygame.image.load("images/pen1.png").convert_alpha(),
            pygame.image.load("images/pen2.png").convert_alpha()
        ]
        # 计算两种笔刷按钮的坐标位置
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)
        self.sizes = [
            pygame.image.load("images/big.png").convert_alpha(),
            pygame.image.load("images/small.png").convert_alpha()
        ]
        # 计算调整笔刷大小按钮的坐标位置
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(10 + i * 32, 138, 32, 32)
            self.sizes_rect.append(rect)
        self.shapes = [
            pygame.image.load("images/circle.png").convert_alpha(),
            pygame.image.load("images/rect.png").convert_alpha()
        ]
        # 计算两种图形的坐标位置
        self.shapes_rect = []
        for (i, img) in enumerate(self.shapes):
            rect = pygame.Rect(10 + i * 32, 170, 32, 32)
            self.shapes_rect.append(rect)

    def set_brush(self, brush):
        self.brush = brush

    def set_cle(self, cle):
        self.cle = cle
    
    # 绘制菜单栏 
    def draw(self):
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.sizes):
            self.screen.blit(img, self.sizes_rect[i].topleft)
        for (i, img) in enumerate(self.shapes):
            self.screen.blit(img, self.shapes_rect[i].topleft)
        '''
        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 180 + 32
        if self.brush.get_brush_style():
            x = x - size
            y = y - size
            self.screen.blit(self.brush.get_current_style(), (x, y))
        else:
            pygame.draw.circle(self.screen, self.brush.get_color(), (x, y), size)
            '''
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

    # 自定义菜单栏按钮的点击相应    
    def click_button(self, pos):
        # 笔刷类型
        for (i, rect) in enumerate(self.pens_rect):
            if rect.collidepoint(pos):
                self.brush.set_brush_style(bool(i))
                self.style = True
                return True
        # 笔刷大小
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i:
                    self.brush.set_size(self.brush.get_size() - 1)
                else:
                    self.brush.set_size(self.brush.get_size() + 1)
                return True
        # 颜色
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                self.cle.set_color(self.colors[i])
                return True
        # 图形类型
        for (i, rect) in enumerate(self.shapes_rect):
            if rect.collidepoint(pos):
                self.cle.set_shapes_style(bool(i))
                self.style = False
                return True
        return False


class Painter:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Painter")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.cle = Shape(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_brush(self.brush)
        self.menu.set_cle(self.cle)
        
    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            # 设置帧率
            self.clock.tick(30)
            # 监听事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                # 鼠标按下事件
                elif event.type == MOUSEBUTTONDOWN:
                    if event.pos[0] <= 74 and self.menu.click_button(event.pos):
                        pass
                    else:
                        if self.menu.style:
                            self.brush.start_draw(event.pos)
                        else:
                            self.cle.start_draw(event.pos)
                # 鼠标移动事件
                elif event.type == MOUSEMOTION:
                    if self.menu.style:
                        self.brush.draw(event.pos)
                    else:
                        self.cle.draw(self.cle.start_pos, event.pos)
                elif event.type == MOUSEBUTTONUP:
                    if self.menu.style:
                        self.brush.end_draw()
                    else:
                        self.cle.end_draw()
            self.menu.draw()
            pygame.display.update()


# 主函数
def main():
    app = Painter()
    app.run()


if __name__ == '__main__':
    main()