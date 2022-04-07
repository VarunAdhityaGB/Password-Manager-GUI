from operator import imod
import mysql.connector as sqlc
from mypfuncs import *
from pwinput import pwinput
import os
import sys
import smtplib
from email.message import EmailMessage
import random
##################################### CREATING DATABASE ################################

mydb = sqlc.connect(host='localhost', user='root', passwd='root',)
mycur = mydb.cursor()
def createDB():
    mycur.execute("CREATE DATABASE MYP;")

##################################### FUNCTIONS ################################
def createTbls():
    mycur.execute("USE MYP;") 
    mycur.execute('''CREATE TABLE myp_users (
            userId INT  UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            firstName VARCHAR(225) NOT NULL,
            lastName VARCHAR(225),
            userName VARCHAR(225) NOT NULL UNIQUE KEY,
            eMail VARCHAR(225) NOT NULL UNIQUE KEY,
            masterPass VARCHAR(225) NOT NULL); ''')

    mycur.execute('''CREATE TABLE myp_data (
        passId INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        website VARCHAR(225),
        loginName VARCHAR(225) NOT NULL,
        loginPass VARCHAR(225) NOT NULL,
        userId INT NOT NULL); ''')

def insintousers(firstName, lastName, userName, eMail, masterPass):
    mycur.execute("USE MYP;")
    global passu
    passu = hashcrypt(masterPass)
    action = f"""INSERT INTO myp_users (firstName, lastName, userName, eMail, masterPass)
        VALUES (""" + "TRIM('" + firstName + "'), " + "TRIM('" + lastName + "'), '" + userName + "', '" + eMail + "', '" + passu + "');"
    mycur.execute(action)
    mydb.commit()

def insintodata(website, loginName, loginPass, userId):
    mycur.execute("USE MYP;") 
    global passd
    passd = hashcrypt(loginPass)
    action = f"""INSERT INTO myp_users (website, loginName, loginPass, userId) 
        VALUES ('""" + website + "', '" + loginName + "', '" + passd + "', '" + userId + "');"
    mycur.execute(action)
    mydb.commit()

def otpmail(name, receivermail):
    global otp
    recmail = receivermail
    otp = random.randint(100000, 999999)

    msg = EmailMessage()
    msg.set_content(f'''Hello {name},
        Thank you for trying our password manager.
        Hope you like our product.
        
        THE ONE-TIME PASSWORD FOR YOUR ACCOUNT IS:
                    
                            {otp}                             ''')
    
    msg['Subject'] = 'One-Time-Password for Password Manager'
    msg['From'] = 'manageyourpass91@gmail.com'
    msg['To'] = recmail
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('manageyourpass91@gmail.com','Acc3ssGr@nted')
    server.send_message(msg)
    server.quit()

def login():
    mycur.execute("USE MYP;")
    print("How would you like to sign in? \n1.Username \n2.E-mail address\n3.Go Back ")
    cho = int(input())
    os.system('clear')
    sea = False  #just a random variable
    while sea == False:
        if cho == 1:
            uname_srch = input("Username: ")
            sea = True
            mycur.execute(f"SELECT masterPass FROM myp_users WHERE userName = '{uname_srch}';")
        elif cho == 2:
            email_srch = input("E-Mail Address: ")
            sea = True
            mycur.execute(f"SELECT masterPass FROM myp_users WHERE eMail = '{email_srch}';")
        elif cho == 3:
            login_page()
            if opt_lp == 3:
                sys.exit
        else:
            print("ENTER ONLY 1 OR 2 OR 3!!")
    pass_ls = []
    for i in mycur:
        pass_ls.extend(i)

    ch = False
    while ch == False:
        masterPass_check_hash = hashcrypt(pwinput("Password: "))
        if masterPass_check_hash == pass_ls[0]:
            print("Access Granted")
            ch = True
        else:
            print("Access Denied")
    pass_ls = []
    post_login()

def signup():
    w = 't'
    fName = input("Enter your first name:")
    lName = input("Enter your last name:")
        
    ############ USER NAME CHECK
    usName = input("Enter your username:")
    while unamecheck(usName) is False:
        print("THIS USERNAME ALREADY EXISTS !!!")
        usName = input("Enter another username: ")

    uName = usName
    
    ############ EMAIL CHECK
    e_Mail = input("Enter your e-mail address:")
    ope = emailvalidation(e_Mail)
    while ope is False:
        print('INVALID EMAIL ID !!')
        e_Mail = input("Enter a vaild e-mail address:") 
        ope = emailvalidation(e_Mail)

    if emailcheck(e_Mail) is False:
        print("There is another account linked with this e-mail address")
        eMail = input("Enter your e-mail address: ")
    else:
        eMail = e_Mail

    otpmail(fName + ' ' + lName, eMail)
    otp_opt = False
    otp_count = 0 
    while otp_opt == False:
        otp_check = int(input("Enter the OTP recieved on your registered email: "))
        if otp_check != otp:
            otp_count += 1
            otp_check = int(input("Please double check your OTP: "))
            if otp_count > 1:
                os.system('clear')
                print('Resend OTP?')
                c = int(input("1.Yes\n2.No\n3.Exit"))
                if c == 1:
                    otpmail(fName + ' ' + lName, eMail)
                elif c == 2:
                    otp_check = int(input("Enter the correct OTP: "))
                else:
                    sys.exit
            elif otp_count > 3:
                print("Need help?")
                print('Forgot your registered email address?')
                d = int(input("1.Yes\n2.No"))
                if d == 1:
                    print(f"Your email address is {eMail}")
                    otp_check = int(input("Now enter the correct OTP: "))
                else:
                    otp_check = int(input("Enter the correct OTP: "))
        else:
            otp_opt = True
    

    ############ password
    while w == 't':
        masterPass = pwinput("New Password: ")
        masterPass_check = pwinput("Re-enter Password: ")
        if masterPass_check == masterPass:    
            insintousers(fName, lName, uName, eMail, masterPass)
            break
        else:
            print("YOUR PASSWORDS DON'T MATCH!")

    os.system('clear')
    login()

def retrievepass():
    pass

def storepass():
    pass

def generatepass():
    web = input("Website Name: ")


def login_page():
    print('''-----------MENU-----------
    1. Login
    2. Sign Up
    3. Exit''')

    global opt_lp
    opt_lp = int(input(""))
    os.system('clear')
    if opt_lp == 1:
        login()

    elif opt_lp == 2:
        signup()
        
    elif opt_lp == 3:
        sys.exit            

def post_login():
    os.system('clear')
    print('''-----------MENU-----------
    1. Retrieve Password
    2. Store Password
    3. Generate Password
    4. Log Out
    5. Exit''')

    opt = int(input())
    if opt == 1:
        pass
    elif opt == 2:
        pass
    elif opt == 3:
        pass
    elif opt == 4:
        os.system('clear')
        login_page()
    elif opt == 5:
        sys.exit