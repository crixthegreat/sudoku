数独游戏 A game of  sudoku

1. **数据结构**

- 一个数独游戏由宽高分别为 block_width,  block_height 的小方块组成

    ![](https://github.com/crixthegreat/sudoku/blob/master/readme_pic/1.png?raw=true)

- 这样的游戏允许出现的最大数字为 max_number = block_width x block_height （假定最小为1） 

- 为确保最终盘面为正方形，这样的方块的行与列数显然应为 row = block_width, column = block_height

    ![image-20200302162751717](https://github.com/crixthegreat/sudoku/blob/master/readme_pic/2.png?raw=true)

- 块的总个数也为 max_number，而数字的总个数应为  (max_number)^ 2

- 最常见的 9x9 的数独即由  (block_width=3) x (block_height=3) 的小方块组成，每个方块中最大的数 max_number 为 9 个，方块的个数也为 9 个，总数字的个数为 9^2 = 81

    ![image-20200302162855145](https://github.com/crixthegreat/sudoku/blob/master/readme_pic/3.png?raw=true)

- 为计算方便，一个块作为一个列表存储，即 block = [number+1 for number in range(max_number)]

- 整个数独矩阵则为 matrix = [block for _ in range(max_number)]

2. **核心算法**

- 为确保数独游戏有解，可以先生成数独的一个解，然后去除（隐藏）其中的一些数字。

- 一个标准的解可以简单用以下方法求得：

    ![image-20200302163711038](https://github.com/crixthegreat/sudoku/blob/master/readme_pic/4.png?raw=true)

    - 每一个块分别根据其所在的行与列，计算出其第一个数字，规律见上图。

        `start_number = block_no//self.block_height + 1 + (block_no % self.block_height) * self.block_width`

    - 每一个块以第一个数字开始，按顺序得出该块中的其余数字。即，将顺序列表以：步长=首个数字 - 1 左移，即 [num+1 for num in range(max_number)].left_rotate(first_number - 1)

- 为保证游戏性，对上面获得的数独的解进行随机处理：

    数独的解具有以下性质：

    - 将数独的一个解的**同一个块内**的任意两行或两列交换，解仍然成立

        ![image-20200302163236295](https://github.com/crixthegreat/sudoku/blob/master/readme_pic/5.png?raw=true)

        ![image-20200302163210304](https://github.com/crixthegreat/sudoku/blob/master/readme_pic/6.png?raw=true)

    - 将数独的任意两行或两列的**整块数据**交换，解仍然成立

        ![image-20200302163545288](https://github.com/crixthegreat/sudoku/blob/master/readme_pic/7.png?raw=true)

其余就是大量枯燥的 GUI 工作了。

游戏使用 Python + cocos2d 实现。
