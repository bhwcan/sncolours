class ColourCombinations:
  def __init__(self):

    self.combinations = [ 
      [1, 1, 1], 
      [1, 1, 2], 
      [1, 1, 3],
      [1, 2, 1],
      [1, 2, 2],
      [1, 2, 3],
      [1, 3, 1],
      [1, 3, 2],
      [1, 3, 3],
      [2, 1, 1],
      [2, 1, 2],
      [2, 1, 3],
      [2, 2, 1],
      [2, 2, 2],
      [2, 2, 3],
      [2, 3, 1],
      [2, 3, 2],
      [2, 3, 3],
      [3, 1, 1],
      [3, 1, 2],
      [3, 1, 3],
      [3, 2, 1],
      [3, 2, 2],
      [3, 2, 3],
      [3, 3, 1],
      [3, 3, 2],
      [3, 3, 3]
      ]

    self.resuts = []

  def set(self, startid, tints):

    self.results = []
    id = startid
    ic = 0
    for c in self.combinations:
      colour = {}
      colour['id'] = id
      colour['name'] = "color"+str(id)
      t = []
      t.append(tints[c[0]-1])
      t.append(tints[c[1]-1])
      t.append(tints[c[2]-1])
      colour['tints'] = t
      self.results.append(colour)
      ic += 1
      id += 1


#main
# tints = [ "red  ", "green", "blue "]

# cc = ColourCombinations()
# cc.set(100, tints)

# for r in cc.results:
#   print(r)


