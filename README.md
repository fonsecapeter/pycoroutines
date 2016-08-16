# Practice creating pipelines with coroutines

* Create a coroutine decorator to avoid having to prime each generator:
```python
  # codecorator.py
  def coroutine(func):
    def start(*args, **kwargs):
      cr = func(*args, **kwargs)
      cr.next()
      return cr
    return start
```

* Create a few building blocks for a pipeline, including a  source, some intermediaries, and a sink. Branch out with a broadcaster:
```python
  # copiping.py

  # takes a sequence of coroutines and passes received items to all
  @coroutine
  def broadcast(targets):
    while True:
      item = (yield)
      for target in targets:
        target.send(item)
```

* Test out a pipeline
```python
  # serial.py

  #                       even_filter -- convert_to_string -- sink
  #                    /
  # nums | source -- broadcast -- even_filter -- multiply_by_three -- sink
  #                    \
  #                      multiply_by_three -- convert_to_string -- sink

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
```
```python
  # =>
    bottom: 3
    top: 2
    middle: 6
    bottom: 6
    bottom: 9
    top: 4
    middle: 12
    bottom: 12
    bottom: 15
    top: 6
    middle: 18
    bottom: 18
    bottom: 21
    top: 8
    middle: 24
    bottom: 24
    bottom: 27
    top: 10
    middle: 30
    bottom: 30
```

* Multi-thread the pipeline with a threaded coroutine pipeline member
```python
  # threaded.py
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

  # ...

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
```

* replace print statements with an arbitrary system call to `echo 'IO bound call' >> /dev/null; sleep .01` and run some time tests on my macbook:
```python
  # comparison.py
  ser_times =  timeit.repeat(ser, number=10)
  thr_times =  timeit.repeat(thr, number=10)
```
```python
#                avg        max        min
# --------  --------  ---------  ---------
  serial    4.12966   4.13732    4.12442
  threaded  0.013469  0.0157881  0.0120649
```

> written wile reading http://www.dabeaz.com/coroutines/Coroutines.pdf
