from RebelStartup import *
class RebelInteractive:
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

@RebelStartup.interactivefunction
def clear():
   from os import system
   system('clear')

@RebelStartup.interactivefunction
def quit():
   """
   Shortcut for quit()
   """
   import sys
   sys.exit()
 
q = quit

@RebelStartup.interactivefunction
def reload(package):
   """
   Reload a module to get newest updates
   """
   from importlib import reload as rl
   try:
      rl(package)
   except Exception as e:
      print(e)

@RebelStartup.interactivefunction
def ls(path = None):
   """
   Linux ls command
   """
   import os
   if path:
      os.system(f'ls {path}')
   else:
      os.system('ls')

@RebelStartup.interactivefunction
def lsl(path = None):
   """
   Linux ls -l command
   """
   import os
   if path:
      os.system(f'ls -l {path}')
   else:
      os.system('ls -l')

@RebelStartup.interactivefunction
def cp(source, dest = '.'):
   """
   Linux cp command
   """
   import os
   os.system(f'cp {source} {dest}')

@RebelStartup.interactivefunction
def cpr(source, dest = '.'):
   """
   Linux cp -r command
   """
   import os
   os.system(f'cp {source} {dest}')

@RebelStartup.interactivefunction
def rm(path):
   """
   Linux rm command
   """
   import os
   os.system(f'rm {path}')

@RebelStartup.interactivefunction
def rmr(path):
   """
   Linux rm -r command
   """
   import os
   os.system(f'rm -r {path}')

@RebelStartup.interactivefunction
def mv(source, dest = '.'):
   """
   Linux mv command
   """
   import os
   os.system(f'mv {source} {dest}')

@RebelStartup.interactivefunction
def cat(path):
   """
   Linux cat command
   """
   import os
   os.system(f'cat {path}')

@RebelStartup.interactivefunction
def hist(search = None):
   """
   Display history with optional filter pattern
   """
   return RebelInteractive.hist(search = search, show = True)

@RebelStartup.interactivefunction
def mc(path = None):
   """
   Invoke interactive mc file manager
   """
   import os
   os.system(f'mc {path}')

@RebelStartup.interactivefunction
def code(file = None, search = None):
   """
   Edit a file with VS-Code
   code --> edit hist.py
   code filename --> edit filename
   code hist --> edit hist.py
   code hist pattern --> edit hist.py that meets pattern
   """
   from os import system
   def hist_code(search = None):
      lines = RebelInteractive.hist(search, False)
      with open('hist.py', 'w') as f:
         f.writelines(map(lambda x: x + '\n', lines))
         system('code hist.py')

   if file:
      if file.lower() == 'hist':
         hist_code(search)
      else:
         system(f'code {file}')
   else:
      hist_code()


print('Loaded Startup module')
