class Rect:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

r = Rect(100, 20)
print(r.width, r.height, r.area())

class Square(Rect):
    def __init__(self, width):
        super().__init__(width, height)
