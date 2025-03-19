from tkinter import *
from tkinter import messagebox
from datetime import datetime, date

def delete1():
    new1.destroy()

def delete2():
    new2.destroy()

def view_all():
    global list2
    s = ''
    dt = datetime.now()
    for i in range(1, len(list2), 2):
        delta = dt - list2[i]
        if abs(delta.total_seconds()) < 60:
            status = "Прямо сейчас"
        elif delta.total_seconds() > 0:
            days = delta.days
            hours = delta.seconds // 3600
            status = f"Прошло: {days} дней, {hours} часов"
        else:
            future = abs(delta)
            days = future.days
            hours = future.seconds // 3600
            status = f"Осталось: {days} дней, {hours} часов"
        s += f'{list2[i - 1]}\n{list2[i].strftime("%d.%m.%Y %H:%M")}\n{status};\n\n'
    events.config(text=s, font='Arial 14')

def view_selected():
    global list2
    s = ''
    try:
        year_val = int(input_year.get())
    except ValueError:
        messagebox.showerror('Ошибка', 'Некорректный ввод года')
        return
    try:
        month_index = list_box.curselection()[0] + 1
    except IndexError:
        messagebox.showerror('Ошибка', 'Для начала выберите месяц')
        return
    dt = datetime.now()
    for i in range(1, len(list2), 2):
        event_dt = list2[i]
        if event_dt.month == month_index and event_dt.year == year_val:
            delta = dt - event_dt
            if abs(delta.total_seconds()) < 60:
                status = "Прямо сейчас"
            elif delta.total_seconds() > 0:
                days = delta.days
                hours = delta.seconds // 3600
                status = f"Прошло: {days} дней, {hours} часов"
            else:
                future = abs(delta)
                days = future.days
                hours = future.seconds // 3600
                status = f"Осталось: {days} дней, {hours} часов"
            s += f'{list2[i-1]}\n{event_dt.strftime("%d.%m.%Y %H:%M")}\n{status};\n\n'
    events.config(text=s if s else 'Событий не найдено', font='Arial 16')
    input_year.delete(0, END)

def add_event():
    n = name.get().strip()
    d = date1.get().strip()
    if not n:
        messagebox.showwarning('Ошибка', 'Заполните название события')
        return
    try:
        dt_obj = datetime.strptime(d, '%d.%m.%Y %H:%M')
    except ValueError:
        messagebox.showerror('Ошибка', 'Некорректный ввод даты и времени. Используйте формат: ДД.ММ.ГГГГ ЧЧ:ММ')
        return
    with open('event_list.txt', 'a', encoding='UTF-8') as file2:
        file2.write(f'\n{n},{d}')
    messagebox.showinfo('Событие', 'Событие успешно создано')
    name.delete(0, END)
    date1.delete(0, END)

def viewing_event():
    global new1, events, list_box, list2, input_year
    new1 = Toplevel()
    new1.geometry('600x650')
    new1.configure(bg='white')
    new1.title('Просмотр событий')
    events = Label(new1, font='Arial 16', bg='white')
    events.place(x=240, y=50)
    Label(new1, text='Введите год', bg='grey', fg='black', font='Arial 16').place(x=0, y=50)
    input_year = Entry(new1, bd=5, width=13, bg='#acdae8', fg='black', font='Arial 16')
    input_year.place(x=0, y=80)
    Label(new1, text='Выберите месяц', bg='gray', fg='black', font='Arial 16').place(x=0, y=130)
    list_box = Listbox(new1, selectmode=SINGLE, bd=5, width=13, height=12, bg='#acdae8', font='Arial 16')
    for month in ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']:
        list_box.insert(END, month)
    list_box.place(x=0, y=170)
    Button(new1, text='Просмотр событий по дате', font='Arial 12', command=view_selected).place(x=225, y=510)
    Button(new1, text='Просмотр всех событий', font='Arial 12', command=view_all).place(x=40, y=510)
    list2 = []
    try:
        with open('event_list.txt', 'r', encoding='UTF-8') as file1:
            for line in file1:
                try:
                    name, date_str = line.strip().split(',')
                    list2.append(name)
                    list2.append(datetime.strptime(date_str, '%d.%m.%Y %H:%M'))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    Button(new1, text='Закрыть', width=13, fg='red', font='Arial 16', command=delete1).place(x=5, y=600)

def create_event():
    global name, date1, new2
    new2 = Toplevel()
    new2.geometry('600x600')
    new2.title('Создание событий')
    Label(new2, text='Формат: ДД.ММ.ГГГГ ЧЧ:ММ', font='Arial 16', fg='red').pack(pady=10)
    Label(new2, text='Имя события', font='Arial 16').pack(pady=5)
    name = Entry(new2, font='Arial 16')
    name.pack(pady=5)
    Label(new2, text='Дата и время', font='Arial 16').pack(pady=5)
    date1 = Entry(new2, font='Arial 16')
    date1.pack(pady=5)
    Button(new2, text='Создать событие', font='Arial 16', fg='green', command=add_event).pack(pady=10)
    Button(new2, text='Закрыть', font='Arial 16', command=delete2).pack(pady=10)

window = Tk()
window.geometry('600x600')
window.title('Календарь событий')
Button(window, text='Создать событие', font='Arial 16', command=create_event).pack(pady=20)
Button(window, text='Просмотр событий', font='Arial 16', command=viewing_event).pack(pady=20)
window.mainloop()
