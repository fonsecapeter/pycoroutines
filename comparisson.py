import timeit

import numpy
from tabulate import tabulate

import serial
import threaded

def main():
  ser = serial.for_timing
  thr = threaded.for_timing

  ser_times =  timeit.repeat(ser, number=10)
  thr_times =  timeit.repeat(thr, number=10)

  ser_row = [ "serial",
             numpy.mean(ser_times),
             numpy.max(ser_times),
             numpy.min(ser_times)]

  thr_row = [ "threaded",
             numpy.mean(thr_times),
             numpy.max(thr_times),
             numpy.min(thr_times)]

  print tabulate([ser_row, thr_row], headers=['', 'avg', 'max', 'min'])

if __name__ == '__main__':
  main()
