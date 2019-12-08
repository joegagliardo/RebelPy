import sys
class RebelStartup():
   """
   This class creates a decorator called @staticmethod that you can use to
   define a function that can be called like a statement without parentheses

   It replaces the sys.displayhook and sys.excepthook with custom functions
   """
   import os, readline, traceback, functools
   
   # Preserve original function pointers in case you want to reset them
   displayhook = sys.displayhook
   excepthook = sys.excepthook

   class interactivefunction(object):
      """
      Decorator to make a function callable in the interactive session by turning it into a class
      with a method called interactivefunction which will be called by the displayhook and excepthook functions
      """
      def __init__(self, f):
         self.f = f

      def __call__(self, *args, **kwargs):
         self.f(*args, **kwargs)

      interactivefunction = __call__

   @staticmethod
   def displayhook(whatever):
      if hasattr(whatever, 'interactivefunction'):
         return whatever.interactivefunction()
      elif whatever:
         print(whatever)

   @staticmethod
   def excepthook(exctype, value, tb):
      import sys, inspect
      if exctype is SyntaxError:
         index = readline.get_current_history_length()
         item = readline.get_history_item(index)
         command = item.split()
         app = sys.modules['__main__']
         if command[0] == '!': ## run an OS command
            import os
            cmd = ' '.join(command[1:])
            os.system(cmd)
         elif command[0] in map(lambda x:x[0], inspect.getmembers(app)) and hasattr(eval(command[0]),'interactivefunction'):
            try:
               eval(command[0]).interactivefunction(*command[1:])
            except:
                  traceback.print_exception(exctype, value, tb)
         else:
              traceback.print_exception(exctype, value, tb)
      else:
         traceback.print_exception(exctype, value, tb)


   @staticmethod
   def hist(search = None, show = True):
      import readline
      ret = []
      for i in range(readline.get_current_history_length()):
         line = readline.get_history_item(i + 1)
         if line.lower() in ['quit()', 'hist()', 'code()', 'dir()', 'clear()', 'quit', 'hist', 'code', 'dir', 'clear', 'ls', 'lsl', 'cat', 'rm', 'rmr', 'cp', 'cpr', 'mv']:
            continue

         if search:
            if search in line:
               ret.append(line)
         else:
            ret.append(line)

      import itertools
      ret = next(zip(*itertools.groupby(ret))) # remove duplicate if is the same as previous command
      if show:
         for l in ret:
            print(l)
      else:
         return ret

sys.displayhook = RebelStartup.displayhook
sys.excepthook = RebelStartup.excepthook
