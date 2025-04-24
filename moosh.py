import psycopg2
import tkinter as tk
import atexit
from datetime import datetime

editingReady = False

conn = psycopg2.connect(database="moosh",
                        host="localhost",
                        user="postgres",
                        password="MintAndThyme!1!",
                        port="5432")

####Functions

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
    save_all_text_of_tasks(tables)

def taskCallback():
      print("1")
#       get_all_text_of_tasks(tables)
      return True
jarCols = ["id","variety ","date_innoculated","shake_date","bulk_date","bulk_id","grain"]
def jarCallback(id,place,value):
      if editingReady:
       #       print(id)
       # #       get_all_text_of_tasks(tables)
       #       print(place)
       print(f'val: {value}, id: {id}, place: {place}')
       #       sql = f"UPDATE jars SET {jarCols[place]} = %P"
       tempCursor = conn.cursor()
      else:
          return True
      return True
bulkCols = ["id","variety ","container_type","bulk_date","flush_ids"]
def bulkCallback(id,place,value):
      if editingReady:
       #       print(id)
       # #       get_all_text_of_tasks(tables)
       #       print(place)
       print(f'val: {value}, id: {id}, place: {place}')
       #       sql = f"UPDATE jars SET {jarCols[place]} = %P"
       tempCursor = conn.cursor()
      else:
          return True
      return True

# def main():
### Initialize Tkinter
root = tk.Tk()
sv = tk.StringVar()

frm = tk.Frame(master=root)


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

now = datetime.now().time()

timing = int(now.hour/6)

greeting = tk.Label(
       text=f"Good {greetingTime[timing]} Exi!",
       font=("Arial", 50),
       fg="steelblue",
)

### Fill tables
#### JARS
tableCount = 2
tableNames = ["jars", "bulk"]

for i in range(tableCount):
    sql = f"SELECT * from {tableNames[i]}"
    cursor.execute(sql)
    colnames = [desc[0] for desc in cursor.description]
    res = cursor.fetchall()
    titles = tk.Frame(master=tables)
    cnt = 0
    for col in colnames:
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
    bulk = tk.Frame(master=tables)
    linecnt = 0
    for line in res:
        print(line)
        frm_tmp_bulk = tk.Frame(master=bulk)
        cnt = 0
        for txt in line:
                print(txt)
                vcmd = root.register(bulkCallback)
                e =tk.Entry(master=frm_tmp_bulk,validate="key",validatecommand=(vcmd, line[0], cnt, "%P"),width=20)
                if txt != None:
                    e.insert(0,txt)
                else:
                    e.insert(0, "None")
                e._id = line[0]
                e.grid(row = 0, column=cnt) #left
                cnt = cnt + 1
        frm_tmp_bulk.grid()
        lincnt = linecnt+1
    bulk.grid(sticky = tk.W)


# sql = "SELECT * from jars"
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
# jars = tk.Frame(master=tables)
# linecnt = 0
# for line in res:
#        frm_tmp = tk.Frame(master=jars)
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
# jars.grid()
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

### Begin program
print("Breakpoint")
root.title('Moosh')
root.geometry("1000x800")
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



