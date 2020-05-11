#TARIH     : 
#PROJE ADI : 

import MOD                                                      #Timer iþlemleri için
import SER                                                      #Seri haberleþme için
import GPIO                                                     #Pin ler iþ yaptýrmak için
import MDM                                                      #Python ile AT komut seti arasýndaki baðlantý
import sys                                                      #Dosya iþlemleri için

#Initiliaze
#----------
uResp = ""
uGetChar = ""
MineIP = ""
dummy1 = ""
DUMMY1 = ""
dummy2 = ""
DUMMY2 = ""
dummy3 = ""
DUMMY3 = ""
dummy4 = ""
DUMMY4 = ""
SMSRESP = 0  
SMSRESP1 = "" 
SMSRESP2 = "" 
SMSRESP3 = "" 
PinStatus = ""
TELRESP3 = ""
uGetCharFromMDM = ""
TelResp = ""
SmsPopUp = ""
uRespFromMDM = ""
uResp = ""
TelResp = ""
tResp = 0
IntResp = 0
Temp = 0
sByte = 0
TEMPRESP = 0
dummy9 = ""
command = ""
whichpin = ""
bwhichpin = 0
logic = ""
blogic = ""
DUMM = 0
fileResp = 0
SMSNO1 = ""
SMSNO2 = ""
TEMPMAX = ""
TEMPMIN = ""
SMTP_SERVER = ""
SENDER_EMAIL_ADDR = ""
SENDER_EMAIL_PASS = ""
RECIEVER_EMAIL_ADDR1 = ""
RECIEVER_EMAIL_ADDR2 = ""
ADJPASSVALUE = 0
TempControlValue = 0
ControlStatus = 0
ADJTELNO = ""

#------------------------Functions--------------------------------------
def ALARMLed(s1):
    Smsled = GPIO.setIOvalue(6,s1)
def TEMPread(Channel):
    Temp = GPIO.getADC(Channel)

    if(Temp == -1):
        tResp = 0
        return tResp
    
    tResp = 1    
    sByte = (Temp / 10000) + 48    
    IntResp = SER.sendbyte(sByte)
    sByte = ((Temp % 10000) / 1000) + 48   
    IntResp = SER.sendbyte(sByte)
    sByte = ((Temp % 1000) / 100) + 48    
    IntResp = SER.sendbyte(sByte)
    sByte = ((Temp % 100) / 10) + 48    
    IntResp = SER.sendbyte(sByte)
    sByte = (Temp % 10) + 48    
    IntResp = SER.sendbyte(sByte)
    
    return tResp

def outGPIO(out,setvalue):
    wrGP = GPIO.setIOvalue(out,setvalue)
    wrGP = (wrGP%10) + 48
    IntResp = SER.sendbyte(wrGP)
    return IntResp

def inGPIO(din):
    rdGP = GPIO.getIOvalue(din)
    rdGP = (rdGP%10) + 48
    IntResp = SER.sendbyte(rdGP)
    return IntResp
    

def SMSLed(s1):
    Smsled = GPIO.setIOvalue(8,s1) 
def SMS(SmsTo_,SmsText_):
    sResp =""
    sRcv = ""
    sTimeout = 0
    SmsStatus = 0

    SMSLed(0)
        
    #Here start the SMS session
    sRcv = ""
    sTimeout = 0
    if( sTimeout < 4 ):
        sTimeout = 0	
        sRcv = ""
        while (sRcv.find('OK')==-1):				
            MDM.send('AT\r',0)
            sRcv = MDM.receive(10)
            sTimeout = sTimeout + 1
            if( sTimeout > 4 ):
                break 

    if( sTimeout < 4 ):
        sTimeout = 0
        MOD.sleep(5)
        
        sRcv = ""
        while (sRcv.find('OK')==-1):				
            MDM.send('AT+CREG?\r',0)
            sRcv = MDM.receive(10)
                
            if (sRcv.find('0,1') != -1) or (sRcv.find('1,1') != -1) or (sRcv.find('0,2') != -1) or (sRcv.find('1,5') != -1):
                SmsStatus = 1                               #Sim registered
                break
            else:
                SmsStatus = 0                               #Sim unregistered
                sTimeout = 5
                break
            sTimeout = sTimeout + 1
            if( sTimeout > 4 ):
                break 
            
                
    if( sTimeout < 4 ):
        sTimeout = 0	
        MOD.sleep(5)
        sRcv = ""
        while (sRcv.find('OK')==-1):				
            MDM.send('AT+CMGF=1\r',0)
            sRcv = MDM.receive(10)
            sTimeout = sTimeout + 1
            if( sTimeout > 4 ):
                break 
        
                
    if( sTimeout < 4 ):
        sTimeout = 0
        MOD.sleep(5)	
        sRcv = ""
        while (sRcv.find('>')==-1):				
            MDM.send('AT+CMGS="' + SmsTo_ + '"\r', 0)
            sRcv = MDM.receive(10)
            sTimeout = sTimeout + 1
            if( sTimeout > 4 ):
                break 
           
                
    if( sTimeout < 4 ):
        sTimeout = 0	
        MOD.sleep(5)
        sRcv = ""
        while (sRcv.find('OK')==-1):				
            MDM.send(SmsText_, 0)
            MOD.sleep(5)
            MDM.sendbyte(0x1A, 0)
            sRcv = MDM.receive(50)
            sTimeout = sTimeout + 1
            if( sTimeout > 4 ):
                break 
          
                
    SMSLed(1)        
    if(sTimeout < 4 ):
        sTimeout = 0
        sRcv = ""
        return 1 
    else:
        sTimeout = 0
        if( SmsStatus == 0 ):
            return -2                                               #Sim unregistered
        else:
            return -1                                               #Sim Kaydý var ama Sms not sent
#1  -->Mesaj Gönderildi
#-1 -->Sim kaydý var ama sms gitmedi
#-2 -->Sim kartýnýn kaydý yok ya da pin girilmedi


def SMS_READ(WhichSms):
    srRcv = ""
    srTimeout = 0
    srDummy1 = ""
    srDummy2 = ""
    srDummy3 = ""
    srDummy4 = ""
    srSmsStatus = ""
    global ADJTELNO

    if( srTimeout == 0 ):
        srRcv = ""
        f = MDM.send('AT+CREG?\r',0)
        srRcv = MDM.receive(20)
        if( srRcv != "" ):
            if (srRcv.find('0,1') != -1) or (srRcv.find('1,1') != -1) or (srRcv.find('0,2') != -1) or (srRcv.find('1,5') != -1):
                srSmsStatus = '1'                                   #Sim registered
            else:
                srSmsStatus = '0'                                   #Sim unregistered
                srTimeout = 1 
        else:
            srSmsStatus = '9'
            srTimeout = 1
            
    if( srTimeout == 0 ):
        srRcv = ""
        MOD.sleep(5)
        f = MDM.send('AT+CMGF=1\r',0)                               #Text moduna geç
        srRcv = MDM.receive(20)
        if( srRcv != "" ):
            if( srRcv.find('OK') == -1 ):
                srTimeout = 1
                srSmsStatus = '9'
        else:
            srTimeout = 1
            srSmsStatus = '9'
            
    if( srTimeout == 0 ):
        srRcv = ""
        MOD.sleep(5)
        f = MDM.send('AT+CMGR=' + WhichSms + '\r',0)
        srRcv = MDM.receive(20)
        #SER.send(srRcv)
        
        if( srRcv.find('READ') != -1 ):
            #sms içeriðini oku
            srDummy1 = srRcv.split(',')
            srDummy2 = srDummy1[0].split('"')
            
            #SER.send(srDummy2[1] + '\r\n')            
            if( srDummy2[1] == "REC READ" ):
                srSmsStatus = '4'                                   #sms okunmuþ
            if( srDummy2[1] == "REC UNREAD" ):
                srSmsStatus = '5'                                   #sms okunmamýþ
            if( srSmsStatus == '5' ):
                #SER.send(srDummy1[1][3:14] + '\r\n')               #sms gelen tel no
                srSmsStatus = srDummy1[1][3:14]                     #sms gelen tel no
                if( srDummy1[4].find('#') != -1 ):
                    srDummy3 = srDummy1[4].split('#')
                    srDummy4 = srDummy3[1].strip()
                    #SER.send(srDummy3[1])                          #sms text i
                    srSmsStatus = srDummy3[1]
                    ADJTELNO = srDummy1[1][3:14]
                else:
                    srSmsStatus = '6'                               #sms text yok
                    
            srTimeout = 0
        elif( srRcv.find('OK') != -1 ):
            srSmsStatus = '3'                                       #sms yok
        elif( srRcv == "" ):
            srTimeout = 1                                           #cevap yok hata
            srSmsStatus = '9'
            rSmsStatus = '2'

    return srSmsStatus
#srSmsStatus = '9'    =>      Timeout
#srSmsStatus = '0'    =>      Sim unregistered
#srSmsStatus = '1'    =>      Sim registered
#srSmsStatus = '2'    =>      Sim registered fakat okuma iþlemine cevap gelmedi
#srSmsStatus = '3'    =>      Sim registered fakat Sms yok
#srSmsStatus = '4'    =>      READ mesaj
#srSmsStatus = '5'    =>      UNREAD mesaj
#srSmsStatus = '6'    =>      Sms geldi UNREAD ama text boþ



def SMS_DEL(dWhichSms):
    sdRcv = ""
    sdTimeout = 0
    sdSmsStatus = ""

    if( sdTimeout == 0 ):
        sdRcv = ""
        f = MDM.send('AT+CREG?\r',0)
        sdRcv = MDM.receive(20)
        if( sdRcv != "" ):
            if (sdRcv.find('0,1') != -1) or (sdRcv.find('1,1') != -1) or (sdRcv.find('0,2') != -1) or (sdRcv.find('1,5') != -1):
                sdSmsStatus = '1'                                   #sim registered
            else:
                sdSmsStatus = '0'                                   #sim unregistered
                sdTimeout = 1 
        else:
            sdTimeout = 1
            
    if( sdTimeout == 0 ):   
        sdRcv = ""
        MOD.sleep(5)
        f = MDM.send('AT+CMGF=1\r',0)                               #text moduna geç
        sdRcv = MDM.receive(20)
        if( sdRcv != "" ):
            if( sdRcv.find('OK') == -1 ):
                sdTimeout = 1
                sdSmsStatus = '9'
        else:
            sdTimeout = 1
            
    if( sdTimeout == 0 ):
        sdRcv = ""
        MOD.sleep(5)
        f = MDM.send('AT+CMGD=' + dWhichSms + '\r',0)
        sdRcv = MDM.receive(20)
 
        if( sdRcv.find('OK') != -1 ):
            sdSmsStatus = '2'                                       #sms silindi
        else:
            sdSmsStatus = '3'
    
    if( sdTimeout != 0 ):
        sdSmsStatus = '9'

    return sdSmsStatus
#sdSmsStatus = '9'    =>      Timeout
#sdSmsStatus = '0'    =>      Sim unregistered
#sdSmsStatus = '1'    =>      Sim registered
#sdSmsStatus = '2'    =>      Sim registered ve sms silindi
#sdSmsStatus = '3'    =>      Sim registered fakat cevap yok ya da sms silinemedi

def SMS_DEL_ALL():
    sdallRcv_ = ""
    sdallTimeout_ = 0
    sdallSmsStatus = ""

    if( sdallTimeout_ == 0 ):
        sdallRcv_ = ""
        f = MDM.send('AT+CREG?\r',0)
        sdallRcv_ = MDM.receive(20)
        if( sdallRcv_ != "" ):
            if (sdallRcv_.find('0,1') != -1) or (sdallRcv_.find('1,1') != -1) or (sdallRcv_.find('0,2') != -1) or (sdallRcv_.find('1,5') != -1):
                sdallSmsStatus = '1'                                  #sim registered
            else:
                sdallSmsStatus = '0'                                  #sim unregistered
                sdallTimeout_ = 1 
        else:
            sdallTimeout_ = 1
            
    if( sdallTimeout_ == 0 ):
        sdallRcv_ = ""
        MOD.sleep(5)
        f = MDM.send('AT+CMGF=1\r',0)                               #text moduna geç
        sdallRcv_ = MDM.receive(20)
        if( sdallRcv_ != "" ):
            if( sdallRcv_.find('OK') == -1 ):
                sdallTimeout_ = 1
                sdallSmsStatus = '9'
        else:
            sdallTimeout_ = 1
            
    if( sdallTimeout_ == 0 ):
        sdallRcv_ = ""
        MOD.sleep(5)
        f = MDM.send('AT+CMGD=1,4\r',0)
        sdallRcv_ = MDM.receive(20)
 
        if( sdallRcv_.find('OK') != -1 ):
            sdallSmsStatus = '2'                                      #sms silindi
        else:
            sdallSmsStatus = '3'
    
    if( sdallTimeout_ != 0 ):
        sdallSmsStatus = '9'
        
    return sdallSmsStatus
#sdaSmsStatus = '9'    =>      Timeout
#sdaSmsStatus = '0'    =>      Sim unregistered
#sdaSmsStatus = '1'    =>      Sim registered
#sdaSmsStatus = '2'    =>      Sim registered ve sms in hepsi silindi
#sdaSmsStatus = '3'    =>      Sim registered fakat cevap yok ya da sms ler silinemedi
    


def LISTEN_SMS():			
    slRcv = ""
    f = MDM.send('AT+CSMP=17,167,0,242\r',0)
    slRcv = MDM.receive(20)
    f = MDM.send('AT+CNMI=1,1,0,0,0\r',0)
    slRcv = MDM.receive(20)
            
    if( slRcv.find('OK') != -1 ):
        return '1' 
    else:
        return '0'
    
#'1'  => Sms gelince uyarma iþlemi aktif
#'0' => cevapta OK yok.
    
def REBOOT():
    rbRcv = ""
    f = MDM.send('AT#REBOOT\r',0)
    rbRcv = MDM.receive(20)
            
    if( rbRcv.find('OK') != -1 ):
        return '1' 
    else:
        return '0'
    
#'1' => Reboot yaptý
#'0' => cevapta OK yok.
    
def PIN():
    # Here start the SMS session
    pRcv = ""   
    pTimeout = 0
    if( pTimeout < 4 ):
        pTimeout = 0
        pRcv = "" 
        while (pRcv.find('+CPIN')==-1):				
            MDM.send('AT+CPIN?\r',0)
            pRcv = MDM.receive(10)
            pTimeout = pTimeout + 1
            if( pTimeout > 4 ):
                break 
    
    if( pTimeout < 4 ):
        pTimeout = 0
        if( pRcv.find('READY') != -1 ):
            #pin koduna gerek yok.
            return '1'
        elif( pRcv.find('SIM PIN') != -1 ):
            #pin kodu girilecek
            return '0'
        elif( pRcv.find('SIM PUK') != -1 ):
            #pin kodu girilecek
            return '2'
        else:
            #sim takýlý deðil olabilir
            return '3'
    else:
        return '9'
#'9'    ->      timout
#'0'    ->      pin kodu girilecek
#'1'    ->      pin koduna gerek yok.
#'2'    ->      pin kodu girilecek
#'3'    ->      sim takýlý deðil olabilir   
         
def PINopen(PinKod):
    x = MDM.send('AT+CPIN='+PinKod+'\r', 0)
    pOpenRcv = MDM.receive(30)
    if( pOpenRcv.find('OK') != -1 ):
        return '1'
    else:
        return '0'
#'1' => PIN kodu doðru
#'0' => PIN kodu yanlýþ
        
#-------------------------------------------------------
#Adjust
#SER.set_speed('115200','8N1')

def EMAILLed(s1):
    Smsled = GPIO.setIOvalue(7,s1)

    
def EMAIL(SMTPSERVER,SENDEREMAIL,SENDERPASSW,SENDERNAME,RCVEMAIL,EMAILSUBJECT,EMAILTEXT):
    EMAILLed(0)
    e = 0
    s = ""
    STATUS = ""

    e = 0
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '16'
                break

    if( e < 4 ):
        e = 0
        MOD.sleep(5) 
     
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT+FCLASS=0\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '15'
                break


    if( e < 4 ):
        e = 0	
        MOD.sleep(5) 

        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT&K0\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '14'
                break    

    if( e < 4 ):
        e = 0
        MOD.sleep(5)
        
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT+CREG?\r',0)
            s = MDM.receive(10)
                
            if (s.find('0,1') != -1) or (s.find('1,1') != -1) or (s.find('0,2') != -1) or (s.find('1,5') != -1):
                break
            else:
                SmsStatus = 0        
                STATUS = '13'
                break
            e = e + 1
            if( e > 4 ):
                break 
            
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#SCFG?\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '12'
                break


    if( e < 4 ):
        e = 0	
        MOD.sleep(5) 
                                       
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#SGACT=1,0\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '11'
                break

    if( e < 4 ):
        e = 0		
        MOD.sleep(5) 
                                                            # configure the socket1
        s = ""
        while (s.find('OK')==-1) :				
            #MDM.send('AT#SCFG=1,1,200,90,300,50\r',0)
            #MDM.send('AT#SCFG=1,1,10,90,300,1\r',0)        10 karakter gönderilitor
            MDM.send('AT#SCFG=1,1,250,90,300,1\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '10'
                break

    if( e < 4 ):
        MOD.sleep(15) 
        e = 0	
        s = ""
        while (s.find('#SGACT')==-1):
            a = MDM.send('AT#SGACT=1,1\r', 10)                # GPRS context activation
            s = MDM.receive(100)
            MineIP = s
            #a = SER.send(s)		                          # debug info
            e = e + 1
            if( e > 4 ):
                STATUS = '09'
                break
            
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#GPRS=0\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '08'
                break

    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#ESMTP="' + SMTPSERVER + '"\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '07'
                break
            
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#EUSER="' + SENDERNAME + '"\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '06'
                break
            
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#EPASSW="' + SENDERPASSW + '"\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '05'
                break
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#EADDR="' + SENDEREMAIL + '"\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '04'
                break
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('OK')==-1):				
            MDM.send('AT#ESAV\r',0)
            s = MDM.receive(10)
            e = e + 1
            if( e > 4 ):
                STATUS = '03'
                break
    if( e < 4 ):
        e = 0	
        s = ""
        while (s.find('>')==-1):		
            MDM.send('AT#SEMAIL="' + RCVEMAIL + '","' + EMAILSUBJECT + '",0\r',0)
            s = MDM.receive(150)
            e = e + 1
            if( e > 4 ):
                STATUS = '02'
                break
	
    if( e < 4 ):
        e = 0	
        s = ""
        MOD.sleep(50)
        s = ""
        while (s.find('OK')==-1):		
            MDM.send(EMAILTEXT, 0)
            MOD.sleep(20)
            MDM.sendbyte(26, 0)
            s = MDM.receive(150)
            e = e + 1
            if( e > 4 ):
                STATUS = '01'
                break
            
    EMAILLed(1)        
    if(e < 4 ):
        e = 0
        s = ""
        #EMAIL islemleri duzgunse 0 doner
        return '00' 
    else:
        e = 0
        #EMAIL islemleri sorunluysa STATUS degeri neyse oradaki AT komutlarý sýraýnda sorun cikmistir
        return STATUS

#EMAIL islemleri sorunluysa STATUS degeri neyse oradaki AT komutlarý sýraýnda sorun cikmistir

        
def ReadRegistry(filename):
    
    global SMSNO1
    global SMSNO2
    global TEMPMAX
    global TEMPMIN
    global SMTP_SERVER
    global SENDER_EMAIL_ADDR
    global SENDER_EMAIL_PASS
    global RECIEVER_EMAIL_ADDR1
    global RECIEVER_EMAIL_ADDR2
    global ADJPASSVALUE
    
    curr_posit=0
    SER.send(filename+'\r\n')
    try:
        MOD.sleep(5) 
        f=open(filename,"r+") 
        MOD.sleep(5) 
        f.seek(0)               #Dosyanýn en baþýna gel
        MOD.sleep(5) 
        Line = f.readlines() 
        
        SMSNO1_ = Line[0].split('#')
        SMSNO1 = SMSNO1_[1].strip()        
        SMSNO2_ = Line[1].split('#')
        SMSNO2 = SMSNO2_[1].strip()
        
        TEMPMAX_ = Line[2].split('#')
        TEMPMAX = TEMPMAX_[1].strip()
        TEMPMIN_ = Line[3].split('#')
        TEMPMIN = TEMPMIN_[1].strip()
        
        SMTP_SERVER_ = Line[4].split('#')
        SMTP_SERVER = SMTP_SERVER_[1].strip()
                                  
        SENDER_EMAIL_ADDR_ = Line[5].split('#')
        SENDER_EMAIL_ADDR = SENDER_EMAIL_ADDR_[1].strip()   
        SENDER_EMAIL_PASS_ = Line[6].split('#')
        SENDER_EMAIL_PASS = SENDER_EMAIL_PASS_[1].strip()
        
        RECIEVER_EMAIL_ADDR1_ = Line[7].split('#')
        RECIEVER_EMAIL_ADDR1 = RECIEVER_EMAIL_ADDR1_[1].strip()  
        RECIEVER_EMAIL_ADDR2_ = Line[8].split('#')
        RECIEVER_EMAIL_ADDR2 = RECIEVER_EMAIL_ADDR2_[1].strip()
        
        ADJPASS_ = Line[9].split('#')
        ADJPASS = ADJPASS_[1].strip() 
        ADJPASSVALUE = int(ADJPASS)
        MOD.sleep(5) 
        f.flush()  
        f.close()
        return 1
    except : 
        v=sys.exc_info()
        return 0

        
def WriteRegistry(filename,WhichLine,Data):
    curr_posit=0
    try:
        f=open(filename,"r+")
        f.seek(0)               #Dosyanýn en baþýna gel
        
        MOD.sleep(20)
        for num in range(0,(WhichLine+1)):
            DUMM__ = f.readline()
        
        SER.send(DUMM__+ '\r\n')
        CurrPosition_ = DUMM__.split('#')
        if(len(CurrPosition_[0]) == 0):
            f.close()
            return -1
        CurrPosition = len(CurrPosition_[0])
        f.seek(0)
        if(WhichLine != 0):
            for num in range(0,(WhichLine)):
                DUMM__ = f.readline()
        f.seek((CurrPosition+1),1)
        f.write(Data)
        f.flush()
        f.close()
        return 1
    except : 
        v=sys.exc_info()
        return 0

def ReadTemp():
    TempMv = GPIO.getADC(1)
       
    if(TempMv == -1):
        return -1

    K1 = 765                       #gerilim bölücü
    K2 = 100
    Temp = (((TempMv*K1)/K2)-2713)/10
    
    return Temp

def TempControl(value,max_,min_):
    minimum = int(min_)
    maximum = int(max_)    
    
    if(value > maximum):
        return 1
    if(value < minimum):
        return 2
    
    return 0


#Gelen SMS i ayristirip test.txt dosyasina kayitlar yapiliyor. Gonderilen sms asagidaki gibi yapilmalidir.
#%%%%*1 05%%%%%%%%% 05%%%%%%%%%*2 45 05*3 %%%%%%%%%%%%%%%%%%%%@hotmail.com %%%%%%%%%%%%%%%%%%%%@yandex.com*4 %%%%%%%%*5 %%%%
def parseANDsave(data):
    #Gelen sms i ayýr ve *.txt dosyasýna kaydet
    SMSDATA = data.split('*')
    Password_ = SMSDATA[0].strip()

    #Password u karsilastir.
    Password = int(Password_)
    if( Password != ADJPASSVALUE):
        SER.send('ERROR\r\n')
        return -1

    for num in range(1,len(SMSDATA)):
        if(SMSDATA[num].find(' ') != -1):
            Seg = SMSDATA[num].split(' ')    
            if( Seg[0].strip() == '1'):
                Dummies = SMSDATA[1].split(' ')  
                WriteRegResp = WriteRegistry('test'+'.txt',0,Dummies[1])
                SER.send('KAYIT 1\r\n')
            if( Seg[0].strip() == '2'):
                Dummies = SMSDATA[1].split(' ')  
                WriteRegResp = WriteRegistry('test'+'.txt',1,Dummies[1])
                SER.send('KAYIT 2\r\n')
            if( Seg[0].strip() == '3'):
                Dummies = SMSDATA[1].split(' ')  
                WriteRegResp = WriteRegistry('test'+'.txt',2,Dummies[1])
                SER.send('KAYIT 3\r\n')
            if( Seg[0].strip() == '4'):
                Dummies = SMSDATA[1].split(' ')  
                WriteRegResp = WriteRegistry('test'+'.txt',3,Dummies[1])
                SER.send('KAYIT 4\r\n')
            if( Seg[0].strip() == '5'):
                Dummies = SMSDATA[1].split(' ')  
                WriteRegResp = WriteRegistry('test'+'.txt',4,Dummies[1])
                SER.send('KAYIT 5\r\n')

        
    if(WriteRegResp != 1):
        SER.send('ERROR\r\n')
    else:
        SER.send('OK\r\n')
        return 1
        
    return 0
    




#---------------------------------------------------------------------
#-----------------------------MAIN MENU-------------------------------

#Baudrate i ayarlama iþlemi 
SER.set_speed('9600','8N1')

#Tum Led leri sondur
DUMM = GPIO.setIOvalue(6,1)
DUMM = GPIO.setIOvalue(7,1)
DUMM = GPIO.setIOvalue(8,1)
DUMM = GPIO.setIOvalue(5,0)

#Program ilk açýldýðýnda seri port tan telit modeme baðlýysan STATUS? gelidiðinde script çalýþmýþ demektir.
a = SER.send('STATUS?\r\n')                     

#Normal çalýþma esnasýnda SMS gelirse PopUp þeklinde (MESAJ GELDI=x, x->Kacinci sms) calismasini saglar.
TELRESP3 = LISTEN_SMS()
MOD.sleep(20)
SER.send('LSMS=' + TELRESP3 + '\r\n')
MOD.sleep(20)

#test.txt isimli dosya telit modulunun icerisinde olmalidir. Ilk aciliste bu dosya okunur ve tum kayitlar ram bellege alinir.
fileResp = ReadRegistry('test'+'.txt')
MOD.sleep(20)

#Seri port a bagli olundugunda acilista bir seferligine asagidaki degerleri seri port tan yazar.
SER.send(SMSNO1+'\r\n')
SER.send(TEMPMAX+'-'+TEMPMIN+'\r\n')
SER.send(SMTP_SERVER+'\r\n')
SER.send(SENDER_EMAIL_ADDR+'\r\n')
SER.send(SENDER_EMAIL_PASS+'\r\n')
SER.send(RECIEVER_EMAIL_ADDR1+'\r\n')

#test.txt dosyasi duzgun acildiysa seri port tan OK veya hata varsa ERROR yazar.
if(fileResp == 1):
    SER.send('OK\r\n')
    #normal çalýþma
else:
    SER.send('ERROR\r\n')
    #ledlerin hepsini yak


ExTempValue = 0
while(1==1):
    TempValue = ReadTemp()
    if(TempValue == -1):
        #Sicaklik degeri okunamiyorsa seri port tan ERROR gonderir.Istenirse LED ler yakýlýr, vb.
        SER.send('ERROR\r\n')
    else:
        #Seri port tan Sicaklik degeri yazilir.
        SER.send(str(TempValue)+'\r\n')

        #Olculen deger test.txt dosyasindeki TEMPMAX ve TEMPMIN degerleri disindaysa TempControlValue degeri '0' olmaz.
        TempControlValue = TempControl(TempValue,TEMPMAX,TEMPMIN)
        if(TempControlValue != 0):
            #Olculen deger sinirlar disindaysa BILDIRME islemlerini yapar. Bu islemler degisim oldugunda yapilmasi gerekir.
            if(TempValue != ExTempValue):
                ControlStatus = 0

            #BILDIRME islemleri burada yapiliyor. ALARM durumu olustu.
            if(ControlStatus == 0):
                ALARMLed(0)
                ExTempValue = TempValue
                ControlStatus = 1
                SER.send('SENDING REPORT..\r\n')
                MOD.sleep(50)
                
                #SMSNO1 (test.txt de kayitli) e "AMBIENT TEMPRATURE xx Celsius" seklide SMS atiliyor. Ýstenirse 2. kayitlara SMS atilabilir.
                SMSCONTROL = SMS(SMSNO1,"AMBIENT TEMPRATURE : "+str(TempValue)+" Celsius")
                MOD.sleep(50)
                
                #test.txt de kayitli email adreslerine EMAIL atiyor.
                CEVAP = EMAIL(SMTP_SERVER,SENDER_EMAIL_ADDR,SENDER_EMAIL_PASS,SENDER_EMAIL_ADDR,RECIEVER_EMAIL_ADDR1,"ALARM","AMBIENT TEMPRATURE : "+str(TempValue)+" Celsius")
                if(CEVAP != '0'):
                    MOD.sleep(50)
                    #EMAIL ilkinde atamazsa 2. seferde atar.
                    CEVAP = EMAIL(SMTP_SERVER,SENDER_EMAIL_ADDR,SENDER_EMAIL_PASS,SENDER_EMAIL_ADDR,RECIEVER_EMAIL_ADDR1,"ALARM","AMBIENT TEMPRATURE : "+str(TempValue)+" Celsius")
                SER.send(CEVAP + '\r\n')
        else:
            #Her sey NORMAL e dondugunde NORMAL a dondu sms ve email i atilir.
            if(ControlStatus == 1):
                ALARMLed(1)
                ControlStatus = 0
                SER.send('SENDING REPORT..\r\n')
                MOD.sleep(50)   
                SMSCONTROL = SMS(SMSNO1,"AMBIENT TEMPRATURE : "+str(TempValue)+" Celsius\r\n AMBIENT TEMPERATURE is NORMAL")
                MOD.sleep(50)   
                CEVAP = EMAIL(SMTP_SERVER,SENDER_EMAIL_ADDR,SENDER_EMAIL_PASS,SENDER_EMAIL_ADDR,RECIEVER_EMAIL_ADDR1,"ALARM","AMBIENT TEMPRATURE : "+str(TempValue)+" Celsius\r\n AMBIENT TEMPERATURE is NORMAL")
                if(CEVAP != '0'):    
                    MOD.sleep(50)          
                    CEVAP = EMAIL(SMTP_SERVER,SENDER_EMAIL_ADDR,SENDER_EMAIL_PASS,SENDER_EMAIL_ADDR,RECIEVER_EMAIL_ADDR1,"ALARM","AMBIENT TEMPRATURE : "+str(TempValue)+" Celsius\r\n AMBIENT TEMPERATURE is NORMAL")
                SER.send(CEVAP + '\r\n')
                MOD.sleep(10)   

    #MODUL den gelen datalar (AT komut modulu ile Script modulu arasindaki baglanti)
    uGetCharFromMDM = MDM.read()
    
    if( uGetCharFromMDM != "" ):
        #SMS PopUp i
        if( uGetCharFromMDM.find('+CMTI:') != -1 ):
            SmsPopUp = uGetCharFromMDM.split(',')
            SER.send('MESAJ GELDI=' + SmsPopUp[1].strip() + '\r\n')

            #Ayar SMS ini ayristirir.            
            SMSRESP1 = SMS_READ(SmsPopUp[1].strip())
            SER.send(SMSRESP1 + '\r\n')
            SER.send(ADJTELNO + '\r\n')
            ParseSMSResp = parseANDsave(SMSRESP1)
            MOD.sleep(20)
            #Yeni kayitlar yapidiysa ya da yapilamadiysa durum sms i gonderilir.
            if(ParseSMSResp == 1):
                SMSCONTROL = SMS(ADJTELNO,"NEW ADJUSTMENT IS OK")
                MOD.sleep(10)   
            else:                
                SMSCONTROL = SMS(ADJTELNO,"NEW ADJUSTMENT IS FAULT")
                
            fileResp = ReadRegistry('test'+'.txt')
            SER.send(SMSNO1+'\r\n')
            SER.send(SMSNO2+'\r\n')

            #5 ten fazla SMS varsa tum SMS leri temizle SMS birikmesin            
            if(int(SmsPopUp[1].strip()) > 5):
                SMS_DEL_ALL()
            uGetCharFromMDM = ""
        else:
            uGetCharFromMDM = ""
     

    #PC den gelen datalar    
    uGetChar = SER.read()       
   
    if((uGetChar == '\r') or (uGetChar == '\n')):
        SER.send(uResp+'\r\n')

        #Seri porttan END gonderirsek Script i durdurur. Modul normal AT komutlariyla seriport tan calisir hale gelir.        
        if(uResp.find('END') != -1):
            SER.send('OK\r\n')
            uResp = ""
            break
    else:
        uResp = uResp + uGetChar
        SER.send(uGetChar)


SMSLed(1)
MOD.sleep(50)
SMSLed(0)
ALARMLed(0)
EMAILLed(0)
#END ile script susar.
SER.send('END\r\n')

