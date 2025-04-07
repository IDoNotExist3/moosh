import psycopg2
import tkinter as tk
import atexit
from datetime import datetime

conn = psycopg2.connect(database="moosh",
                        host="localhost",
                        user="postgres",
                        password="MintAndThyme!1!",
                        port="5432")

####Functions
def taskCallback():
      print("1")

def main():
       ### Initialize Tkinter
       root = tk.Tk()
       sv = tk.StringVar()

       frm = tk.Frame(master=root)


       ######TESTING
       def hello():   #Hello! menu
              print("hello!")
       def Hello():   #Quit! menu
              print("Hello!")
       # create a toplevel menu
       menubar = tk.Menu(root)
       menubar.add_command(label="Hello!", command=hello)
       menubar.add_command(label="Quit!", command=Hello)
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
       sql = "SELECT * from jars"
       cursor.execute(sql)
       colnames = [desc[0] for desc in cursor.description]
       res = cursor.fetchall()
       jar_titles = tk.Frame(master=tables)
       for col in colnames:
              text = tk.StringVar()
              text.set(col)
              tk.Label(
                    text = col,
                    master=jar_titles,
                    width=20,
              ).pack(side=tk.LEFT)
              # tk.Entry(master=jar_titles,textvariable=text,validate="focusout",width=20).pack(side=tk.LEFT)
       jar_titles.pack()
       for line in res:
              frm_tmp = tk.Frame(master=tables)
              cnt = 0
              for txt in line:
                     text = tk.StringVar()
                     text.set(txt)
                     e =tk.Entry(master=frm_tmp,textvariable=text,validate="key",validatecommand=taskCallback,width=20)
                     e._id = len(line)-1
                     e.pack(side=tk.LEFT)
                     cnt = cnt + 1
              frm_tmp.pack()

       ###Packing
       greeting.pack()
       tables.pack()
       frm.pack()
       
       ### Begin program
       print("Breakpoint")
       root.title('Moosh')
       root.geometry("1000x800")
       root.mainloop()

       

def exit_handler():
    print ('I am dying')
    # for line in dailies:
    #     print(line)

atexit.register(exit_handler)


       ### Packing
       

if __name__ == '__main__':
    main()