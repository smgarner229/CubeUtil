import sys
import numpy as np

class Atom:
  def __init__(self,sym_,x_,y_,z_,quantum_=False):
    sym_=str(sym_)
    if "GH" in sym_:
      sym_=sym_.replace("GH","X")
    self.__sym=sym_
    self.__x=float(x_)
    self.__y=float(y_)
    self.__z=float(z_)
    self.__quantum=quantum_

  def __str__(self):
    return "{0} {1:8f} {2:8f} {3:8f}\n".format(self.__sym,self.__x,self.__y,self.__z)

  @property
  def symbol(self):
    return self.__sym

  def set_symbol(self,symbol):
    self.__sym = symbol

  def add_index(self,num):
    self.__sym+=str(num)

  @property
  def is_quantum(self):
    return self.__quantum

class Cube:
  def __init__(self):
    self.__natom = 0
    self.__origin = [None,None,None]
    self.__npts = [0,0,0]
    self.__axis_def = [[],[],[]]
    self.__geom = []
    self.__cube = []

    return

  def load_from_file(self,filename):
    zs = []
    cube = []
    with open(filename,'r') as f1:
      for line in f1:
        # Skip first two lines
        m = next(f1)
        m = next(f1)
        # Number of atoms and cube origin on line 3
        self.__natom = int(m.split()[0])
        self.__origin = [float(i) for i in m.split()[1:]]
        # Number of points and axis is following 3 lines
        for i in range(3):
          m = next(f1)
          self.__npts[i]     = int(m.split()[0])
          self.__axis_def[i] = [float(i) for i in m.split()[1:]]
        # Read the geometry
        for _ in range(self.__natom):
          m=next(f1)
          self.__geom.append(Atom(*[float(i) for i in m.split()[1:]]))
        break
    
      for line in f1:
        self.__cube+=[float(i) for i in line.split()]
    self.__cube = np.reshape(np.asarray(self.__cube),self.__npts)

  @property
  def data(self):
    return self.__cube

  @property
  def origin(self):
    return self.__origin

  @property
  def npts(self):
    return self.__npts

  @property
  def steps(self):
    return self.__axis_def

if __name__ == '__main__':
  my_cube = Cube()
  my_cube.load_from_file(sys.argv[1])
  print(my_cube.data[50,50,:])
