import operator
import sys
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from .models import Messages,Mail,Orders
#For machine Learning Model
import numpy 
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import cx_Oracle
import os
import datetime

user = ""


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        role = request.POST['role']

        if(pass1==pass2):
            Myuser = User.objects.create_user(username,pass1,role)
            Myuser.save()
            messages.success(request,'Account created!')
            return redirect("signin")

    return render(request, "signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username=username,password=pass1)
        print(user)
        if user is not None:
            #print("1")
            login(request,user)
            name = user.username
            role = user.email
            print(role)
            print("BATMAN!!")
            return render(request, 'index.html', {'username': name})

        else:
            #print("2")
            messages.error(request, 'Bad credentaials')

            return redirect('signin')
    #print("3")
    return render(request, "login.html")

def dashboard(request):
    if request.user.is_authenticated:
        name = request.user.username
        message = Messages.objects.all()
        mail = Mail.objects.all()
        # url1 = "https://app.powerbi.com/reportEmbed?reportId=7b0f05ea-60e4-4f2f-8b1f-422148f528bf&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9"
        # if request.user.first_name == 6:
        #     return render(request,'dashboard.html', {'username': name, 'url1': url1,"message" : message, "mail" : mail})
        if int(request.user.first_name) == 4:
            url1 = "https://app.powerbi.com/reportEmbed?reportId=2e2b275f-0933-4209-be03-485494cb4ce8&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9"
        elif int(request.user.first_name) == 5:
            url1 = "https://app.powerbi.com/reportEmbed?reportId=71933686-5cda-4456-86e9-b28a4c2e735e&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9"
        elif int(request.user.first_name) == 6 :
            url1 = "https://app.powerbi.com/reportEmbed?reportId=6229b756-5adb-487e-8440-af0b428f53b1&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9" 
        elif int(request.user.first_name) == 7:
            url1 = "https://app.powerbi.com/reportEmbed?reportId=d165ee75-94b7-4f19-8bb1-34f06bb54b3f&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9" 
        elif int(request.user.first_name) == 8:
            url1 = "https://app.powerbi.com/reportEmbed?reportId=a548249c-12db-4518-a893-83b6b3101c0e&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9"
        elif int(request.user.first_name) == 9:
            url1 = "https://app.powerbi.com/reportEmbed?reportId=6dca31f6-165b-4d01-8e29-086e15811e91&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9"
        elif request.user.username == "admin":
            url1 = "" 
        
        return render(request,'dashboard.html', {'username': name, 'url1': url1,"message" : message, "mail" : mail})
    else:
        return render(request, "login.html")
        

def index(request):
    if request.user.is_authenticated:
        name = request.user.username
        message = Messages.objects.all()
        mail = Mail.objects.all()
        return render(request, "index.html", {'username': name,"message" : message, "mail" : mail})
    else:
        return render(request, "login.html")

def details(request):
    if request.user.is_authenticated:
        #getting data from data base
        lib_dir = r"C:\Users\PSGH\Downloads\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3"
        try:
            cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\PSGH\Downloads\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3")
        except Exception as err:
            print("Error connecting: cx_Oracle.init_oracle_client()")
            print(err);
            
        
        cno=request.user.first_name
        dsn_tns = cx_Oracle.makedsn('172.17.100.250', '1521', 'POCDB12C')
        conn = cx_Oracle.connect(user='PAO', password='PAO', dsn=dsn_tns)
        if cno == 6:
            q="SELECT PHRVAA_DRUG_CODE,PHRVAA_DRUG_NAME,PHRVAA_COUNTER,PHRVAA_CURR_QTY,PHRVAB_CATG_DESC,PHRVAD_DRUG_TYPE FROM phrvah_drug_name_view order by PHRVAA_COUNTER"
            print(q)
            with conn.cursor() as cursor:
                cursor.execute(q)
                from pandas import DataFrame
                df = DataFrame(cursor.fetchall())
                df.columns = [x[0] for x in cursor.description]
                print("I got %d lines " % len(df))
            df
            data=df
            dcode=df["PHRVAA_DRUG_CODE"].to_list()
            dname=df["PHRVAA_DRUG_NAME"].to_list()
            dcntr=df["PHRVAA_COUNTER"].to_list()
            dqty=df["PHRVAA_CURR_QTY"].to_list()
            dcatg=df["PHRVAB_CATG_DESC"].to_list()
            dtype=df["PHRVAD_DRUG_TYPE"].to_list()
            df = numpy.array(df)
            print(df)
            name = request.user.username
            message = Messages.objects.all()
            mail = Mail.objects.all()
            return render(request,'details.html', {'username': name,"message" : message, "mail" : mail, "df": df,"dcode":dcode, "dname":dname, "dcntr":dcntr, "dqty":dqty, "dcatg":dcatg, "dtype":dtype})

        if cno != 6:
            q="SELECT PHRVAA_DRUG_CODE,PHRVAA_DRUG_NAME,PHRVAA_CURR_QTY,PHRVAB_CATG_DESC,PHRVAD_DRUG_TYPE FROM phrvah_drug_name_view WHERE PHRVAA_COUNTER="+str(cno)
            print(q)
            with conn.cursor() as cursor:
                cursor.execute(q)
                from pandas import DataFrame
                df = DataFrame(cursor.fetchall())
                df.columns = [x[0] for x in cursor.description]
                print("I got %d lines " % len(df))
            df
            dcode=df["PHRVAA_DRUG_CODE"].to_list()
            dname=df["PHRVAA_DRUG_NAME"].to_list()
            dqty=df["PHRVAA_CURR_QTY"].to_list()
            dcatg=df["PHRVAB_CATG_DESC"].to_list()
            dtype=df["PHRVAD_DRUG_TYPE"].to_list()
        bill_date = []
        df = numpy.array(df)
        print(df[0])
        name = request.user.username
        message = Messages.objects.all()
        mail = Mail.objects.all()
        return render(request,'details.html', {'username': name,"message" : message, "mail" : mail, "df" : df})
    else:
        return render(request, "login.html")
    

def alerts(request):
    if request.user.is_authenticated:
        name = request.user.username
        message = Messages.objects.all()
        mail = Mail.objects.all()
        for m in message:
            if request.user.username == "admin":
                print("its me ",request.user)
                return render(request, 'alerts.html', {'username': name,"message" : message, "mail" : mail})
            elif request.user.first_name == m.to_user:
                print(request.user.first_name)
                return render(request, 'alerts.html', {'username': name,"message" : message, "mail" : mail})
        return render(request, 'alerts.html', {'username': name})
            # else:
            #     m.message = "No messages"
            #     print("No messages")
            #     return render(request, 'alerts.html', {'username': name,"message" : message})

    else:
        return render(request, "login.html")
    

def requests(request):
    if request.user.is_authenticated:
        name = request.user.username
        message = Messages.objects.all()
        mail = Mail.objects.all()
        for m in mail:
            if request.user.username == "admin" or request.user.username == "store_pharmacy":
                print("its me ",request.user)
                return render(request, 'requests.html', {'username': name,"mail" : mail,"message" : message})
            elif request.user.username == m.to_user:
                return render(request, 'requests.html', {'username': name,"mail" : mail,"message" : message})
        return render(request, 'requests.html', {'username': name})
        
    else:
        return render(request, "login.html")
    
def mailCompose(request):
    if request.user.is_authenticated:
        name = request.user.username
        message = Messages.objects.all()
        mail = Mail.objects.all()
        return render(request, 'mail.html', {'username': name,"message" : message, "mail" : mail})
    else:
        return render(request, "login.html")
    
def sendMail(request):
    name = request.user.username
    if request.method == "POST":
        my_mail = Mail()
        my_mail.from_user =request.POST['from_user']
        my_mail.to_user = request.POST['to_user']
        my_mail.body = request.POST['body']
        my_mail.time= datetime.datetime.now()
        my_mail.save()


    return redirect('requests')

# def alerts_info(request):
#     if request.user.is_authenticated:
#         name = request.user.username
#         message = Messages.objects.all()
#         mail = Mail.objects.all()
#         return render(request, 'alerts-info.html', {'username': name,"message" : message, "mail" : mail})
#     else:
#         return render(request, "login.html")

def orders(request):
    if request.user.is_authenticated and request.user.username == "store_pharmacy":
        name = request.user.username
        message = Messages.objects.all()
        mail = Mail.objects.all()
        return render(request, 'orders.html', {'username': name,"message" : message, "mail" : mail})
    elif request.user.is_authenticated:
          return render(request, "index.html", {'username': name,"message" : message, "mail" : mail})
    else:
        return render(request, "login.html")


def messaiah(request):
    
    if request.user.is_authenticated:
        message = Messages.objects.all()
        for m in message:
            if request.user.username == m.to_user:
                print("its me ",request.user)
                return render(request, "m.html",context={"message" : message})
    else:
        return render(request, "login.html")
# need to add
def get_orders(request):
    if request.user.is_authenticated:
        ud_code = []
        alerts = Messages.objects.all()
        
        try:
            o = Orders.objects.all()
            o.delete()
        except:
            print()
        for a in alerts:
            ud_code.append(a.drug_code)
        ud_code = numpy.array(ud_code)
        ud_code = list(numpy.unique(ud_code))
        print(ud_code)
        for i in ud_code:
            demand = 0
            rol = 0

            for a in alerts:
                if a.drug_code == i:
                    name = a.drug_name
                    demand += a.demand
                    rol += a.rol
            
            ord = Orders()
            ord.drug_code = i
            ord.drug_name = a.drug_name
            ord.current_quantity = a.current_quantity # need to get current_qty from database
            ord.demand = demand
            ord.rol= rol
            
            ord.save()

            orders = Orders.objects.all()
        # df.groupby(["drug_code"]).sum()   
        # messages = Messages.objects.all()
        # orders.delete()
        # d_codes = messages.objects.values('drug_code').distinct()
        # for m1 in d_codes:
        #     for m2 in messages:
        #         dugInOrd = Orders.objects.get(name=m1)
        #         if request.user.username == m.to_user:
        #             return render(request, "oders.html",context={"orders" : orders})
        return render(request, "orders.html",context={"orders" : orders})
    else:
        return render(request, "login.html")

def ml_predict(request):
    if request.user.is_authenticated:
        a = Messages.objects.all()
        a.delete()
        print("Machine is taking over now!")
        ib_dir = r"C:\Users\PSGH\Downloads\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3"
        try:
            cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\PSGH\Downloads\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3")
        except Exception as err:
            print("Error connecting: cx_Oracle.init_oracle_client()")
            print(err);
        cno=request.user.first_name
        dsn_tns = cx_Oracle.makedsn('172.17.100.250', '1521', 'POCDB12C')
        conn = cx_Oracle.connect(user='PAO', password='PAO', dsn=dsn_tns)
        q="SELECT PHRVAA_DRUG_CODE FROM \"PAO\".\"PHRVAA_DRUG_MASTER_VIEW\" WHERE phrvaa_counter="+cno
        print(q)
        with conn.cursor() as cursor:
                cursor.execute(q)
                from pandas import DataFrame
                dnf = DataFrame(cursor.fetchall())
                dnf.columns = [x[0] for x in cursor.description]
        dnf=dnf.to_numpy()
        dnf=dnf.flatten()
        for i in dnf:
            cals1drug(i,request.user.first_name,request)
        name = request.user.username
        return render(request, 'alerts.html', {'username': name})

    else:
        return render(request, "login.html")

def cals1drug(dcode,cno,request):
        
        #Choosing drug code and counter number
        # dcode="SHEL002"
        # cno=request.user.first_name
        try:
            dsn_tns = cx_Oracle.makedsn('172.17.100.250', '1521', 'POCDB12C')
            conn = cx_Oracle.connect(user='PAO', password='PAO', dsn=dsn_tns)
            # q="select PHRVAD_BILL_DATE , sum(phrvad_sal_qty) from \"PAO\".\"PHRVAD_FOOT_FALLX\" where phrvad_counter_no=4 and phrvad_drug_code='ATRO006' group by PHRVAD_BILL_DATE order by TO_DATE(phrvad_bill_date, 'dd-mm-yyyy')"
            q="select PHRVAD_BILL_DATE , sum(phrvad_sal_qty) from \"PAO\".\"PHRVAD_FOOT_FALLX\" where phrvad_counter_no="+str(cno)+" and phrvad_drug_code='"+dcode+"' group by PHRVAD_BILL_DATE order by TO_DATE(phrvad_bill_date, 'dd-mm-yyyy')"
            print(q)
            with conn.cursor() as cursor:
                cursor.execute(q)
                from pandas import DataFrame
                df = DataFrame(cursor.fetchall())
                df.columns = [x[0] for x in cursor.description]
                print("I got %d lines " % len(df))
        except:
            return
        
        start = datetime.datetime.strptime("05-05-2021", "%d-%m-%Y")
        end = datetime.datetime.strptime("26-03-2022", "%d-%m-%Y")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
        dl=[]
        for date in date_generated:
            dl.append(date.strftime("%d-%m-%Y"))

        df.PHRVAD_BILL_DATE.tolist()
        nli=[]
        for i in dl:
            if i not in df.PHRVAD_BILL_DATE.tolist():
                # print(i)
                nli.append(i)
            # if i=="03-09-2021":
            #     print("hi")
        print(len(nli))
        listofzeros = [0] * len(nli)
        df2 = pd.DataFrame({"PHRVAD_BILL_DATE":nli,
                            "SUM(PHRVAD_SAL_QTY)":listofzeros})
        df3=pd.concat([df,df2])

        print(type(df3.PHRVAD_BILL_DATE[0]))
        df3['PHRVAD_BILL_DATE']=pd.to_datetime(df3['PHRVAD_BILL_DATE'],dayfirst=True,format='%d-%m-%y', infer_datetime_format=True)
        print(type(df3.PHRVAD_BILL_DATE[0]))

        df4=df3.sort_values(by='PHRVAD_BILL_DATE')

        df4.reset_index(drop=True, inplace=True)

        # fix random seed for reproducibility
        numpy.random.seed(7)

        df5=df4['SUM(PHRVAD_SAL_QTY)']

        dataset=df5.values
        dataset = dataset.astype('float32')

        dataset=dataset.reshape(-1, 1)

        # normalize the dataset
        scaler = MinMaxScaler(feature_range=(0, 1))
        dataset = scaler.fit_transform(dataset)

        # split into train and test sets
        train_size = int(len(dataset))
        train= dataset[0:train_size,:]
        print(len(train))

        # create_dataset(dataset, look_back=1) #not too sure
        # reshape into X=t and Y=t+1
        look_back = 14
        trainX, trainY = create_dataset(train, look_back)

        # reshape input to be [samples, time steps, features]
        trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))

        # create and fit the LSTM network
        model = Sequential()
        model.add(LSTM(4, input_shape=(1, look_back)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam' , metrics=['accuracy'])
        model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)

        # make predictions
        ypred = model.predict(trainX)

        ypred = ypred.reshape(ypred.shape[0], 1, ypred.shape[1])

        #rebuild test set for inverse transform
        pred_test_set = []
        for index in range(0,30):
            numpy.concatenate([ypred[index],trainX[index]],axis=1)
            pred_test_set.append(numpy.concatenate([ypred[index],trainX[index]],axis=1))

        #reshape pred_test_set
        pred_test_set = numpy.array(pred_test_set)
        pred_test_set = pred_test_set.reshape(pred_test_set.shape[0], pred_test_set.shape[2])

        #inverse transform
        pred_test_set_inverted = scaler.inverse_transform(pred_test_set)

        start = datetime.datetime.strptime("27-03-2022", "%d-%m-%Y")
        end = datetime.datetime.strptime("28-04-2022", "%d-%m-%Y")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
        d2=[]
        for date in date_generated:
            d2.append(date.strftime("%d-%m-%Y"))

        # pred_test_set_inverted #not sure
        len(pred_test_set_inverted)

        len(d2)

        #create dataframe that shows the predicted sales
        result_list = []
        sales_dates = d2

        for index in range(0,len(pred_test_set_inverted)):
            result_dict = {}
            result_dict['pred_value'] = int(pred_test_set_inverted[index][0] )
            result_dict['date'] = sales_dates[index+1]
            result_list.append(result_dict)
        df_result = pd.DataFrame(result_list)

        df_result.set_index(['date'],inplace=True,drop=True)

        # df_result.plot() #not sure

        avgsales=sum(df_result['pred_value'].to_list())
        sum(df4['SUM(PHRVAD_SAL_QTY)'].to_list())/12

        dsn_tns = cx_Oracle.makedsn('172.17.100.250', '1521', 'POCDB12C')
        conn = cx_Oracle.connect(user='PAO', password='PAO', dsn=dsn_tns)
        # q="select PHRVAD_BILL_DATE , sum(phrvad_sal_qty) from \"PAO\".\"PHRVAD_FOOT_FALLX\" where phrvad_counter_no=4 and phrvad_drug_code='ATRO006' group by PHRVAD_BILL_DATE order by TO_DATE(phrvad_bill_date, 'dd-mm-yyyy')"
        q="select * from \"PAO\".\"PHRVAI_ORDDATE_VIEW\" where phrvai_drug_code='"+dcode+"'"

        with conn.cursor() as cursor:
            cursor.execute(q)
            from pandas import DataFrame
            dxf = DataFrame(cursor.fetchall())
            dxf.columns = [x[0] for x in cursor.description]
            print("I got %d lines " % len(df))
        print(q)

        x=dxf.PHRVAI_INWD_DATE[0]- dxf.PHRVAI_ORD_DATE[0]
        x.days
        x=[]
        
        for i in range(len(dxf.index)):
            x.append((dxf.PHRVAI_INWD_DATE[i]- dxf.PHRVAI_ORD_DATE[i]).days)
        
        avg=sum(x)/len(x)
        avg

        leadtime=avg/30

        rol=avgsales*leadtime

        q="select PHRVAF_CURR_QTY from \"PAO\".\"PHRVAF_STOCK_ANALYSIS_COUNTER\" where PHRVAF_DRUG_CODE='"+dcode+"' and PHRVAF_COUNT_NO="+str(cno)
        with conn.cursor() as cursor:
            cursor.execute(q)
            from pandas import DataFrame
            c=cursor.fetchall()
                
        c=list(c[0])
        cstock=c[0]

        if cstock<rol:
            print("Please request central store to place an order for drug code : "+str(dcode)+" , demand per month : "+str(avgsales)+" since the current stock is "+str(cstock)+" units , which is less than the re-order level"+str(math.floor(rol)))
            msg="Please request central store to place an order for drug code : "+str(dcode)+" , demand per month : "+str(avgsales)+" since the current stock is "+str(cstock)+" units , which is less than the re-order level"+str(math.floor(rol))

        new_msg = Messages()
        new_msg.message = msg
        if cno == 6:
            new_msg.from_user = cno
        else:
            new_msg.from_user = request.user.first_name
        new_msg.to_user = cno
        new_msg.time = datetime.date.today()
        new_msg.drug_code = str(dcode)
        new_msg.current_quantity = str(cstock)
        new_msg.demand = str(avgsales)
        new_msg.proposed_order_quantity = str(math.floor(rol))
        new_msg.save()
        print("ALERT SENT!!!")
        # if cno!=6:
        #     q="select PHRVAF_CURR_QTY from \"PAO\".\"PHRVAF_STOCK_ANALYSIS_COUNTER\" where PHRVAF_DRUG_CODE='"+dcode+"' and PHRVAF_COUNT_NO="+str(cno)
        #     with conn.cursor() as cursor:
        #         cursor.execute(q)
        #         from pandas import DataFrame
        #         c=cursor.fetchall()
        #     try:   
        #         c=list(c[0])
        #         cstock=c[0]
        #         alertflag=0
        #         if(c[0]<avgsales):
        #             alertflag=1
        #         else:
        #             alertflag=0
        #     except:
        #         print("exception")
        # else:
        #     q="select PHRVAE_CURR_QTY from \"PAO\".\"PHRVAE_STOCK_ANALYSIS_STORE\" where PHRVAE_DRUG_CODE='"+dcode+"' "
        #     print(q)
        #     with conn.cursor() as cursor:
        #         cursor.execute(q)
        #         from pandas import DataFrame
        #         c=cursor.fetchall()
                
        #     c=list(c[0])
        #     cstock=c[0]
        #     alertflag=0
        #     if(c[0]<avgsales):
        #         alertflag=1
        #     else:
        #         alertflag=0
        # if alertflag==0:
        #     print("sufficient quantity available for "+dcode)
        #     return
        # if alertflag==1:   
        #     print("alert to be sent!!!!!!")
        #     dsn_tns = cx_Oracle.makedsn('172.17.100.250', '1521', 'POCDB12C')
        #     conn = cx_Oracle.connect(user='PAO', password='PAO', dsn=dsn_tns)
        #     q="select PHRVAD_BILL_DATE , sum(phrvad_sal_qty) from \"PAO\".\"PHRVAD_FOOT_FALLX\" where phrvad_counter_no=4 and phrvad_drug_code='ATRO006' group by PHRVAD_BILL_DATE order by TO_DATE(phrvad_bill_date, 'dd-mm-yyyy')"
        #     q="select * from \"PAO\".\"PHRVAI_ORDDATE_VIEW\" where phrvai_drug_code='"+dcode+"'"

        #     with conn.cursor() as cursor:
        #         cursor.execute(q)
        #         from pandas import DataFrame
        #         dxf = DataFrame(cursor.fetchall())
        #         dxf.columns = [x[0] for x in cursor.description]
        #         print("I got %d lines " % len(df))
        #     print(q)

        # if alertflag==1:      
        #     x=dxf.PHRVAI_INWD_DATE[0]- dxf.PHRVAI_ORD_DATE[0]
        #     x.days
        #     x=[]
        
        #     for i in range(len(dxf.index)):
        #         x.append((dxf.PHRVAI_INWD_DATE[i]- dxf.PHRVAI_ORD_DATE[i]).days)

        # if alertflag==1:       
        #     avg=sum(x)/len(x)
        #     avg#not sure

        

        # if alertflag==1:   
        #   leadtime=avg/30
        
        # if alertflag==1:   
        #     if(cno!=6):
        #         q="select PHRVAF_MIN_ROL,PHRVAF_CURR_QTY from \"PAO\".\"PHRVAF_STOCK_ANALYSIS_COUNTER\" where PHRVAF_DRUG_CODE='"+dcode+"' and PHRVAF_COUNT_NO="+str(cno)
        #         with conn.cursor() as cursor:
        #             cursor.execute(q)
        #             from pandas import DataFrame
        #             c=cursor.fetchall()
        #         print(q)    
        #         c=list(c[0])
        #         c
        #     else:
        #         q="select PHRVAE_MIN_ROL,PHRVAE_CURR_QTY from \"PAO\".\"PHRVAE_STOCK_ANALYSIS_STORE\" where PHRVAE_DRUG_CODE='"+dcode+"' and PHRVAE_COUNT_NO="+str(cno)
        #         with conn.cursor() as cursor:
        #             cursor.execute(q)
        #             from pandas import DataFrame
        #             c=cursor.fetchall()
        #         print(q)    
        #         c=list(c[0])
        #         c #not sure
        #     minrol=c[0]
        #     print(c)

        # if alertflag==1:   
        #     dsn_tns = cx_Oracle.makedsn('172.17.100.250', '1521', 'POCDB12C')
        #     conn = cx_Oracle.connect(user='PAO', password='PAO', dsn=dsn_tns)
        #     # q="select PHRVAD_BILL_DATE , sum(phrvad_sal_qty) from \"PAO\".\"PHRVAD_FOOT_FALLX\" where phrvad_counter_no=4 and phrvad_drug_code='ATRO006' group by PHRVAD_BILL_DATE order by TO_DATE(phrvad_bill_date, 'dd-mm-yyyy')"
        #     q="select * from \"PAO\".\"PHRVAI_ORDDATE_VIEW\" where phrvai_drug_code='"+dcode+"'"

        #     with conn.cursor() as cursor:
        #         cursor.execute(q)
        #         from pandas import DataFrame
        #         dxf = DataFrame(cursor.fetchall())
        #         dxf.columns = [x[0] for x in cursor.description]
        #         print("I got %d lines " % len(df))
        #     dxf #not sure

        # if alertflag==1:       
        #     safetystock=c[0]

        # rol=avgsales*leadtime

        # if alertflag==1:   
        #     rol=avgsales*leadtime+safetystock
        #     if cno==6:
        #         msg = "Please place an order for drug code : "+str(dcode)+" , suggested quantity of order : "+str(math.floor(rol))+" since the demand per month is "+str(avgsales)+" units" +", which is less than the current stock "+str(cstock)
        #     else:
        #         msg = "Please request central store to place an order for drug code : "+str(dcode)+" , suggested quantity of order : "+str(math.floor(rol))+" since the demand per month is "+str(avgsales)+" units , which is less than the current stock "+str(cstock)

       
#ml func
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

def signout(request):
    logout(request)
    return redirect('signin')