matrix = np.array([[0, 1, 1, 1, 1, 1, 1, 0], 
                           [0, 1, 1, 1, 1, 1, 1, 0], 
                           [0, 1, 1, 1, 1, 1, 1, 0],
                           [0, 1, 1, 1, 1, 1, 1, 0], 
                           [0, 0, 0, 0, 1, 1, 1, 1], 
                           [0, 0, 0, 0, 1, 1, 1, 1], 
                           [0, 1, 1, 1, 0, 0, 0, 1]])
grid = VGroup()
number_of_cols = len(matrix[0])
number_of_rows = len(matrix)
square_size = 0.5  
for i in range(number_of_rows):
    for j in range(number_of_cols):
        square = Square(side_length=square_size).set_stroke(BLACK, 1)
        square.move_to((j * square_size, -i * square_size, 0))
        number = Text(str(matrix[i][j]), color=BLACK, font="SF Pro", font_size=18).move_to(square.get_center())
        if ( matrix[i][j] == 0):
            grid_black.add(square)
            text_white.add(number)
        grid.add(VGroup(square, number))
grid.move_to(ORIGIN).scale(1)
self.play(FadeIn(grid))
s1 = Text("Input Matrix", font = "Segoe UI", color = BLACK, font_size= 25).next_to(grid, UP)
self.play(Write(s1))
self.play(Circumscribe(s1, color = BLUE, fade_out=True))
self.wait(1)