import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import math

class Point:
    """Класс, представляющий точку на холсте."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, color="black", size=3):
        """Рисует точку на холсте."""
        x1, y1 = self.x - size / 2, self.y - size / 2
        x2, y2 = self.x + size / 2, self.y + size / 2
        return canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

class Line:
    """Класс, представляющий линию между двумя точками."""
    def __init__(self, start_point, end_point):
        self.start = start_point
        self.end = end_point
    
    def draw(self, canvas, color="black", width=1):
        """Рисует линию на холсте."""
        return canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=color, width=width)


class Rectangle:
    """Класс, представляющий прямоугольник."""
    def __init__(self, start_point, end_point):
        self.start = start_point
        self.end = end_point
        
    def draw(self, canvas, color="black", width=1):
        """Рисует прямоугольник на холсте."""
        return canvas.create_rectangle(self.start.x, self.start.y, self.end.x, self.end.y, fill="", outline=color, width=width)

class Circle:
    """Класс, представляющий круг."""
    def __init__(self, center_point, radius):
        self.center = center_point
        self.radius = radius

    def draw(self, canvas, color="black", width=1):
        """Рисует круг на холсте."""
        x1, y1 = self.center.x - self.radius, self.center.y - self.radius
        x2, y2 = self.center.x + self.radius, self.center.y + self.radius
        return canvas.create_oval(x1, y1, x2, y2, fill="", outline=color, width=width)

class CanvasEditor:
    """Главный класс, управляющий окном, холстом и инструментами."""
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")
        
        self.current_color = "black"
        self.current_size = 1
        self.drawing_mode = "line"
        self.start_point = None
        self.selected_item = None
        self.items = [] # Список для хранения созданных объектов
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для инструментов
        tools_frame = ttk.Frame(self.root)
        tools_frame.pack(side=tk.TOP, fill=tk.X)

        # Кнопки для выбора инструмента
        ttk.Button(tools_frame, text="Линия", command=self.set_line_mode).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(tools_frame, text="Точка", command=self.set_point_mode).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(tools_frame, text="Прямоугольник", command=self.set_rectangle_mode).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(tools_frame, text="Круг", command=self.set_circle_mode).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(tools_frame, text="Ластик", command=self.set_eraser_mode).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(tools_frame, text="Выбрать цвет", command=self.choose_color).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Label(tools_frame, text="Размер:").pack(side=tk.LEFT, padx=5, pady=5)
        self.size_entry = ttk.Entry(tools_frame, width=5)
        self.size_entry.insert(0, "1")
        self.size_entry.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(tools_frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=5, pady=5)


        # Холст для рисования
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
    
    def set_line_mode(self):
        self.drawing_mode = "line"
        self.selected_item = None
    
    def set_point_mode(self):
        self.drawing_mode = "point"
        self.selected_item = None
    
    def set_rectangle_mode(self):
         self.drawing_mode = "rectangle"
         self.selected_item = None
         
    def set_circle_mode(self):
        self.drawing_mode = "circle"
        self.selected_item = None
    
    def set_eraser_mode(self):
        self.drawing_mode = "eraser"
        self.selected_item = None

    def choose_color(self):
        color = colorchooser.askcolor(title="Выбрать цвет")
        if color and color[1]:
            self.current_color = color[1]
        
    def get_current_size(self):
       try:
           return int(self.size_entry.get())
       except ValueError:
           return 1

    def on_canvas_click(self, event):
        """Обработчик нажатия на холст."""
        x, y = event.x, event.y
        
        if self.drawing_mode in ["line", "rectangle"]:
            self.start_point = Point(x, y)
        elif self.drawing_mode == "point":
            size = self.get_current_size()
            point = Point(x, y)
            point_id = point.draw(self.canvas, color=self.current_color, size=size)
            self.items.append((point, point_id))
        elif self.drawing_mode == "circle":
            self.start_point = Point(x, y)
        elif self.drawing_mode == "eraser":
            self.delete_item_under_mouse(x,y)
        else:
            self.start_point = None
            self.selected_item = self.canvas.find_closest(x, y)[0]
            
    def on_canvas_drag(self, event):
        if self.drawing_mode in ["line", "rectangle"] and self.start_point:
            x, y = event.x, event.y
            self.canvas.delete("temp_shape")
            temp_end = Point(x, y)
            if self.drawing_mode == "line":
              temp_shape = Line(self.start_point, temp_end)
            elif self.drawing_mode == "rectangle":
              temp_shape = Rectangle(self.start_point, temp_end)
            temp_shape.draw(self.canvas, color=self.current_color, width=self.get_current_size())
            self.canvas.itemconfig(temp_shape.draw(self.canvas, color=self.current_color, width=self.get_current_size()), tags="temp_shape")
        elif self.drawing_mode == "circle" and self.start_point:
             x, y = event.x, event.y
             radius = math.sqrt((x - self.start_point.x)**2 + (y - self.start_point.y)**2)
             self.canvas.delete("temp_circle")
             temp_circle = Circle(self.start_point, radius)
             temp_circle.draw(self.canvas, color=self.current_color, width=self.get_current_size())
             self.canvas.itemconfig(temp_circle.draw(self.canvas, color=self.current_color, width=self.get_current_size()), tags="temp_circle")
        elif self.selected_item:
            x, y = event.x, event.y
            dx = x - self.canvas.coords(self.selected_item)[0] - (self.canvas.coords(self.selected_item)[2] - self.canvas.coords(self.selected_item)[0])/2
            dy = y - self.canvas.coords(self.selected_item)[1] - (self.canvas.coords(self.selected_item)[3] - self.canvas.coords(self.selected_item)[1])/2
            self.canvas.move(self.selected_item, dx, dy)

    def on_canvas_release(self, event):
       if self.drawing_mode in ["line", "rectangle"] and self.start_point:
            x, y = event.x, event.y
            end_point = Point(x, y)
            if self.drawing_mode == "line":
                shape = Line(self.start_point, end_point)
            elif self.drawing_mode == "rectangle":
                shape = Rectangle(self.start_point, end_point)
            shape_id = shape.draw(self.canvas, color=self.current_color, width=self.get_current_size())
            self.items.append((shape, shape_id))
            self.start_point = None
            self.canvas.delete("temp_shape")
       elif self.drawing_mode == "circle" and self.start_point:
           x, y = event.x, event.y
           radius = math.sqrt((x - self.start_point.x)**2 + (y - self.start_point.y)**2)
           circle = Circle(self.start_point, radius)
           circle_id = circle.draw(self.canvas, color=self.current_color, width=self.get_current_size())
           self.items.append((circle, circle_id))
           self.start_point = None
           self.canvas.delete("temp_circle")
       self.selected_item = None #сброс выделения элемента

    def delete_item_under_mouse(self,x,y):
        item = self.canvas.find_closest(x, y)[0]
        if item:
             for shape, item_id in self.items:
               if item_id == item:
                  self.canvas.delete(item)
                  self.items.remove((shape, item_id))
                  break
        
    def clear_canvas(self):
        """Очищает холст."""
        self.canvas.delete("all")
        self.items = []

if __name__ == "__main__":
    root = tk.Tk()
    editor = CanvasEditor(root)
    root.mainloop()
