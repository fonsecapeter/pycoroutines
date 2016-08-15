def grep(pattern):
  print "Looking for %s" % pattern
  while True:
    line = (yield)  # yield as expression
    if pattern in line:
      print line

g = grep("python") # no output was produced
g.next() # prime it, on first operation, coroutine starts running, alternatively call send(None)
g.send("Yeah, but no, but yea, but no")
g.send("A series of tubes")
g.send("python generators rock!")
