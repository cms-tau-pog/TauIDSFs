import os
from ROOT import TFile, TH1
modulepath = os.path.dirname(__file__)
#print modulepath

def ensureTFile(filename,option='READ'):
  """Open TFile, checking if the file in the given path exists."""
  if not os.path.isfile(filename):
    raise OSError('File in path "%s" does not exist!'%(filename))
    exit(1)
  file = TFile(filename,option)
  if not file or file.IsZombie():
    raise OSError('Could not open file by name "%s"'%(filename))
    exit(1)
  return file
  
def ensureFile(*paths,**kwargs):
  """Ensure file exists."""
  filepath = os.path.join(*paths)
  stop     = kwargs.get('stop',True)
  if '*' in filepath or '?' in filepath:
    exists = len(glob.glob(filepath))>0
  else:
    exists = os.path.isfile(filepath)
  if not exists and stop:
      raise OSError('File "%s" does not exist'%(filepath))
  return filepath
  
def extractTH1(file,histname,setdir=True):
  """Get histogram from a given file."""
  if not file or file.IsZombie():
    raise OSError('Could not open file!')
    exit(1)
  hist = file.Get(histname)
  if not hist:
    raise OSError('Did not find histogtam "%s" in file %s!'%(histname,file.GetName()))
    exit(1)
  if setdir and isinstance(hist,TH1):
    hist.SetDirectory(0)
  return hist

def ensureTFileAndTH1(filename,histname,verbose=True,setdir=True):
  """Open a TFile and get a histogram."""
  if verbose:
    print ">>>   %s"%(filename)
  file = ensureTFile(filename,'READ')
  hist = extractTH1(file,histname,setdir=setdir)
  return file, hist

def warning(string,**kwargs):
  """Print warning with color."""
  pre    = kwargs.get('pre',  "") + "\033[1m\033[93mWarning!\033[0m \033[93m"
  title  = kwargs.get('title',"")
  if title: pre = "%s%s: "%(pre,title)
  string = "%s%s\033[0m"%(pre,string)
  print string.replace('\n','\n'+' '*(len(pre)-18))
  
