from django.conf import settings
import json
from email.message import Message
import operator
import sys
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from psg_pharmacy.models import Messages,Mail,Orders
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

# def schedule_api():
#     print("OKAY")

def schedule_api():
    l = [8,5,9,7,4,11]
    for x in l:
        x = str(x)
        a = Messages.objects.filter(from_user=x)
        a.delete()
        print("Machine is taking over now!")
        ib_dir = r"C:\Users\PSGH\Downloads\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3"
        try:
            cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\PSGH\Downloads\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3")
        except Exception as err:
            print("Error connecting: cx_Oracle.init_oracle_client()")
            print(err);
        cno=x
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
            cals1drug(i,x)

def cals1drug(dcode,cno):
        
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
            
        print(q)

        x=dxf.PHRVAI_INWD_DATE[0]- dxf.PHRVAI_ORD_DATE[0]
        x.days
        x=[]
        
        for i in range(len(dxf.index)):
            x.append((dxf.PHRVAI_INWD_DATE[i]- dxf.PHRVAI_ORD_DATE[i]).days)
        
        avg=sum(x)/len(x)
        avg

        leadtime=avg/30

        rol=(avgsales*leadtime)+(avgsales*2/3)

        q="select PHRVAF_CURR_QTY from \"PAO\".\"PHRVAF_STOCK_ANALYSIS_COUNTER\" where PHRVAF_DRUG_CODE='"+dcode+"' and PHRVAF_COUNT_NO="+str(cno)
        with conn.cursor() as cursor:
            cursor.execute(q)
            from pandas import DataFrame
            c=cursor.fetchall()
                
        c=list(c[0])
        cstock=c[0]

        # if cstock<rol:
        if cstock>rol:
            q="select UNIQUE(PHRVAA_DRUG_NAME) from \"PAO\".\"PHRVAA_DRUG_MASTER_VIEW\" where phrvaa_drug_code = '"+str(dcode)+"'"
            with conn.cursor() as cursor:
                cursor.execute(q)
                from pandas import DataFrame
                c=cursor.fetchall()
            name=list(c[0])
            name=str(c[0][0])
            print(c,name,list(c))
            print("Please request central store to place an order for drug code : "+str(dcode)+" , demand per month : "+str(avgsales)+" since the current stock is "+str(cstock)+" units , which is less than the re-order level"+str(math.floor(rol)))
            msg="Please request central store to place an order for drug code : "+str(dcode)+" , demand per month : "+str(avgsales)+" since the current stock is "+str(cstock)+" units , which is less than the re-order level"+str(math.floor(rol))

            new_msg = Messages()
            new_msg.message = msg
            if cno == 6:
                new_msg.from_user = cno
            else:
                new_msg.from_user = cno 
            new_msg.to_user = cno
            new_msg.time = datetime.date.today()
            new_msg.drug_code = str(dcode)
            new_msg.drug_name=name
            new_msg.current_quantity = str(cstock)
            new_msg.demand = str(avgsales)
            new_msg.rol = str(math.floor(rol))
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