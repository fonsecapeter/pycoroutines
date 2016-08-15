import os

import codecorator
coroutine = codecorator.coroutine
from copiping import source, sink, broadcast, even_filter, multiply_by_three, convert_to_string, os_call_sink


#                       even_filter -- convert_to_string -- sink
#                    /
# nums | source -- broadcast -- even_filter -- multiply_by_three -- sink
#                    \
#                      multiply_by_three -- convert_to_string -- sink

# top-branch: all evens in the nums
# milddle-branch: all evens, each multiply by three
# bottom-branch: all numbers multiplied by three

# prints:
# bottom: 3
# top: 2
# middle: 6
# bottom: 6
# bottom: 9
# top: 4
# middle: 12
# bottom: 12
# bottom: 15
# top: 6
# middle: 18
# bottom: 18
# bottom: 21
# top: 8
# middle: 24
# bottom: 24
# bottom: 27
# top: 10
# middle: 30
# bottom: 30

def main():
  os.system("echo 'IO bound call' >> /dev/null; sleep .01")
  source(
    range(10),
    broadcast([
      even_filter(
        convert_to_string(
          sink(), 'top'
        )
      ),
      even_filter(
        multiply_by_three(
          convert_to_string(
            sink(), 'middle'
          )
        )
      ),
      multiply_by_three(
        convert_to_string(
          sink(), 'bottom'
        )
      )
    ])
  )

def for_timing():
  os.system("echo 'IO bound call' >> /dev/null; sleep .01")
  source(
    range(10),
    broadcast([
      even_filter(
        convert_to_string(
          os_call_sink(), 'top'
        )
      ),
      even_filter(
        multiply_by_three(
          convert_to_string(
            os_call_sink(), 'middle'
          )
        )
      ),
      multiply_by_three(
        convert_to_string(
          os_call_sink(), 'bottom'
        )
      )
    ])
  )

if __name__ == '__main__':
  main()
