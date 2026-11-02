## МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ

## ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ

«Омский государственный технический университет»

Кафедра «Автоматизация и робототехника»

Отчет

По дисциплине «Программирование на языке Python»

Лабораторная работа №5

Вариант 8

Выполнил: Студент группы УТС-251т Дмитриева Д.Ю.

Проверил: Доц., К.н. Ситников Д.В.


## Цель работы

Изучение основ объектно-ориентированного программирования в

Python (классы, инкапсуляция, наследование, полиморфизм) и получение практических навыков разработки настольного приложения с графическим интерфейсом на библиотеке Tkinter для моделирования и контроля мехатронного объекта.

## Задание

Вариант 8 Схват манипулятора. Классы: Gripper (усилие, степень

раскрытия), ParallelGripper и VacuumGripper (разная логика захвата). Окно: выбор типа схвата, ползунок усилия, кнопки «Захватить/Отпустить», Canvas с изображением схвата и детали; при превышении допустимого усилия — предупреждение.

## Диаграмма классов

*Рисунок 1 – Диаграмма классов*


Детальная спецификация элементов классов

## 1. Базовый класс Gripper

Описывает общие параметры и поведение зажимного механизма.

Параметры конструктора (__init__):

- name (str) – 8<O 8;8 <0@:0 CAB@>9AB20.

- max_force (float, ?> C<>;G0=8N 100.0) ‑ :>=AB@C:B82=K9 ?@545; прочности механизма.

Внутренние атрибуты состояния (Поля класса):

- self.name (str) — A>E@0=Q==>5 8<O CAB@>9AB20.

- self.max_force (float) ‐ A>E@0=Q==K9 ;8<8B CA8;8O.

- self.opening (float) ‐ B5:CI55 @0AAB>O=85 <564C 7068<=K<8 губками.

- self._force (float) — B5:CI55 @0728205<>5 CA8;85.

- self.target_state (str) — @568< @01>BK <5E0=8:8: "open" (раскрытие) или "closed" (сжатие).

Контролируемые свойства (@property):

- @property def force(self) ‒ 35BB5@, 2>72@0I05B B5:CI55 CA8;85 _force.

- @force.setter def force(self, value) ‒ A5BB5@, ?@>25@O5B, ;568B ;8 передаваемое значение в диапазоне от 0.0 до max_force. При ошибке выбрасывает исключение ValueError.

Методы класса:

- def reset(self) – 2>72@0I05B <5E0=87< 2 8AE>4=>5 A>AB>O=85.

- def update_force_rate(self) - 2>72@0I05B 107>2CN A:>@>ABL изменения усилия.

- def step(self, dt=0.1) - A8<C;8@C5B >48= H03 87<5=5=8O A>AB>O=8O за время dt. Описывает холостой ход губок (без препятствий).

- def __str__(self) - D>@<8@C5B B5:AB>2>5 >?8A0=85 >1J5:B0 4;O вывода пользователю.

- 2. Класс-потомок ParallelGripper (Модель параллельного схвата с деталью)


Расширяет базовый класс, добавляя алгоритм физического

взаимодействия губок с твёрдой деталью.

Параметры конструктора (__init__):

- name (str) – 8<O CAB@>9AB20.

- item_size (float, ?> C<>;G0=8N 40.0) ‒ D878G5A:89 @07<5@ зажимаемой детали в мм.

- max_force (float, ?> C<>;G0=8N 100.0) ‐ ;8<8B CA8;8O.

Новые атрибуты состояния:

- self.item_size (float) – 70D8:A8@>20==K9 @07<5@ 45B0;8.

- self.target_force (float) - 65;05<>5 CA8;85, :>B>@>5 2K1@0; пользователь на ползунке интерфейса.

Переопределённые методы (Полиморфизм):

- def update_force_rate(self) - C25;8G8205B 107>2CN A:>@>ABL нарастания силы, возвращая значение родительского класса, умноженное на коэффициент: super().update_force_rate() * 2.5.

- def step(self, dt=0.1) — 87<5=O5B D878:C H030. —A;8 3C1:8 ?@8 закрытии упираются в размер item_size, их движение блокируется, а внутреннее усилие _force начинает расти до значения target_force.

- 3. Класс интерфейса GripperApp (Графическое окно приложения)

Наследует свойства базового окна tk.Tk. Отвечает за генерацию

виджетов, обработку нажатий и визуализацию.

Константы класса (Параметры среды):

- SCALE = 1.5 ‒ <0AHB01 3@0D8:8 (A:>;L:> ?8:A5;59 E>;AB0 занимает 1 мм модели).

- SIZE = 400 — H8@8=0 :204@0B=>3> E>;AB0.

- DT = 0.1 — H03 B09<5@0 >1=>2;5=8O 2 A5:C=40E.

Связи и управляющие переменные:

- self.gripper ‐ ?@O<0O AAK;:0 =0 0AA>F88@>20==K9 >1J5:B <>45;8 (ParallelGripper).


- self.running (bool) - D;03, @07@5H0NI89 8;8 70?@5I0NI89 расчёт физики в текущий момент времени.

- self.info (tk.StringVar) – @50:B82=0O AB@>:0 Tkinter 4;O B5:AB>2>3> вывода состояния.

- self.force_var (tk.DoubleVar) ‒ @50:B82=>5 G8A;> Tkinter, связанное с положением ползунка.

Графические компоненты (Виджеты):

- self.canvas (tk.Canvas) - E>;AB 4;O @8A>20=8O AE20B0.

- self.bar (ttk.Progressbar) ‑ ?>;>A0 >B>1@065=8O =03@C7:8.

Функции и методы обработки событий:

- def _build_widgets(self) ‑ A>740QB, :>=D83C@8@C5B 8 @07<5I05B элементы управления на экране.

- def _on_force_change(self, value) ‒ A@010BK205B ?@8 42865=88 ползунка. Безопасно передаёт число в модель через try/except. Если value > 75.0, прерывает выполнение и выводит диалоговое окно messagebox.showwarning.

- def _grip(self) ‐ 0:B828@C5B @568< 7060B8O (target_state = "closed", running = True).

- def _release(self) ‑ 0:B828@C5B @568< @0A:@KB8O (target_state = "open", running = True).

- def _reset(self) – >AB0=02;8205B ?@>F5AA, A1@0AK205B 8=B5@D59A 8 модель к заводским нулям.

- def _tick(self) – D>=>2K9 =51;>:8@CNI89 B09<5@.  07 2 100 вызывает симуляцию шага модели self.gripper.step(self.DT), метод перерисовки графики и перезапускает сам себя через метод .after().

- def _redraw(self) - AB8@05B AB0@K5 >1J5:BK =0 E>;AB5 8 @8AC5B новые геометрические фигуры, привязывая их координаты к текущему значению self.gripper.opening.


## Макет окна приложения и перечень используемых виджетов

*Рисунок 1 – Макет окна приложения*

Используемые виджеты:

- 1. tk.Tk (Главное окно)

Главный виджет, холст всего приложения, внутри которой размещаются все остальные элементы.

- 2. ttk.Label (Текстовая метка / Надпись)

Текст на экране, который используется для вывода подсказок/надписей или для динамического показа меняющейся информации (строка состояния схвата в самом низу окна).

- 3. ttk.Button (Кнопка)

Нажимаемая кнопка, которая привязывает клик мыши к выполнению конкретной функции в коде.

- 4. ttk.Scale (Ползунок / Шкала регулировки)

Линейка с бегунком, который можно двигать мышкой, подходит для плавного ввода числовых параметров в диапазоне.

- 5. ttk.Progressbar (Индикатор выполнения / Полоса загрузки)

Графическая полоса, которая заполняется цветом. Наглядно показывает уровень какого-либо параметра. В выполненной работе - реальное текущее усилие, с которым клешня давит на деталь.

- 6. tk.Canvas (Графический холст)


Зона для рисования двумерной графики. Позволяет с помощью кода рисовать геометрические фигуры.

## 7. ttk.LabelFrame (Рамка с заголовком)

Визуальный блок с тонкой линией по периметру и надписью сверху. Служит для группировки других виджетов. Мы объединили в рамку «Управление» ползунок и кнопки, чтобы интерфейс выглядел структурированно.

## Листинг программы

```
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
self.opening = 100.0 # Текущее раскрытие клешней
self._force = 0.0 # Текущее развиваемое усилие
self.target_state = "open" # Состояние: "open" (открыт) или "closed"
(закрывается)
@property
def force(self):
"""Свойство для чтения текущего усилия."""
return self._force
@force.setter
def force(self, value):
"""Свойство для установки усилия."""
if not 0.0 <= value <= self.max_force:
raise ValueError(f"Усилие должно быть в диапазоне
0...{self.max_force} Н")
self._force = value
def update_force_rate(self):
"""Скорость нарастания усилия при контакте."""
return 20.0 # Базовая скорость изменения усилия, Н/с
def step(self, dt=0.1):
"""Один шаг моделирования механики схвата."""
speed = 40.0 * dt # Скорость движения губок, мм/с
if self.target_state == "open":
# Логика открытия схвата
self._force = max(0.0, self._force - self.update_force_rate() * 5
* dt)
if self._force == 0.0 and self.opening < 100.0:
self.opening = min(100.0, self.opening + speed)
elif self.target_state == "closed":
# Робот пытается закрыть схват полностью (до 0 мм), если нет
препятствий
if self.opening > 0.0:
```


```
self.opening = max(0.0, self.opening - speed)
self._force = 0.0
def __str__(self):
"""Строковое представление состояния схвата."""
return f"{self.name}: Раскрытие={self.opening:.1f} мм,
Усилие={self._force:.1f} Н"
class ParallelGripper(Gripper):
"""Параллельный схват: учитывает размер детали и жесткость захвата."""
def __init__(self, name, item_size=40.0, max_force=100.0):
super().__init__(name, max_force)
self.item_size = item_size # Размер зажимаемой детали, мм
self.target_force = 0.0 # Какое усилие задал пользователь на
ползунке
def update_force_rate(self):
"""Переопределенный метод: зажим происходит быстрее (Полиморфизм)."""
return super().update_force_rate() * 2.5 # Увеличенная скорость
нарастания силы
def step(self, dt=0.1):
"""Переопределенный шаг моделирования с учетом детали
(Полиморфизм)."""
speed = 40.0 * dt
if self.target_state == "open":
# Логика открытия
if self._force > 0.0:
self._force = max(0.0, self._force - self.update_force_rate()
* 4 * dt)
else:
self.opening = min(100.0, self.opening + speed)
elif self.target_state == "closed":
# Логика закрытия: клешни едут до тех пор, пока не упрутся в
размер детали
if self.opening > self.item_size:
self.opening = max(self.item_size, self.opening - speed)
self._force = 0.0
else:
# Губки уперлись в деталь — плавно увеличиваем усилие до
целевого
if self._force < self.target_force:
self._force = min(self.target_force, self._force +
self.update_force_rate() * dt)
class GripperApp(tk.Tk):
"""Главное окно приложения управления схватом."""
SCALE = 1.5 # Масштаб пикселей на 1 мм
SIZE = 400 # Размер холста
DT = 0.1 # Шаг моделирования, с
def __init__(self, gripper):
super().__init__()
self.title("Управление схватом манипулятора")
self.resizable(False, False)
self.gripper = gripper
self.running = False # Флаг активности процесса сжатия/разжатия
self.info = tk.StringVar()
self.force_var = tk.DoubleVar(value=0.0)
self._build_widgets()
```


```
self._redraw()
self.after(int(self.DT * 1000), self._tick)
def _build_widgets(self):
# Создаем холст для визуализации
self.canvas = tk.Canvas(self, width=self.SIZE, height=self.SIZE // 2,
bg="white")
self.canvas.grid(row=0, column=0, padx=5, pady=5)
# Боковая панель управления
panel = ttk.LabelFrame(self, text="Управление")
panel.grid(row=0, column=1, sticky="n", padx=5, pady=5)
ttk.Label(panel, text="Усилие зажима, Н:").pack(anchor="w")
# Ползунок для регулировки силы
ttk.Scale(panel, from_=0.0, to=self.gripper.max_force,
variable=self.force_var, command=self._on_force_change).pack(fill="x",
pady=3)
# Кнопки управления состояниями схвата
ttk.Button(panel, text="Захватить",
command=self._grip).pack(fill="x", pady=2)
ttk.Button(panel, text="Отпустить",
command=self._release).pack(fill="x", pady=2)
ttk.Button(panel, text="Сброс", command=self._reset).pack(fill="x",
pady=2)
# Наглядный индикатор текущего усилия (аналог Progressbar батареи из
примера)
ttk.Label(panel, text="Текущая нагрузка:").pack(anchor="w", pady=(8,
0))
self.bar = ttk.Progressbar(panel, maximum=self.gripper.max_force,
length=140)
self.bar.pack(fill="x")
# Нижняя информационная строка
ttk.Label(self, textvariable=self.info).grid(row=1, column=0,
columnspan=2)
def _on_force_change(self, value):
"""Вызывается при движении ползунка."""
try:
val = float(value)
# Если пользователь выставил опасную силу, выдаем предупреждение
if val > 75.0:
messagebox.showwarning("Внимание", "Высокое усилие зажима!
Возможна деформация детали.")
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
```


```
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
cv.create_oval(mid_x - item_r, mid_y - item_r, mid_x + item_r,
mid_y + item_r, fill="#ffaa00", outline="black")
cv.create_text(mid_x, mid_y, text="Деталь", fill="black")
# 2. Левая прижимная губка манипулятора
left_x = mid_x - half_open_px
cv.create_rectangle(left_x - 15, mid_y - 30, left_x, mid_y + 30,
fill="#777", outline="black")
cv.create_line(0, mid_y, left_x - 15, mid_y, width=6, fill="#aaa") #
Тяга привода
# 3. Правая прижимная губка манипулятора
right_x = mid_x + half_open_px
cv.create_rectangle(right_x, mid_y - 30, right_x + 15, mid_y + 30,
fill="#777", outline="black")
cv.create_line(right_x + 15, mid_y, self.SIZE, mid_y, width=6,
fill="#aaa") # Тяга привода
# Индикация усилия на самой полосе прогресса
self.bar["value"] = g.force
# Формируем строку состояния с использованием метода __str__
self.info.set(f"{g} статус={g.target_state}")
def main():
# Создаем параллельный схват для детали размером 40 мм и ограничением
силы 100 Н
gripper = ParallelGripper("Gripper-P8", item_size=40.0, max_force=100.0)
app = GripperApp(gripper)
app.mainloop()
if __name__ == "__main__":
main()
```


## Результаты работы

*Рисунок 2 – Штатный зажим детали*

При установке силы 50.0 Н на ползунке и нажатии кнопки «Захватить»,

губки плавно сближаются со 100.0 мм до 40.0 мм. Достигнув физического контакта, губки останавливаются, а значение текущей силы зажима на индикаторе возрастает до уставки 50.0 Н.

*Рисунок 3 - Граничный сценарий*


При перемещении ползунка выше безопасной отметки 75.0 Н

срабатывает встроенный обработчик и на экран выводится предупреждающее диалоговое окно с сообщением: «Высокое усилие зажима! Возможна деформация детали».

## Вывод

В ходе выполнения лабораторной работы были успешно освоены

ключевые концепции объектно-ориентированного программирования (ООП) на языке Python:

Инкапсуляция продемонстрирована через сокрытие внутреннего поля

усилия _force и использование свойств @property с декоратором @force.setter для проверки корректности входящих данных.

Наследование реализовано при создании специализированного класса

ParallelGripper от базового класса Gripper с явным вызовом родительского конструктора через функцию super().__init__().

Полиморфизм осуществлен путем полного переопределения методов

step() и update_force_rate() в классе-потомке, что позволило кардинально изменить физическую модель поведения при соприкосновении с объектом манипулирования.

Разработано устойчивое графическое приложение на базе библиотеки

Tkinter, эффективно использующее неблокирующие таймеры периодического обновления состояния .after() вместо недопустимого циклического использования time.sleep(). Логика симуляции полностью отделена от оконного интерфейса, что соответствует принципам модульного проектирования программного обеспечения.
