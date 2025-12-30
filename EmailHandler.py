import gmail
def send_credentials(email,name,acn,pwd):
    con=gmail.GMail('priyaporwal2003@gmail.com','zphe ylwv pdwh kgpx')
    body=f'''Hello {name},
    Welcome to Canara Bank,Here is your credentials
    Account No= {acn}
    Password= {pwd}

    Kindly change your password when login first time

    Canara Bank
    Sector-16,Noida
'''
    msg=gmail.Message(to=email,subject='Your Credentials For Operating Account',text=body)
    con.send(msg)

def send_otp(email,name,otp):
    con=gmail.GMail('priyaporwal2003@gmail.com','zphe ylwv pdwh kgpx')
    body=f'''Hello {name},
    Welcome to Canara Bank,Here is your otp to recover password

    OTP = {otp}

    Canara Bank
    Sector-16,Noida
'''
    msg=gmail.Message(to=email,subject='OTP for password recovery',text=body)
    con.send(msg)

def send_otp_withdraw(email,name,otp,amt):
    con=gmail.GMail('priyaporwal2003@gmail.com','zphe ylwv pdwh kgpx')
    body=f'''Hello {name},
    Welcome to Canara Bank,Here is your otp to withdraw {amt}

    OTP = {otp}

    Canara Bank
    Sector-16,Noida
'''
    msg=gmail.Message(to=email,subject='OTP for withdrawl',text=body)
    con.send(msg)    

def send_otp_transfer(email,name,otp,amt,to_acn):
    con=gmail.GMail('priyaporwal2003@gmail.com','zphe ylwv pdwh kgpx')
    body=f'''Hello {name},
    Welcome to Canara Bank,Here is your otp to transfer amount : {amt} to ACN : {to_acn}

    OTP = {otp}

    Canara Bank
    Sector-16,Noida
'''
    msg=gmail.Message(to=email,subject='OTP for transfer',text=body)
    con.send(msg)