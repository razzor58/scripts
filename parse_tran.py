import sys
import time
import codecs
tran_str = open(sys.argv[1])
tran = {"PassDate":None,"Pan16":None,"SN":None,"Amount":None,"Zn_in":None,"Zn_out":None,"TripNo":None,"Tarif_type":None}
header = dict()
for line in tran_str:
    for s in range(len(line)):
        if line[s:s+2]=="2F":            
            tag_num = line[s+2:s+4]            
            if tag_num == "02":                 
                 route_num = line[s+6:s+6+int(line[s+4:s+6],16)*2]
                 ##header["RouteNum"]=codecs.decode(route_num,"hex").decode("866")
            #elif tag_num == "01":                
            #     res["HEADER_LEN"]=int(line[s+6:s+10],16)                                                       
            elif tag_num == "03":
                 con = line[s+6:s+6+int(line[s+4:s+6],16)*2]
                 ##header["Conductor"]=codecs.decode(con,"hex").decode("866")                                                                               
            elif tag_num == "04":
                 ext = line[s+6:s+6+int(line[s+4:s+6],16)*2]
                 ##header["ExtInfo"]=codecs.decode(ext,"hex").decode("866")
            elif tag_num == "05":
                 print("{:*<50}".format(""))
                 #tran["TType"]=int(line[s+10:s+12],16)
                 tran["Pan16"]=line[s+12:s+28]
                 #tran["DataVers"]=line[s+28:s+30]
                 #tran["TicketID"]=line[s+30:s+42]
                 ##tran["Tarif_type"]=codecs.decode(line[s+42:s+44],"hex").decode("866")
                 tran["Amount"]=int(line[s+46:s+48] + line[s+44:s+46],16)
                 tran["SN"]=line[s+48:s+62].rstrip("0")
                 tran["PassDate"]=line[s+68:s+70]+":"+line[s+70:s+72]+":"+line[s+72:s+74]+" " +line[s+66:s+68]+"."+line[s+64:s+66]+"."+line[s+62:s+64]
                 tran["TripNo"]=line[s+74:s+76]
                 #tran["TariffIndex"]=line[s+76:s+78]
                 #tran["PppTermId"]=int(line[s+84:s+86]+line[s+82:s+84]+line[s+80:s+82]+line[s+78:s+80],16)
                 #tran["KeyId"]=line[s+86:s+88]
                 #tran["CrDate"]=time.ctime(int(line[s+94:s+96]+line[s+92:s+94]+line[s+90:s+92]+line[s+88:s+90],16))
                 #tran["CounterVal"]=line[s+102:s+104]+line[s+100:s+102]+line[s+98:s+100]+line[s+96:s+98]
                 #tran["ExpDate"]=int(line[s+106:s+108]+line[s+104:s+106],16)
                 #tran["S_Date"]=int(line[s+110:s+112]+line[s+108:s+110],16)
                 #tran["E_Date"]=int(line[s+114:s+116]+line[s+112:s+114],16)                 
                 #tran["Oper"]=int(line[s+116:s+118],16)
                 tran["Zn_in"]=int(line[s+118:s+120],16)
                 tran["Zn_out"]=int(line[s+120:s+122],16)
                 ext_info_len = int(line[s+124:s+126]+line[s+122:s+124],16)
                 #res["tran_ext_info"] = line[s+126:s+126+ext_info_len*2]
                 #continue
                 print("\n".join(["{:15}:{:<5}".format(key,value) for key,value in tran.items()]))                 
            elif tag_num == "06":
                 st = line[s+6:s+6+int(line[s+4:s+6],16)*2]
                 header["St_id"]=int(st,16)
                 #int(line[s+4:s+8],16)
print("{:*<50}".format(""))
print("Header")
print("{:*<50}".format(""))
print("\n".join(["{:15}:{:<5}".format(key,value) for key,value in header.items()]))
                  
