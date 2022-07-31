from random import randint
from math import floor
import pygame as pg


ACTION_NONE = {'forward': False, 'backward': False,
               'left': False, 'right': False, 'attack': False}


class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [4, 2, 1, 1]
        self.action = ACTION_NONE.copy()
        self.playerID = helper.get_self_id()
        self.walls = self.helper.get_wall_position()

    def reset(self):
        self.action = ACTION_NONE.copy()

    def avoidbullet(self):
        bullet = self.helper.get_bullet_info()
        # print(bullet)
        # print('==========')
        for i in bullet:
            myPos = self.helper.get_self_position()
            speed = i.get('speed')
            angle = myPos.angle_to(speed)
            angle = (angle*180)/pi
            if angle > 0:
                angle = angle % 360
            else:
                if abs(angle) % 360 == 0:
                    angle = angle + 360 * abs(angle) // 360
                else:
                    angle = angle + 360 * ((abs(angle) // 360) + 1)

            print(angle)

    def buff(self):
        buffpos = self.helper.get_nearest_item_info()['position']
        selfpos = self.helper.get_self_position()
        if ((selfpos-buffpos).normalize() - self.helper.get_self_direction()).magnitude() < 0.1:
            self.action['forward'] = True
        else:
            self.action['left'] = True

    def attack_decide(self):
        self_position = self.helper.get_self_position()
        nearest_player = self.helper.get_nearest_player_position()
        x1, y1 = self_position[0], self_position[1]
        x2, y2 = nearest_player[0], nearest_player[1]
        if floor(x1) == floor(x2):
            # y下去比
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if y1 >= y2:
                for i in range(int(y1-y2)+2):
                    if pg.Vector2([x1, y2]) in self.walls:
                        #print('obstacle detected 1')
                        return False
                    y2 += 1
                #print('non-detected 1')
                return True

            else:
                for i in range(int(y2-y1)+2):
                    if pg.Vector2([x1, y1]) in self.walls:
                        #print('obstacle detected 2')
                        return False
                    y1 += 1
                #print('non-detected 2')
                return True

        elif floor(y1) == floor(y2):
            # x下去比
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if x1 >= x2:
                for i in range(int(x1-x2)+2):
                    if pg.Vector2([x2, y1]) in self.walls:
                        #print('obstacle detected 3')
                        return False
                    x2 += 1
                #print('non-detected 3')
                return True

            else:
                for i in range(int(x2-x1)+2):
                    if pg.Vector2([x1, y1]) in self.walls:
                        #print('obstacle detected 4')
                        return False
                    x1 += 1
                #print('non-detected 4')
                return True
        else:
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if x1 < x2:
                if y1 < y2:
                    for i in range(int(x2-x1+y2-y1)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 5')
                            return False
                        x1 += 1
                        y1 += 1
                    #print('non-detected 5')
                    return True
                else:
                    for i in range(int(x2-x1+y1-y2)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 6')
                            return False
                        x1 += 1
                        y1 -= 1
                    #print('non-detected 6')
                    return True
            else:
                if y1 > y2:
                    for i in range(int(x1-x2+y1-y2)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 5')
                            return False
                        x1 -= 1
                        y1 -= 1
                    #print('non-detected 5')
                    return True
                else:
                    for i in range(int(x1-x2+y2-y1)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 6')
                            return False
                        x1 -= 1
                        y1 += 1
                    #print('non-detected 6')
                    return True

    def attack(self):
        self.action['attack'] = True

    def avoid_RE_field(self):
        self_position = self.helper.get_self_position()
        nearest_RE = self.helper.get_nearest_RE_position()
        distance2RE = ((self_position[0]-nearest_RE[0])
                       ** 2 + (self_position[1]-nearest_RE[1])**2)**0.5
        return False if distance2RE <= 2.2 else True

    def decide(self):
        self.reset()
        if self.attack_decide() and self.avoid_RE_field():
            self.attack()
            self.buff()
        elif self.avoid_RE_field() and not self.attack_decide:
            self.action['forward'] = True
        if not self.avoid_RE_field():
            self.reset()

        return self.action
