#fileName:const.py

class _const:
  class ConstError(TypeError):pass
  def __setattr__(self,name,value):
    #if self.__dict__.has_key(name): 3.x之后has_key被废弃
    if name in self.__dict__:
      raise self.ConstError("Can't rebind const(%s)"%name)
    self.__dict__[name] = value
import sys
sys.modules[__name__] = _const()