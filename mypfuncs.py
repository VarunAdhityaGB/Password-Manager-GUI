######################## IMPORTING MODULES ###############################################
import mysql.connector as sqlc
import random
from string import ascii_letters, ascii_uppercase, digits, ascii_lowercase, punctuation
from hashlib import *
import requests

######################## CONNECTING SQL ###############################################
mydb = sqlc.connect(host='localhost', user='root', passwd='root',)
mycur = mydb.cursor()

#########################   VARIABLES   ##################################################
#characters
lcase, ucase, num, alpha, pun = list(ascii_lowercase), list(ascii_uppercase),\
     list(digits), list(ascii_letters), ['!','@','#','$','%','^','&','*','-','_','/']
charst = lcase + ucase + num 

#defining encryption variables
lcase_crypt = ['M','L','W','U','Z','C','H','A','N','J','O','P','I','S','T','D','G','K','X','E','B','Y','R','Q','V','F']
ucase_crypt = ['m','w','f','l','s','n','o','i','d','a','g','e','u','h','p','r','y','k','q','c','x','b','v','z','j','t']
num_crypt = ['6', '4', '7', '8', '5', '2', '0', '3', '1', '9']
charst_crypt = lcase_crypt + ucase_crypt + num_crypt

#########################   FUNCTIONS   ##################################################
def shuffle(strg):
    ls = list(strg)
    random.shuffle(ls)
    
def password(n : int):
    char = [lcase, ucase, num, alpha, pun]

    #generating the password
    passwd = random.choice(pun) +  random.choice(lcase) +  random.choice(ucase) + random.choice(alpha) +  random.choice(num) 
    for i in range(n-6):
        passwd += random.choice(random.choice(char))

    #Seperating the password AND Checking
    passwd_l = list(passwd)
    
    if pun not in passwd_l:
        passwd_l.append(random.choice(pun))
    elif ucase not in passwd_l:
        passwd_l.append(random.choice(ucase))
    elif num not in passwd_l:
        passwd_l.append(random.choice(num))
    
    #Joining the password
    passwd = ''.join(passwd_l)

    #shuffling the password    
    shuffle(passwd)
    
    return passwd

def encrypt(strg : str):
    str_ls = list(strg)
    for i in str_ls:
        if i in charst:
            i_pos = str_ls.index(i)
            c_pos = charst.index(i)
            str_ls[i_pos] = charst_crypt[c_pos]
        else:
            pass        
    strg = ''.join(str_ls)
    return strg      
        

def hashcrypt(var):
    hash = md5(var.encode())
    hashc = hash.hexdigest()
    hash_crypt = encrypt(hashc)
    return hash_crypt

def unamevalidation(strg):
    pun_ls = list(punctuation)
    pun_ls.remove('@')
    pun_ls. remove('_')
    pun_ls.append(' ')
    strg_ls = list(strg)
    for i in strg_ls:
        if i in pun_ls:
            return False
        else:
            return True

def emailvalidation(strg):
    email = strg
    response = requests.get("https://isitarealemail.com/api/email/validate", params= {'email': email})
    status = response.json()['status']
    if status == "valid":
        return True
    elif status == "invalid":
        return False

def unamecheck(strg):
    mycur.execute("USE MYP;")
    username_ls = []
    mycur.execute("SELECT userName FROM myp_users;")
    for i in mycur:
        username_ls.append(i)
    if strg in username_ls:
        return False
    else:
        return True

def emailcheck(strg):
    mycur.execute("USE MYP;")
    email_ls = []
    mycur.execute("SELECT eMail FROM myp_users;")
    for i in mycur:
        email_ls.append(i)
    if strg in email_ls:
        return False
    else:
        return True