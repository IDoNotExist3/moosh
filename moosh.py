import psycopg2
import tkinter as tk
import atexit

conn = psycopg2.connect(database="moosh",
                        host="localhost",
                        user="postgres",
                        password="MintAndThyme!1!",
                        port="5432")


def main():
       ### Initialize Tkinter
       root = tk.Tk()
       sv = tk.StringVar()

       frm = tk.Frame(master=root)

       ###Frames
       frm_ent_test = tk.Frame(master=root,relief=tk.RIDGE,borderwidth=5)

       ### Initalize postgreSQL cursor
       cursor = conn.cursor()

       sql = "SELECT * from jars"
       cursor.execute(sql)
       res = cursor.fetchall()
       for line in res:
              frm_tmp = tk.Frame(master=frm_ent_test)
              cnt = 0
              for txt in line:
                     text = tk.StringVar()
                     text.set(txt) 
                     tk.Entry(master=frm_tmp,textvariable=text,validate="focusout",width=20).pack(side=tk.LEFT)
                     cnt = cnt + 1
              frm_tmp.pack()

       ###Packing
       frm_ent_test.pack()
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