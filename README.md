# python3_arcade_midway_island_war_simple_simulate
A Simple Version of Midway Island Naval Warfare with Python for Easy Learning by lixingqiu
这个射击游戏是使用Arcade模块制作的。这个版本是核心版本，演示了爆炸效果，类的继承，按键检测等。
This shooting game is made using Arcade module. This version is the core version and demonstrates explosion effects, class inheritance, and key detection.
其中滚动的背景是使用两张图片制作的，它们相隔SCREEN_HEIGHT的高度。如果图片的top到了最底下，也就是坐标为0了，那么它就瞬间移
到最顶上去。
The scrolling background is made using two pictures, which are separated by the height SCREEN_HEIGHT. If the top of the picture reaches the bottom, that is, the coordinate is 0, then it will move instantaneously to the top.
要注意Arcade的坐标系统和数学中的坐标系统一样，在本游戏中是以左下角为原点，y轴正向上。在Pygame中则是左上角为原点，y轴正向>下。
It should be noted that the coordinate system of Arcade is the same as the coordinate system in mathematics. In this game, the lower left corner is used as the origin, and the y axis is upward. In Pygame, the upper left corner is the origin, and the y-axis is positive > bottom.

运行这个游戏需要安装arcade模块。for more arcade game or animation, please open url http://www.lixingqiu.com
