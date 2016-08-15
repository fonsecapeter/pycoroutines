# decorator to avoid having to prime each coroutine
# => just @coroutine over each coroutine definition
def coroutine(func):
  def start(*args, **kwargs):
    cr = func(*args, **kwargs)
    cr.next()
    return cr
  return start
