import itertools
import random
import queue

from tqdm import tqdm


class StepGenerator:
    def __init__(self, x, y, w, h):
        self.step = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (1, -1), (1, 1), (-1, 1)]
        random.shuffle(self.step)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vis = set()
        self.qu = queue.Queue()
        self.qu.put((self.x, self.y))

    def __next__(self):
        while not self.qu.empty():
            a, b = self.qu.get()
            if (a, b) in self.vis:
                continue
            self.vis.add((a, b))
            for i, j in self.step:
                x = a + i
                y = b + j
                if 0 <= x < self.w and 0 <= y < self.h and (x, y) not in self.vis:
                    self.qu.put((x, y))

            if (a, b) == (self.x, self.y):
                continue
            else:
                return a, b


def get_nearest_n(x, y, n, w, h, cls):
    g = StepGenerator(x, y, w, h)
    ans = []
    while n > 0:
        a, b = next(g)
        if cls[a][b] > 0:
            ans.append(cls[a][b])
            n -= 1
    return ans


def cal_sub_graph(links):
    if not links:
        return 0
    eles = set()
    eles.add(links[0][0])
    eles.add(links[0][1])
    while True:
        inds = set()
        for i, (a, b) in enumerate(links):
            if a in eles or b in eles:
                eles.add(a)
                eles.add(b)
                inds.add(i)
        if len(inds) == 0:
            break
        links = [links[i] for i in range(len(links)) if i not in inds]
    # print(eles)
    return cal_sub_graph(links) + 1


# n: 人数,
# w: 教室宽度
# h: 教室长度 n <= w * h
def simulate(n, w, h, cnt):
    all_n = w * h
    rev = False
    if n > all_n / 2:
        n = all_n - n
        rev = True
    cls = [[0 for _ in range(h)] for _ in range(w)]
    for i in range(1, n + 1):
        while True:
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            if cls[x][y] == 0:
                cls[x][y] = 1
                break
    if rev:
        cls = [[0 if x == 1 else 1 for x in l] for l in cls]
        n = all_n - n
    i = 1
    stu = []
    for x, y in itertools.product(range(w), range(h)):
        if cls[x][y]:
            cls[x][y] = i
            stu.append((i, x, y))
            i += 1
    # for l in cls:
    #     print(l)
    link = []
    for i, x, y in stu:
        for nei in get_nearest_n(x, y, cnt, w, h, cls):
            link.append((i, nei))

    # print(link)
    return cal_sub_graph(link)


def test(n, x, y, cnt, repeat=3000):
    res = {}
    print(f"人数:{n} 教室:{x}x{y} 拍照次数:{cnt} 上座率:{n / (x * y)}")
    for _ in range(repeat):
        r = simulate(n, x, y, cnt)
        if r not in res:
            res[r] = 1
        else:
            res[r] += 1
    print(res)


if __name__ == '__main__':
    test(70, 12, 10, 2)
    test(80, 12, 10, 2)
    test(90, 12, 10, 2)
    test(70, 12, 10, 3)
    test(80, 12, 10, 3)
    test(90, 12, 10, 3)

# 人数:70 教室:12x10 拍照次数:2 上座率:0.5833333333333334
# {1: 2195, 2: 690, 3: 100, 4: 13, 5: 2}
# 人数:80 教室:12x10 拍照次数:2 上座率:0.6666666666666666
# {1: 2608, 2: 352, 3: 40}
# 人数:90 教室:12x10 拍照次数:2 上座率:0.75
# {1: 2806, 2: 187, 3: 7}
# 人数:70 教室:12x10 拍照次数:3 上座率:0.5833333333333334
# {1: 2946, 2: 53, 3: 1}
# 人数:80 教室:12x10 拍照次数:3 上座率:0.6666666666666666
# {1: 2977, 2: 23}
# 人数:90 教室:12x10 拍照次数:3 上座率:0.75
# {1: 2994, 2: 6}
