import os

import codecorator
coroutine = codecorator.coroutine

# |--->
# entry point of the pipeline
def source(nums, target):
  for num in nums:
    target.send(num)

#     /--->
# >------->
#     \--->
# takes a sequence of coroutines and passes received items to all
@coroutine
def broadcast(targets):
  while True:
    item = (yield)
    for target in targets:
      target.send(item)

# >----|
# end point of the pipeline - just prints each value
@coroutine
def sink():
  while True:
    num = (yield)
    print num
    
@coroutine
def os_call_sink():
  while True:
    num = (yield)
    os.system("echo 'IO bound call' >> /dev/null; sleep .01")


# ------------------------------------------------------------------------------
# >----->
# sample intermediary pipes
@coroutine
def even_filter(target):
  while True:
    num = (yield)
    if num % 2 == 0:
      target.send(num)

@coroutine
def multiply_by_three(target):
  while True:
    num = (yield)
    target.send(num * 3)

@coroutine
def convert_to_string(target, branch):
  while True:
    num = (yield)
    target.send('{b}: {n}'.format(b=branch, n=num))
