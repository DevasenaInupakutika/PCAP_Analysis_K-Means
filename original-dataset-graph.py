import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

colors = ['red','green','blue','yellow','purple','pink']

def initial_plot():
    data = pd.read_csv("data/pcap_cleaned.csv",header = 0)
    Y = data['protocol_type']
    X = data['label']
    plt.scatter(X,Y,c='black')
    plt.xlabel("Attack Type")
    plt.ylabel("Protocol Type")
    plt.title("Original Dataset")
    plt.savefig("data/Initial_plt.png")
    plt.show()


if __name__ == "__main__":
    initial_plot()
