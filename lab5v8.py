import math
import tkinter as tk
from tkinter import ttk, messagebox

class Gripper:
    """Модель схвата манипулятора."""
    def __init__(self, name, max_force=100.0):
        self.name = name
        self.max_force = max_force
        self.reset()
        
    def reset(self):
        self.opening = 100.0       # Текущее раскрытие клешней 
        self._force = 0.0          # Текущее развиваемое усилие
        self.target_state = "open" # Состояние: "open" (открыт) или "closed" (закрывается)
        
    @property
    def force(self):
        """Свойство для чтения текущего усилия."""
        return self._force
        
    @force.setter
    def force(self, value):
        """Свойство для установки усилия."""
        if not 0.0 <= value <= self.max_force:
            raise ValueError(f"Усилие должно быть в диапазоне 0...{self.max_force} Н")
        self._force = value

    def update_force_rate(self):
        """Скорость нарастания усилия при контакте."""
        return 20.0 # Базовая скорость изменения усилия, Н/с

    def step(self, dt=0.1):
        """Один шаг моделирования механики схвата."""
        speed = 40.0 * dt # Скорость движения губок, мм/с
        
        if self.target_state == "open":
            # Логика открытия схвата
            self._force = max(0.0, self._force - self.update_force_rate() * 5 * dt)
            if self._force == 0.0 and self.opening < 100.0:
                self.opening = min(100.0, self.opening + speed)
                
        elif self.target_state == "closed":
            # Робот пытается закрыть схват полностью (до 0 мм), если нет препятствий
            if self.opening > 0.0:
                self.opening = max(0.0, self.opening - speed)
                self._force = 0.0
                
    def __str__(self):
        """Строковое представление состояния схвата."""
        return f"{self.name}: Раскрытие={self.opening:.1f} мм, Усилие={self._force:.1f} Н"


class ParallelGripper(Gripper):
    """Параллельный схват: учитывает размер детали и жесткость захвата."""
    def __init__(self, name, item_size=40.0, max_force=100.0):
        super().__init__(name, max_force)
        self.item_size = item_size # Размер зажимаемой детали, мм
        self.target_force = 0.0    # Какое усилие задал пользователь на ползунке
        
    def update_force_rate(self):
        """Переопределенный метод: зажим происходит быстрее (Полиморфизм)."""
        return super().update_force_rate() * 2.5 # Увеличенная скорость нарастания силы
        
    def step(self, dt=0.1):
        """Переопределенный шаг моделирования с учетом детали (Полиморфизм)."""
        speed = 40.0 * dt
        
        if self.target_state == "open":
            # Логика открытия 
            if self._force > 0.0:
                self._force = max(0.0, self._force - self.update_force_rate() * 4 * dt)
            else:
                self.opening = min(100.0, self.opening + speed)
                
        elif self.target_state == "closed":
            # Логика закрытия: клешни едут до тех пор, пока не упрутся в размер детали
            if self.opening > self.item_size:
                self.opening = max(self.item_size, self.opening - speed)
                self._force = 0.0
            else:
                # Губки уперлись в деталь — плавно увеличиваем усилие до целевого
                if self._force < self.target_force:
                    self._force = min(self.target_force, self._force + self.update_force_rate() * dt)


class GripperApp(tk.Tk):
    """Главное окно приложения управления схватом."""
    SCALE = 1.5 # Масштаб пикселей на 1 мм
    SIZE = 400  # Размер холста
    DT = 0.1    # Шаг моделирования, с
    
    def __init__(self, gripper):
        super().__init__()
        self.title("Управление схватом манипулятора")
        self.resizable(False, False)
        self.gripper = gripper
        self.running = False # Флаг активности процесса сжатия/разжатия
        self.info = tk.StringVar()
        self.force_var = tk.DoubleVar(value=0.0)
        self._build_widgets()
        self._redraw()
        self.after(int(self.DT * 1000), self._tick)
        
    def _build_widgets(self):
        # Создаем холст для визуализации
        self.canvas = tk.Canvas(self, width=self.SIZE, height=self.SIZE // 2, bg="white")
        self.canvas.grid(row=0, column=0, padx=5, pady=5)
        
        # Боковая панель управления
        panel = ttk.LabelFrame(self, text="Управление")
        panel.grid(row=0, column=1, sticky="n", padx=5, pady=5)
        
        ttk.Label(panel, text="Усилие зажима, Н:").pack(anchor="w")
        # Ползунок для регулировки силы
        ttk.Scale(panel, from_=0.0, to=self.gripper.max_force, variable=self.force_var, command=self._on_force_change).pack(fill="x", pady=3)
        
        # Кнопки управления состояниями схвата
        ttk.Button(panel, text="Захватить", command=self._grip).pack(fill="x", pady=2)
        ttk.Button(panel, text="Отпустить", command=self._release).pack(fill="x", pady=2)
        ttk.Button(panel, text="Сброс", command=self._reset).pack(fill="x", pady=2)
        
        # Наглядный индикатор текущего усилия (аналог Progressbar батареи из примера)
        ttk.Label(panel, text="Текущая нагрузка:").pack(anchor="w", pady=(8, 0))
        self.bar = ttk.Progressbar(panel, maximum=self.gripper.max_force, length=140)
        self.bar.pack(fill="x")
        
        # Нижняя информационная строка
        ttk.Label(self, textvariable=self.info).grid(row=1, column=0, columnspan=2)
        
    def _on_force_change(self, value):
        """Вызывается при движении ползунка."""
        try:
            val = float(value)
            # Если пользователь выставил опасную силу, выдаем предупреждение
            if val > 75.0:
                messagebox.showwarning("Внимание", "Высокое усилие зажима! Возможна деформация детали.")
            self.gripper.target_force = val
        except ValueError as err:
            messagebox.showerror("Ошибка", str(err))
            
    def _grip(self):
        """Переключает цель модели на сжатие клешни."""
        self.gripper.target_state = "closed"
        self.running = True
        
    def _release(self):
        """Переключает цель модели на раскрытие клешни."""
        self.gripper.target_state = "open"
        self.running = True
        
    def _reset(self):
        """Сброс симуляции к начальным настройкам."""
        self.running = False
        self.gripper.reset()
        self.force_var.set(0.0)
        self._redraw()
        
    def _tick(self):
        """Периодический таймер симуляции."""
        if self.running:
            self.gripper.step(self.DT)
            self._redraw()
            
        # Зацикливаем таймер after
        self.after(int(self.DT * 1000), self._tick)
        
    # отрисовка схемы на холсте
    def _redraw(self):
        cv, g = self.canvas, self.gripper
        cv.delete("all")
        
        mid_x = self.SIZE / 2
        mid_y = (self.SIZE // 2) / 2
        
        # Рисуем осевые линии для симметрии
        cv.create_line(0, mid_y, self.SIZE, mid_y, fill="#eee")
        cv.create_line(mid_x, 0, mid_x, self.SIZE // 2, fill="#eee")
        
        # Вычисляем положение губок в пикселях от центра холста
        half_open_px = (g.opening / 2) * self.SCALE
        
        # 1. Отрисовка зажимаемой детали (круг по центру)
        if isinstance(g, ParallelGripper):
            item_r = (g.item_size / 2) * self.SCALE
            cv.create_oval(mid_x - item_r, mid_y - item_r, mid_x + item_r, mid_y + item_r, fill="#ffaa00", outline="black")
            cv.create_text(mid_x, mid_y, text="Деталь", fill="black")
            
        # 2. Левая прижимная губка манипулятора
        left_x = mid_x - half_open_px
        cv.create_rectangle(left_x - 15, mid_y - 30, left_x, mid_y + 30, fill="#777", outline="black")
        cv.create_line(0, mid_y, left_x - 15, mid_y, width=6, fill="#aaa") # Тяга привода
        
        # 3. Правая прижимная губка манипулятора
        right_x = mid_x + half_open_px
        cv.create_rectangle(right_x, mid_y - 30, right_x + 15, mid_y + 30, fill="#777", outline="black")
        cv.create_line(right_x + 15, mid_y, self.SIZE, mid_y, width=6, fill="#aaa") # Тяга привода
        
        # Индикация усилия на самой полосе прогресса
        self.bar["value"] = g.force
        
        # Формируем строку состояния с использованием метода __str__
        self.info.set(f"{g} статус={g.target_state}")

def main():
    # Создаем параллельный схват для детали размером 40 мм и ограничением силы 100 Н
    gripper = ParallelGripper("Gripper-P8", item_size=40.0, max_force=100.0)
    app = GripperApp(gripper)
    app.mainloop()

if __name__ == "__main__":
    main()
