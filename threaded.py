import Queue
import threading

import codecorator
coroutine = codecorator.coroutine
from copiping import source, sink, broadcast, even_filter, multiply_by_three, convert_to_string, os_call_sink

@coroutine
def threaded(target):
  messages = Queue.Queue()
  def run_target():
    while True:
      item = messages.get()
      if item is GeneratorExit:
        target.close()
        return
      else:
        target.send(item)
  threading.Thread(target=run_target).start()
  try:
    while True:
      item = (yield)
      messages.put(item)
  except GeneratorExit:
    messages.put(GeneratorExit)

def main():
  source(
    range(10),
    broadcast([
      threaded(
        even_filter(
          convert_to_string(
            sink(), 'top'
          )
        ),
      ),
      threaded(
        even_filter(
          multiply_by_three(
            convert_to_string(
              sink(), 'middle'
            )
          )
        ),
      ),
      threaded(
        multiply_by_three(
          convert_to_string(
            sink(), 'bottom'
          )
        )
        )
    ])
  )

def for_timing():
  source(
    range(10),
    broadcast([
      threaded(
        even_filter(
          convert_to_string(
            os_call_sink(), 'top'
          )
        ),
      ),
      threaded(
        even_filter(
          multiply_by_three(
            convert_to_string(
              os_call_sink(), 'middle'
            )
          )
        ),
      ),
      threaded(
        multiply_by_three(
          convert_to_string(
            os_call_sink(), 'bottom'
          )
        )
        )
    ])
  )

if __name__ == '__main__':
  main()
