# -*- coding: utf-8 -*-
"""
A Simple Version of Midway Island Naval Warfare with Python for Easy Learning by lixingqiu
这个射击游戏是使用Arcade模块制作的。这个版本是核心版本，演示了爆炸效果，类的继承，按键检测等。
This shooting game is made using Arcade module. This version is the core version and demonstrates explosion effects, class inheritance, and key detection.
其中滚动的背景是使用两张图片制作的，它们相隔SCREEN_HEIGHT的高度。如果图片的top到了最底下，也就是坐标为0了，那么它就瞬间移到最顶上去。
The scrolling background is made using two pictures, which are separated by the height SCREEN_HEIGHT. If the top of the picture reaches the bottom, that is, the coordinate is 0, then it will move instantaneously to the top.
要注意Arcade的坐标系统和数学中的坐标系统一样，在本游戏中是以左下角为原点，y轴正向上。在Pygame中则是左上角为原点，y轴正向下。
It should be noted that the coordinate system of Arcade is the same as the coordinate system in mathematics. In this game, the lower left corner is used as the origin, and the y axis is upward. In Pygame, the upper left corner is the origin, and the y-axis is positive > bottom.

"""

__author__ = "lixingqiu"
__date__ = "2019/3/13"
__url__ = "http://www.lixingqiu.com/?p=209"
__qq__ = "406273900"

import os
import random
import arcade

SPRITE_SCALING = 1.0

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "A Simple Version of Midway Island Naval Warfare with Python for Easy Learning Python (中途岛海战街机模拟)"
ENEMY_COUNT = 100
MOVEMENT_SPEED  = 5

class Explosion(arcade.Sprite):
    """ 创建可爆炸的角色 create explosion sprite""" 

    def __init__(self, texture_list,x,y):
        """texture_list是已经load了的造型列表"""
        super().__init__()

        self.center_x = x
        self.center_y = y
        # 第一帧
        self.current_texture = 0      # 这是造型索引号
        self.textures = texture_list  # 这是每帧图片列表
        self.set_texture(self.current_texture)

    def update(self):

        # 更新每帧的图片，到了最后一帧后就会删除自己。
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()

class Bullet(arcade.Sprite):
    """子弹类，继承自Arcade自带的角色类，它从飞机的坐标射出"""
    def __init__(self,image,plane):
        super().__init__(image)
        self.center_x = plane.center_x
        self.center_y = plane.center_y
        self.change_y = 20        

    def update(self):
        """每帧更新坐标 update coordinates"""
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom >  SCREEN_HEIGHT: self.kill()
        
class Background(arcade.Sprite):
    
    def __init__(self,image):
        super().__init__(image)    
        self.change_y = -10       

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.top <=0 : self.bottom = SCREEN_HEIGHT
        
class Enemy(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image)
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT,SCREEN_HEIGHT*30)

    def update(self):
        
        if self.top<=0:self.kill()
            
        
class MyGame(arcade.Window):
    """ 应用程序主要类. """

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        # 角色列表定义
        self.all_sprites_list = None
        self.enemy_list = None

        # 定义玩家的相关变量 
        self.score = 0
        self.player_sprite = None

        self.enemy_explosion_images = []
#        for i in range(55):
#            # 加载从 explosion0000.png 到 explosion0054.png 的所有图片为敌人的爆炸效果动画帧            
#            texture_name = "images/enemy_explosion/explosion{x:04d}.png".format(x=i)
#            self.enemy_explosion_images.append(arcade.load_texture(texture_name))             

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"
        # Load the explosions from a sprite sheet
        self.enemy_explosion_images = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def start_new_game(self):
        """ 设置与初始化游戏 """
        
        self.shoot_sound = arcade.sound.load_sound("images/midway/Shot.wav")        
        self.background_music = arcade.sound.load_sound("images/midway/background.wav")
        arcade.sound.play_sound(self.background_music)        
        
        # 实例化所有角色列表      
        self.enemy_list = arcade.SpriteList()            # 敌人列表        
        self.bullet_list = arcade.SpriteList()           # 玩家子弹列表
        self.all_sprites_list = arcade.SpriteList()      # 所有角色列表
        self.enemy_explosion_list = arcade.SpriteList()  # 所有敌人的爆炸角色列表
        
        # 设置玩家操作的飞机
        self.score = 0
        self.player_sprite = arcade.AnimatedTimeSprite("images/midway/Plane 1.png",SPRITE_SCALING)
        self.player_sprite.textures.append(arcade.load_texture("images/midway/Plane 2.png"))
        self.player_sprite.textures.append(arcade.load_texture("images/midway/Plane 3.png"))
        self.player_sprite.scale = 1.0
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_sprite.health  = 10             # 血条，在左上角画一根即可
        self.all_sprites_list.append(self.player_sprite)

        # 敌人角色生成
        for i in range(ENEMY_COUNT):
            enemy = Enemy("images/midway/Fighters.png")
            self.enemy_list.append(enemy)
            self.all_sprites_list.append(enemy)
            
        sea_image = "images/midway/sea.png"
        # Setting a Fixed Background 设置不动的背景 To cover up rolling background cracks
        self.background = arcade.Sprite(sea_image)
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.bottom = 0
        
        # 设置滚动背景，两个最先画的角色往下移，移到一定坐标就到上面去
        self.background1 = Background(sea_image)
        self.background1.center_x = SCREEN_WIDTH // 2
        self.background1.bottom = 0
        self.all_sprites_list.append(self.background1)
        
        self.background2 = Background(sea_image)
        self.background2.center_x = SCREEN_WIDTH // 2
        self.background2.bottom = SCREEN_HEIGHT  
        self.all_sprites_list.append(self.background2)

        # 1943logo
        self.logo_1943 = arcade.Sprite("images/midway/1943Logo2.png")
        self.logo_1943.center_x  = SCREEN_WIDTH // 2
        self.logo_1943.center_y  = SCREEN_HEIGHT // 2
        self.interval = 60
        self.interval_counter = 0
        
        
    def on_key_press(self, key, modifiers):
        """鼠标按键事件 """
        if self.player_sprite.health <=0 :return
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.J:
            arcade.sound.play_sound(self.shoot_sound)
            self.bullet = Bullet("images/midway/Shot 1.png",self.player_sprite)
            self.bullet_list.append(self.bullet)
            self.all_sprites_list.append(self.bullet)            

    def on_key_release(self, key, modifiers):
        """鼠标松开事件 """
        if self.player_sprite.health <=0 :return
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def update(self, delta_time):
        """ 游戏更新逻辑"""

        # 更新坐标等等
        #  print(self.background2.bottom - self.background1.top)
        distance = self.background2.bottom - self.background1.top
        if  distance < 0 and distance > -40:   # Fissure remedy 弥补裂隙问题
             
            self.background2.bottom = self.background1.top
            
        self.enemy_list.move(0, -5)
        self.all_sprites_list.update() 
        self.player_sprite.update_animation()         

        if self.player_sprite.health > 0:
            # 玩家和所有敌机的碰撞检测.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_list)
            # 遍历碰到的敌机列表
            for enemy in hit_list:
                enemy.kill()
                self.player_sprite.health -= 1
                if self.player_sprite.health < 0 :
                    e = Explosion(self.enemy_explosion_images)
                    e.center_x = self.player_sprite.center_x
                    e.center_y = self.player_sprite.center_y
                    e.update()
                    self.player_sprite.kill()
                    
                e = Explosion(self.enemy_explosion_images,enemy.center_x,enemy.center_y)
                e.center_x = enemy.center_x
                e.center_y = enemy.center_y
                e.update()
                self.enemy_explosion_list.append(e)
                self.all_sprites_list.append(e)
            
        # 每个敌人有没有碰到子弹
        for enemy in self.enemy_list:   
            hit_list = arcade.check_for_collision_with_list(enemy,self.bullet_list)
            if len(hit_list) > 0:
                enemy.kill()
                [b.kill() for b in hit_list]   # 碰到的每颗子弹都删除
                self.score += len(hit_list)                
                e = Explosion(self.enemy_explosion_images,enemy.center_x,enemy.center_y)
                e.center_x = enemy.center_x
                e.center_y = enemy.center_y
                e.update()
                self.enemy_explosion_list.append(e)
                self.all_sprites_list.append(e)
                
    def on_draw(self):
        """   渲染屏幕    """

        # 开始渲染，此命令要在所有重画命令之前
        arcade.start_render()
        self.background.draw()    # 画不动的背景，弥补滚动背景裂纹问题
        self.background1.draw()   # 画滚动背景
        self.background2.draw()   # 画滚动背景
        # 画所有的角色
        self.enemy_list.draw()
        if self.player_sprite.health > 0:            
           self.player_sprite.draw()
        self.bullet_list.draw()
        self.enemy_explosion_list.draw()
        
        # 画得分情况
        score = "score: " + str(self.score) + " , Blood volume: " + str(self.player_sprite.health)
        arcade.draw_text(score, 10, 20, arcade.color.WHITE, 14 )

        if self.player_sprite.health < 1:  # 血量小于1显示游戏结束
           self.interval_counter +=1
           if self.interval_counter < self.interval //2: self.logo_1943.draw()
           if self.interval_counter % self.interval == 0:self.interval_counter = 0
              
class Cover(arcade.Window):
    """封面类"""
    def __init__(self, width, height, title):

        super().__init__(width, height, title)

    def setup(self):
        self.background = arcade.Sprite("images/midway/Logo1.png")
        self.background.left = 50
        self.background.top = SCREEN_HEIGHT
        self.demo_plane = arcade.AnimatedTimeSprite("images/midway/Plane 1.png",0.8)
        self.demo_plane.textures.append(arcade.load_texture("images/midway/Plane 2.png"))
        self.demo_plane.textures.append(arcade.load_texture("images/midway/Plane 3.png"))
        self.demo_plane.scale = 0.8
        self.demo_plane.center_x = 300
        self.demo_plane.center_y = 100
        self.begin_music = arcade.sound.load_sound("images/midway/start.wav")
        arcade.sound.play_sound(self.begin_music)
        
    def on_key_press(self, key, modifiers):
        """鼠标按键事件 """

        if key == arcade.key.SPACE: # 按空格键关闭窗口
            self.close()
                                        
    def update(self,delta_time):
        self.demo_plane.update()
        self.demo_plane.update_animation()
        
                                        
    def on_draw(self):
        """        渲染屏幕        """

        # 开始渲染，此命令要在所有重画命令之前
        arcade.start_render()
        self.background.draw()
        self.demo_plane.draw()         
        

def main():

    cover = Cover(800, 600, SCREEN_TITLE)
    cover.setup()
    arcade.run()
    
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()
