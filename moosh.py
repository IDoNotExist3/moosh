import psycopg2
import tkinter as tk
import atexit
# from datetime import datetime
import datetime
from tkcalendar import Calendar
from moosh_calendary import MooshEvents
# from jsonify import jsonify
 
from flask import Flask, jsonify

###Global Values
tableCount = 3
editingReady = False
editedEntries = [{} for j in range(tableCount)]
tableNames = ["spawn", "bulk", "flush"]
print(editedEntries)
SPAWN = 0
BULK = 1
FLUSH = 2

columnCounts = [0,0,0,0,0,0]

bulkCols = ["id","variety","container_type","bulk_date","flush_ids","p-value"]
jarCols = ["id","variety","date_innoculated","shake_date","bulk_date","bulk_id","grain","p-value"]
flushCols = ["id", "variety", "flush_order", "harvest_date", "weight_grams", "bulk_id", "p-value"]

###Initial initializations

conn = psycopg2.connect(database="moosh",
                        host="localhost",
                        user="postgres",
                        password="MintAndThyme!1!",
                        port="5432")



####Functions
class TkinterCalendar(Calendar):

    def formatmonth(self, master, year, month):

        dates = self.monthdatescalendar(year, month)

        frame = tk.Frame(master)

        self.labels = []

        for r, week in enumerate(dates):
            labels_row = []
            for c, date in enumerate(week):
                label = tk.Button(frame, text=date.strftime('%Y\n%m\n%d'))
                label.grid(row=r, column=c)

                if date.month != month:
                    label['bg'] = '#aaa'

                if c == 6:
                    label['fg'] = 'red'

                labels_row.append(label)
            self.labels.append(labels_row)

        return frame

def get_all_text_of_tasks(parent_widget):
    print("printing children")
    children_widgets = parent_widget.winfo_children()
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            print("This is an entry")
            children_widgets2 = child_widget.winfo_children()
            for child_widget2 in children_widgets2:
                if child_widget.winfo_class() == 'Entry':
                    print(child_widget.get())
        elif child_widget.winfo_class() == 'Label':
            print()
        elif child_widget.winfo_class() == 'Frame':
            children_widgets2 = child_widget.winfo_children()
       #      print(children_widgets2)
       #      for child_widget2 in children_widgets2:
       #          if child_widget2.winfo_class() == 'Entry':
       #              print(child_widget2.get())

def save_all_text_of_tasks(parent_widget):
#     print("printing children")
    children_widgets = parent_widget.winfo_children()
    # print(len(children_widgets))
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            print("This is an entry")
            children_widgets2 = child_widget.winfo_children()
            for child_widget2 in children_widgets2:
                if child_widget.winfo_class() == 'Entry':
                    print(child_widget.get())
        elif child_widget.winfo_class() == 'Label':
            # print(child_widget.text)
            print()
        elif child_widget.winfo_class() == 'Frame':
            # print("This is frame")
            children_widgets2 = child_widget.winfo_children()
       #      print(children_widgets2)
            for child_widget2 in children_widgets2:
                if child_widget2.winfo_class() == 'Entry':
                    print(child_widget2.get())
                # elif child_widget2.winfo_class() == 'Label':
                #     # print("Another label...")  

def save():
    # save_all_text_of_tasks(tables)
    
    tempCursor = conn.cursor()
    
    for table, name in zip(editedEntries, tableNames):
        dicti = table.items()
        for entry in dicti:
            split = entry[0].split(",")
            print(f"Identifier split is {split}")
            sql = f"UPDATE {name} SET {(jarCols[int(split[1])])} = '{entry[1]}' WHERE id = {split[0]}"
            print(sql)
            tempCursor.execute(sql)

            #####TESTING
            # sqlRollback = "ROLLBACK"
            # tempCursor.execute(sqlRollback)
            conn.commit()

def addEntry(type):
    global columnCounts
    if type == "spawn":
        print("Jar Update")
        e =tk.Entry(master=tableFrames[0],validate="key",width=20)
        e.grid(row = columnCounts[0], column=0)
        columnCounts[0] = columnCounts[0] + 1
    elif type == "bulk":
        print("Bulk Update")
    elif type == "flush":
        print("Flush Updates")
        e =tk.Entry(master=tableFrames[2],validate="key",width=20)
        e.grid(row = columnCounts[2]+2, column=0)
        columnCounts[2] = columnCounts[2] + 1
    else:
        print("Unkown update")
    # print("Entrying")
    root.update()

def taskCallback():
      print("1")
#       get_all_text_of_tasks(tables)
      return True
def jarCallback(id,place,value):
      if editingReady:
       #       print(id)
       # #       get_all_text_of_tasks(tables)
       #       print(place)
       print(f'val: {value}, id: {id}, place: {place}')
       sql = f"UPDATE spawn SET {(jarCols[int(place)])} = {value}"
       print(sql)
    #    tempCursor = conn.cursor()
       editedEntries[SPAWN].update({f"{id},{place}": f"{value}"})
      else:
          return True
      return True

def bulkCallback(id,place,value):
      if editingReady:
       #       print(id)
       # #       get_all_text_of_tasks(tables)
       #       print(place)
       print(f'val: {value}, id: {id}, place: {place}')
       #       sql = f"UPDATE spawn SET {jarCols[int(place)]} = {value}"
       sql = f"UPDATE bulk SET {bulkCols[int(place)]} = {value}"
    #    editedEntries[BULK].append(id)
       editedEntries[BULK].update({f"{id},{place}": f"{value}"})
      else:
          return True
      return True

def flushCallback(id,place,value):
      if editingReady:
       #       print(id)
       # #       get_all_text_of_tasks(tables)
       #       print(place)
       print(f'val: {value}, id: {id}, place: {place}')
       #       sql = f"UPDATE spawn SET {jarCols[int(place)]} = {value}"
       sql = f"UPDATE flush SET {flushCols[int(place)]} = {value}"
    #    editedEntries[BULK].append(id)
       editedEntries[FLUSH].update({f"{id},{place}": f"{value}"})
      else:
          return True
      return True

# def main():
### Initialize Tkinter



root = tk.Tk()


sv = tk.StringVar()

frm = tk.Frame(master=root)

cal_frame = tk.Frame(master=root)

''' calendar shit
class MyCalendar(Calendar):

    def _next_month(self):
        Calendar._next_month(self)
        self.event_generate('<<CalendarMonthChanged>>')

    def _prev_month(self):
        Calendar._prev_month(self)
        self.event_generate('<<CalendarMonthChanged>>')

    def _next_year(self):
        Calendar._next_year(self)
        self.event_generate('<<CalendarMonthChanged>>')

    def _prev_year(self):
        Calendar._prev_year(self)
        self.event_generate('<<CalendarMonthChanged>>')

    def get_displayed_month_year(self):
        return self._date.month, self._date.year


def on_change_month(event):
    # remove previously displayed events
    cal.calevent_remove('all')
    year, month = cal.get_displayed_month_year()
    # display the current month events 
    # ...
    print(year, month)

cal = MyCalendar(cal_frame)
cal.pack()

cal.bind('<<CalendarMonthChanged>>', on_change_month)
'''
cal = Calendar(master=cal_frame, font = "Arial 20", locale='en_US', selectmode = 'day', year = 2025, month = 5, day = 1)
cal.calevent_create(datetime.datetime.today().date(), "AHHH", tags=["jar"])
cal.grid()





######TESTING
menubar = tk.Menu(root)
menubar.add_command(label="Save", command=save, font=("Arial", 20))
# menubar.add_command(label="Quit!", command=Hello)
root.config(menu=menubar)

#####END TESTING

###Frames
tables = tk.Frame(master=root,relief=tk.RIDGE,borderwidth=5)

### Initalize postgreSQL cursor
cursor = conn.cursor()


### Greeting
greetingTime = ["Night", "Morning", "Afternoon", "Evening"]

now = datetime.datetime.now().time()

timing = int(now.hour/6)

greeting = tk.Label(
       text=f"Good {greetingTime[timing]} Exi!",
       font=("Arial", 50),
       fg="steelblue",
)

### Fill tables
#### SPAWN
tableCount = 3
tableNames = ["spawn", "bulk", "flush"]
vcmdBulk = root.register(bulkCallback)
vcmdSpawn = root.register(jarCallback)
vcmdFlush = root.register(flushCallback)
callbacks = [vcmdSpawn,vcmdBulk,vcmdFlush]
tableFrames = []
for i in range(tableCount): ### Do spawn and bulk tables
    bulk = tk.Frame(master=tables, width = 1000)
    title = tk.Label(master=bulk, text=tableNames[i], font=("Arial",20)).grid(sticky=tk.W)
    sql = f"SELECT * from {tableNames[i]} ORDER BY id" ###Grabbing everything from table
    cursor.execute(sql)
    colnames = [desc[0] for desc in cursor.description]
    res = cursor.fetchall()
    titles = tk.Frame(master=bulk)
    cnt = 0
    for col in colnames: ###Column names
        text = tk.StringVar()
        text.set(col)
        tk.Label(
                text = col,
                master=titles,
                width=20,
        ).grid(row=0, column=cnt) #was left
        cnt = cnt+1
        # tk.Entry(master=jar_titles,textvariable=text,validate="focusout",width=20).pack(side=tk.LEFT)
    titles.grid(sticky = tk.W)
    
    linecnt = 0
    inno_date_saved = None
    for line in res: ###Looping through each line of data
        columnCounts[i] = columnCounts[i] + 1
        print(line)
        frm_tmp_bulk = tk.Frame(master=bulk)
        cnt = 0
        for txt in line:
                print(txt)
                # vcmd = root.register(callbacks[i])
                e =tk.Entry(master=frm_tmp_bulk,validate="key",validatecommand=(callbacks[i], line[0], cnt, "%P"),width=20)
                if tableNames[i] == "spawn" and (colnames[cnt] == "bulk_date" or colnames[cnt] == "date_innoculated"):
                    if colnames[cnt] == "date_innoculated": ## Save inno date for potential prediction
                        inno_date_saved = txt
                        if txt != None:
                            e.insert(0,txt)
                        else:
                            e.insert(0, "None")
                    elif colnames[cnt] == "bulk_date" and txt == None: ## Want to predict bulk date
                        # temp_date = datetime.datetime.strptime(inno_date_saved, '%Y-%m-%d').date()
                        # temp_date = temp_date + datetime.timedelta(days=14)
                        temp_date = (inno_date_saved + datetime.timedelta(days=14)).strftime('%Y-%m-%d') ###Add 14 days to date and convert to string
                        e.insert(0, "(Est) " + temp_date)
                    else:
                        if txt != None:
                            e.insert(0,txt)
                        else:
                            e.insert(0, "None")
                else:
                    if txt != None:
                        e.insert(0,txt)
                    else:
                        e.insert(0, "None")
                e._id = line[0]
                e.grid(row = 0, column=cnt) #left
                cnt = cnt + 1
        frm_tmp_bulk.grid()
        lincnt = linecnt+1
    addEntries = tk.Button(bulk, text = "Add Entry", command = lambda: addEntry(tableNames[i]))
    addEntries.grid(sticky = tk.W)
    bulk.grid(sticky = tk.W, pady=20)
    tableFrames.append(bulk)


# sql = "SELECT * from spawn"
# cursor.execute(sql)
# colnames = [desc[0] for desc in cursor.description]
# res = cursor.fetchall()
# jar_titles = tk.Frame(master=tables)
# cnt = 0
# for col in colnames:
#     text = tk.StringVar()
#     text.set(col)
#     tk.Label(
#             text = col,
#             master=jar_titles,
#             width=20,
#     ).grid(row=0, column=cnt)
#     cnt = cnt+1
#     # tk.Entry(master=jar_titles,textvariable=text,validate="focusout",width=20).pack(side=tk.LEFT)
# jar_titles.grid()
# spawn = tk.Frame(master=tables)
# linecnt = 0
# for line in res:
#        frm_tmp = tk.Frame(master=spawn)
#        cnt = 0
#        for txt in line:
#               vcmd = root.register(jarCallback)
#               e =tk.Entry(master=frm_tmp,validate="key",validatecommand=(vcmd, line[0], cnt, "%P"),width=20)

#               if txt != None:
#                 e.insert(0,txt)
#               else:
#                 e.insert(0, "None")
#               e._id = line[0]
#               e.grid(row = linecnt, column=cnt)
#               cnt = cnt + 1
#        frm_tmp.grid(row = linecnt)
#        linecnt = linecnt + 1
# spawn.grid()
# #### Bulk
# sql = "SELECT * from bulk"
# cursor.execute(sql)
# colnames = [desc[0] for desc in cursor.description]
# res = cursor.fetchall()
# bulk_titles = tk.Frame(master=tables)
# for col in colnames:
#        text = tk.StringVar()
#        text.set(col)
#        tk.Label(
#               text = col,
#               master=bulk_titles,
#               width=20,
#        ).grid() #was left
#        # tk.Entry(master=jar_titles,textvariable=text,validate="focusout",width=20).pack(side=tk.LEFT)
# bulk_titles.grid()
# bulk = tk.Frame(master=tables)
# for line in res:
#        print(line)
#        frm_tmp_bulk = tk.Frame(master=bulk)
#        cnt = 0
#        for txt in line:
#               print(txt)
#               vcmd = root.register(bulkCallback)
#               e =tk.Entry(master=frm_tmp_bulk,validate="key",validatecommand=(vcmd, line[0], cnt, "%P"),width=20)
#               if txt != None:
#                 e.insert(0,txt)
#               else:
#                 e.insert(0, "None")
#               e._id = line[0]
#               e.grid() #left
#               cnt = cnt + 1
#        frm_tmp_bulk.grid()
# bulk.grid()

editingReady = True
###Packing
greeting.grid(row=0)

tables.grid(row=1)
frm.grid()
cal_frame.grid()

###
today = datetime.datetime.now(datetime.timezone.utc).astimezone()
mooshCal = MooshEvents()
dict = mooshCal.get_upcoming_as_dict()
# mooshCal.add_event("TestTestTest", today, today)

print(dict)
# print(dict[0])
# jsonify(dict)

# canvas = tk.Canvas(
#     root, scrollregion = "0 0 2000 1000", width = 400, height = 400)
# canvas.grid(row = 0, column = 0, sticky = tk.NSEW)

# scroll = tk.Scrollbar(tableFrames, orient = tk.VERTICAL, command = canvas.yview)
# scroll.grid(row = 0, column = 1, sticky = tk.NS)
# canvas.config(yscrollcommand = scroll.set)
# item = canvas.create_window(( 2, 2 ), anchor = tk.NW,  window = tableFrames )

### Begin program
print("Breakpoint")
root.title('Moosh')
root.geometry("1200x1200")
root.mainloop()



       

def exit_handler():
#     get_all_text_of_tasks(tables)
    print ('I am dying')
    
    # for line in dailies:
    #     print(line)



atexit.register(exit_handler)


       ### Packing





# if __name__ == '__main__':
#     main()



