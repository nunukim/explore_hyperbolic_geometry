# 自由群内の移動を書く。

import sys

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

import util

def _make_line(x, y, n=4):
    x = np.asarray(x)
    y = np.asarray(y)

    dy = util.translate(y, -x)
    lin = np.linspace(0, 1, n)[:,None] * dy[None,:]
    return util.translate(lin, x)

def _unit_tile(tile_size):
    dx = 0.5*tile_size
    xs = np.concatenate([
        _make_line([-dx,-dx], [-dx, dx]),
        _make_line([-dx, dx], [ dx, dx]),
        _make_line([ dx, dx], [ dx,-dx]),
        _make_line([ dx,-dx], [-dx,-dx])
        ], axis=0)

    return xs

def _translate_tile(x, position_code, tile_size):
    for s in position_code[::-1]:
        delta = None
        if s == 'u':
            delta = [0,tile_size]
        elif s == 'd':
            delta = [0,-tile_size]
        elif s == 'l':
            delta = [-tile_size,0]
        elif s == 'r':
            delta = [tile_size,0]
        else:
            raise ValueError("invalid position code")
        x = util.translate(x, np.array(delta))

    return x

def _plot_xy(xy, *args, **kwargs):
    plt.plot(xy[:,0], xy[:,1], *args, **kwargs)

def make_tile_xy(size=4, step=10, tile_size=0.1):
    # 2階の自由群を作る。
    g = ["u", "d", "l", "r"]
    G = g
    for i in range(size):
        a = []
        for c in g:
            if c[-1] != "d": a.append(c+"u")
            if c[-1] != "u": a.append(c+"d")
            if c[-1] != "r": a.append(c+"l")
            if c[-1] != "l": a.append(c+"r")
        g = a
        G = G + g
    # print(G)

    # タイル配置を作成
    positions = [""]
    for g in G:
        p = "".join([c*step for c in g[:-1]])
        for s in range(step):
            positions.append(p + g[-1]*s)

    # タイルの座標に変換
    tile = _unit_tile(tile_size)
    xys = np.array([_translate_tile(tile, pos, tile_size) for pos in positions])

    return xys # (tiles, points_in_tile, xy)

if __name__ == '__main__':

    fn = sys.argv[1]
    print(fn)

    step = 9
    n = 6
    tile_size = 0.1

    # 描画する点の集合を作成
    tiles = make_tile_xy(n, step=step, tile_size=0.1)
    marker = np.array([
        [ 0.00, 0.03],
        [-0.03,-0.03],
        [ 0.00,-0.01],
        [ 0.00, 0.03],
        [ 0.03,-0.03],
        [ 0.00,-0.01],
        ])

    def draw(i):
        state = "rotate"
        rotate = 0
        advance = 0
        print(i)
        for j in range(i):
            if state == "rotate":
                rotate += np.pi*0.5 * 0.1
                if rotate >= np.pi*0.5:
                    rotate = 0
                    state = "advance"
            elif state == "advance":
                advance = util.translate([0,advance], [0,-0.02])[1]
                finish =  _translate_tile([0,0], "d"*step, tile_size=tile_size)[1]
                if finish > advance:
                    advance = finish
                    state = "finish"
        if state == "finish":
            print("finish")

        t_tiles = util.rotate(tiles, rotate)
        t_tiles = util.translate(t_tiles, [0,advance])

        plt.cla()
        util.draw_circle()

        plt.plot(t_tiles[:,:,0].T, t_tiles[:,:,1].T, lw=0.5, color="blue")

        _plot_xy(marker, color="red", lw=1)

    fig = plt.figure(figsize=(6,6))
    ax = plt.axes(xlim=(-1,1), ylim=(-1,1))
    ax.set_aspect('equal')

    anim = animation.FuncAnimation(fig, draw, interval=100, frames=57, repeat=True)

    anim.save("{}.gif".format(fn), writer="imagemagick")
    # plt.show()


