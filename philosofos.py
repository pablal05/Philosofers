#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:06:26 2022

@author: mat
"""

from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager
import time
import random
from monitor import Table
NPHIL = 5
K = 10


def delay(n):
 time.sleep(random.randint(0,5))
 
 
def philosopher_task(num:int, table: Table):
 k=0
 table.set_current_phil(num)
 while k != K:
     print (f"Philosofer {num} thinking")
     print (f"Philosofer {num} wants to eat")
     table.wants_eat(num)
     print (f"Philosofer {num} eating")
     table.wants_think(num)
     print (f"Philosofer {num} stops eating")
     
     k += 1
     #print(f'philosofo {num} con bucle {k}')
     
def main():
 manager = Manager()
 table = Table(NPHIL, manager)
 philosofers = [Process(target=philosopher_task, args=(i,table)) \
                for i in range(NPHIL)]
 for i in range(NPHIL):
     philosofers[i].start()
 for i in range(NPHIL):
     philosofers[i].join()
     
if __name__ == '__main__':
 main()