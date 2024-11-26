import tkinter as tk
from tkinter import *
from tkinter import ttk

from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *
from Plot import *

def creat_redtogreen_hexcolorlist():
        # Define the sequence of colors and texts
        colors_list = ['#FF0000',
                        '#FF1A1A',
                        '#FF3333', 
                        '#FF4D4D', 
                        '#FF6666', 
                        '#FF8080', 
                        '#FF9999', 
                        '#FFB3B3', 
                        '#FFCCCC', 
                        '#FFE6E6', 
                        '#FFFFFF',
                        '#E6F2E6',
                        '#CCE6CC',
                        '#B3D9B3',
                        '#99cc99',
                        '#80C080',
                        '#66B366',
                        '#4DA64D',
                        '#339933',
                        '#1A8D1A',
                        '#008000']
        
        return colors_list


def creat_standard_timeframelist():
        # Define a list that contain the standard timeframe that metatrader functions accept 
        timeframe_list = ['1m',
                       '2m',
                       '3m']
        
        return timeframe_list

login_1 = metatrader(51735591,'Wy7v5r4hu','Alpari-MT5-Demo')
login_1.start_mt5()