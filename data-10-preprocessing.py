#import statements

import pandas as pd
from time import time

#Data column names
col_names = ["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]

#Loading the  data
pcap_data = pd.read_csv("data/kddcup.data_10_percent", header=None, names = col_names)

#Structure of the data
pcap_data.describe()

print(pcap_data.tail(10))

#Checking how the labels are distributed
print(pcap_data['label'].value_counts())

#Printing unique values for columns with non-numeric values (for clustering purposes later on)
print("Values in protocol_type")
print(pcap_data.protocol_type.unique())

print("Values in service")
print(pcap_data.service.unique())

print("Values in flag")
print(pcap_data.flag.unique())

print("Values in labels")
print(pcap_data.label.unique())

#Converting the labels to 5 types with 4 types of attacks and normal packets.
pcap_data.loc[pcap_data['label'] == "buffer_overflow.",'label'] = "u2r"
pcap_data.loc[pcap_data['label'] == "ipsweep.",'label'] = "probe"
pcap_data.loc[pcap_data['label'] == "portsweep.",'label'] = "probe"
pcap_data.loc[pcap_data['label'] == "nmap.",'label'] = "probe"
pcap_data.loc[pcap_data['label'] == "satan.",'label'] = "probe"
pcap_data.loc[pcap_data['label'] == "loadmodule.",'label'] = "u2r"
pcap_data.loc[pcap_data['label'] == "perl.",'label'] = "u2r"
pcap_data.loc[pcap_data['label'] == "rootkit.",'label'] = "u2r"

pcap_data.loc[pcap_data['label'] == "back.",'label'] = "dos"
pcap_data.loc[pcap_data['label'] == "land.",'label'] = "dos"
pcap_data.loc[pcap_data['label'] == "neptune.",'label'] = "dos"
pcap_data.loc[pcap_data['label'] == "pod.",'label'] = "dos"
pcap_data.loc[pcap_data['label'] == "smurf.",'label'] = "dos"
pcap_data.loc[pcap_data['label'] == "teardrop.",'label'] = "dos"
pcap_data.loc[pcap_data['label'] == "ftp_write.",'label'] = "r21"

pcap_data.loc[pcap_data['label'] == "guess_passwd.",'label'] = "r21"
pcap_data.loc[pcap_data['label'] == "imap.",'label'] = "r21"
pcap_data.loc[pcap_data['label'] == "multihop.",'label'] = "r21"
pcap_data.loc[pcap_data['label'] == "phf.",'label'] = "r21"
pcap_data.loc[pcap_data['label'] == "spy.",'label'] = "r21"
pcap_data.loc[pcap_data['label'] == "ipsweep.",'label'] = "r21"


pcap_data.loc[pcap_data['label'] == "warezclient.",'label'] = "r21"
pcap_data.loc[pcap_data['label'] == "warezmaster.",'label'] = "r21"
pcap_data.loc[pcap_data['label'] == "normal.",'label'] = "normal"


print("New Values in labels")
print(pcap_data.label.unique())

#Converting the string valued features (column names) to numbers for clustering later on.
protocolType = pcap_data['protocol_type'].unique()
service1 = pcap_data['service'].unique()
flag1 = pcap_data['flag'].unique()
label1 = pcap_data['label'].unique()

p_val = {}
s_val = {}
f_val = {}
l_val = {}

#Protocol Type feature
k = 1
for i in protocolType:
    p_val[i] = k
    k = k+1

#Service Feature
k = 1
for i in service1:
    s_val[i] = k
    k = k+1

#Flag Feature
k = 1
for i in flag1:
    f_val[i] = k
    k = k+1

#Label Feature
k = 1
for i in label1:
    l_val[i] = k
    k = k+1

#Now updating the originally captured data
pcap_data["protocol_type"] = pcap_data['protocol_type'].apply(lambda x: p_val[x])
pcap_data["service"] = pcap_data["service"].apply(lambda x: s_val[x])
pcap_data["flag"] = pcap_data["flag"].apply(lambda x: f_val[x])
pcap_data["label"] = pcap_data["label"].apply(lambda x: l_val[x])

#For all other columns to required data formats


print(pcap_data['label'].head(10))


'''
#Checking for NaN values
print("NaN Values:")
for cols in pcap_data:
    if pcap_data[cols].isnull().any():
        print(cols)
'''

#Seems like no NaN values in any columns
#Moving this cleaned data to modified csv file for further processing
print(pcap_data.tail(10))

pcap_data.to_csv('data/pcap_cleaned_10percent.csv')
