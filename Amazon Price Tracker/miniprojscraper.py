from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
import requests
from bs4 import BeautifulSoup
import smtplib

headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36' }

#Functions to Insert record into Database
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def insert():
    id = e_id.get()
    URL = e_URL.get()
    name = e_name.get();
    phone = e_phone.get();

    if(id== "" or name=="" or phone==""):
       MessageBox.showinfo("Insert Status","All Fields are Required")
    else:
         con =mysql.connect(host = "localhost",user="root",password="",database="price tracker db")
         cursor =con.cursor()
         cursor.execute("insert into student values('"+ id +"', '"+ URL +"', '"+ name +"','"+ phone +"')")
         cursor.execute("commit");

         e_id.delete(0, 'end')
         e_URL.delete(0, 'end')
         e_name.delete(0, 'end')
         e_phone.delete(0, 'end')
         show()
         MessageBox.showinfo("Insert Status","Inserted Successfully");
         con.close();
   

#Functions to Delete the record from Database by taking tracking id 
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def delete():    
   
       if(e_id.get() ==""):
          MessageBox.showinfo("Delete Status","ID is compulsory for delete")
       else:
         con =mysql.connect(host = "localhost",user="root",password="",database="price tracker db")
         cursor =con.cursor()
         cursor.execute("delete from student where id='"+ e_id.get() +"'")
         cursor.execute("commit");
         e_id.delete(0, 'end')
         e_URL.delete(0, 'end')
         e_name.delete(0, 'end')
         e_phone.delete(0, 'end')
         show()
         MessageBox.showinfo("Delete Status","Deleted Successfully");

         con.close();


#Functions to Update the record from Databae by taking tracking id 
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def update():
   id = e_id.get();
   URL = e_URL.get();
   name = e_name.get();
   phone = e_phone.get();

   if(id== "" or URL== "" or name=="" or phone==""):
       MessageBox.showinfo("Update Status","All Fields are Required")
   else:
      con =mysql.connect(host = "localhost",user="root",password="",database="price tracker db")
      cursor =con.cursor()
      cursor.execute("Update student set Email='"+ name +"',Price='"+ phone +"' ,URL ='"+ URL+"' where id='"+ id +"'")
#      cursor.execute("Update student set name='"+ name +"',phone='"+ phone +"' where id='"+ id +"'")
      cursor.execute("commit");
      e_id.delete(0, 'end')
      e_URL.delete(0, 'end')
      e_name.delete(0, 'end')
      e_phone.delete(0, 'end')
      show()
      MessageBox.showinfo("Update Status","Updated Successfully");

      con.close();   


#Functions to Retrieve the record from Database by taking tracking id 
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def get():
   if(e_id.get() ==""):
            MessageBox.showinfo("Fetch Status","ID is compulsory for fetch")
   else:
      con =mysql.connect(host = "localhost",user="root",password="",database="price tracker db")
      cursor =con.cursor()
      cursor.execute("Select * from student where id='"+ e_id.get() +"'")
      rows = cursor.fetchall()

      for row in rows:
            e_URL.insert(0,row[1])     
            e_name.insert(0, row[2])
            e_phone.insert(0,row[3])

            con.close()  ;

#Functions is to Show the list of record 
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def show():  
    con =mysql.connect(host = "localhost",user="root",password="",database="price tracker db")
    cursor =con.cursor()
    cursor.execute("Select * from student ")
    rows = cursor.fetchall()
    list.delete(0,list.size())
          
    for row in rows:
        insertData = str(row[0])+'     '+row[1]
        list.insert(list.size()+1,insertData)

    con.close()

#Functions is Run Scrapper job by taking tracking id and sending email based on user requirement. 
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def run():
   if(e_id.get() ==""):
       MessageBox.showinfo("Run Status","ID is compulsory for Tracking Your Product")
   else:
       #MessageBox.showinfo("Run Status","Tracking Successfully");
       ProdURL=e_URL.get()
       UserEmail=e_name.get()
       ProdPrice=e_phone.get()
       check_price(ProdURL, UserEmail, ProdPrice)
       #MessageBox.showinfo("URL",ProdURL+" " +UserEmail+" "+ProdPrice);

#Functions to check price by taking URL, Price and Email address as Parameters
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def check_price(URL_Param, Email_Param, Price_Param):
    page = requests.get(URL_Param, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    MessageBox.showinfo("URL",URL_Param+" " +Email_Param+" "+Price_Param);
    try: 
        print("Inside try block priceblock_ourprice Sudheer Singh 1:")
        price = soup.find(id="priceblock_ourprice").get_text().strip()      
    except AttributeError: 
        print("There is no such attribute called priceblock_ourprice")     
    try: 
        print("Inside try block priceblock_dealprice Sudheer Singh 1:")
        price = soup.find(id="priceblock_dealprice").get_text().strip()      
    except AttributeError: 
        print("There is no such attribute called priceblock_dealprice")     
    try: 
        print("Inside try block priceblock_saleprice Sudheer Singh 1:")
        price = soup.find(id="priceblock_saleprice").get_text().strip()      
    except AttributeError: 
        print("There is no such attribute called priceblock_saleprice")     

#   price = soup.find(id="priceblock_ourprice").get_text().strip()
#    price_deal = soup.find(id="priceblock_dealprice").get_text().strip()
    price1 = price.replace("," , "")
    print("Price  : " +price)
    print("Price1 : " +price1)
    converted_price = float(price1[2:8])    
    if(converted_price < float(Price_Param)):
         send_mail(Email_Param, URL_Param)

    # if(converted_price < float(Price_Param)) && price_flag == "L":
    #     send_mail(Email_Param, URL_Param)
    # if(converted_price > float(Price_Param)) && price_flag == "H":
    #     send_mail(Email_Param, URL_Param)

   

    

#Function will send email 
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

def send_mail(Email_Param, URL_Param):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo

    server.login('rishabhsinghyy@gmail.com', 'ixkicvutadbfpjim')

    subject='Price fell down'
    body = "Check the URL Link :" + URL_Param
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail('rishabhsinghyy@gmail.com', Email_Param, msg )

    MessageBox.showinfo("Message is sent To : ",Email_Param);
    
    server.quit()    


#Below is Code of GUI
#Author : Rishabh Singh and SVIT Amazon Price Monitoring APP Team

root =Tk()
root.geometry("800x400")
root.title("Scraper GUI")

id = Label(root, text='Tracking ID',font=('bold',10))
id.place(x=20, y=30);

URL = Label(root, text='URL',font=('bold',10))
URL.place(x=20, y=60);

name = Label(root, text='Email Address',font=('bold',10))
name.place(x=20, y=90);

Phone = Label(root, text='Price',font=('bold',10))
Phone.place(x=20, y=120);

e_id =Entry()
e_id.place(x=150, y=30)

e_URL =Entry()
e_URL.place(x=150, y=60, width=400)

e_name =Entry()
e_name.place(x=150, y=90, width=250)

e_phone=Entry()
e_phone.place(x=150, y=120)


insert = Button(root, text="Insert",font= ("italic",10),bg="white",command=insert)
insert.place(x=20, y=160)

delete = Button(root, text="Delete",font= ("italic",10),bg="white",command=delete)
delete.place(x=70, y=160)

update = Button(root, text="Update",font= ("italic",10),bg="white",command=update)
update.place(x=130, y=160)

Run = Button(root, text="Run",font= ("italic",10),bg="white",command=run)
Run.place(x=190, y=160)

get = Button(root, text="Get",font= ("italic",10),bg="white",command=get)
get.place(x=250, y=160)

T = Text(root, x = 5, width = 52)

l = Label(root, text = "Fact of the Day") 
l.config(font =("Courier", 14))



# def sel():
#    selection = "You selected the option " + str(var.get())
#    label.config(text = selection)


# var = IntVar()

# R1 = Radiobutton(root, text="H", variable=var, value=1,
#                   command=sel)
# R1.place(x=300, y=120)

# R2 = Radiobutton(root, text="L", variable=var, value=2,
#                   command=sel)
# R2.place(x=340, y=120)


list = Listbox(root)
list.place(x=600,y=30)
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

show()

root.mainloop()
