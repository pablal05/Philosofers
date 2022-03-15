#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:18:50 2022

@author: mat
"""
from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Value
from multiprocessing import current_process
import time, random

class Table():
    def __init__(self, nphil, manager):
        self.phil = manager.list( [False]*nphil)
        self.eating = Value('i',0)
        self.actual = None
   
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
        
    def set_current_phil(self,i):
        self.actual = i
        
    def vecinos_libres(self):
        i = self.actual
        return not(self.phil[(i+1)%len(self.phil)]) and not(self.phil[(i-1)%(len(self.phil))])
        
    def wants_eat(self, i):
        self.mutex.acquire()
        self.freefork.wait_for(self.vecinos_libres)
        #print(self.actual,i)
        self.phil[i]=True
        self.eating.value +=1
        self.mutex.release()
        
    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.eating.value -=1
        self.freefork.notify()
        self.mutex.release()
        
        
        
class CheatMonitor():
    
    def __init__(self):
        self.eating = Value('i',0)
        self.mutex = Lock()
        self.checkingFriend = Condition(self.mutex)
        
    def is_eating(self,n):
        self.mutex.acquire()
        self.eating.value += 1
        self.checkingFriend.notify()
        self.mutex.release()
        
    def readyToThink(self):
        return self.eating.value == 2
    
    def wants_think(self,n):
        self.mutex.acquire()
        self.checkingFriend.wait_for(self.readyToThink)
        self.eating.value -= 1
        self.mutex.release()