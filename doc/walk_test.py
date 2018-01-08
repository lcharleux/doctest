import os
from string import Template
# SETUP
nbdir = "./notebooks/"
rstdir = "./notebooks_rst/"
template = Template(open("notebooks_index.template").read())
exclude_prefixes = ('__', '.')  # exclusion prefixes
file_suffixes = (".ipynb",)
title_levels = "+=~-_"

# DATA PROCESSING (whole section needs serious cleaning)
for dirpath, dirnames, filenames in os.walk(nbdir):
  dirnames[:] = [dirname
                 for dirname in dirnames
                 if not dirname.startswith(exclude_prefixes)]
  filenames = [f for f in filenames if f.endswith(file_suffixes)]
  print("#OPERATING ON: ",dirpath, dirnames, filenames)
  """
  if len(dirnames) + len(filenames)==0:
    print("=> No files to proceed, skipping")
  else:  
  """
  if True:
    path_depth = len(dirpath.strip("./").strip("/").split("/")) # Depth of the subdir
    rst_path = dirpath.replace(nbdir, rstdir) # Output rst path
    if rst_path.endswith("/") == False: rst_path += "/"
    if os.path.isdir(rst_path) == False: os.mkdir(rst_path)
    print("rst_path={0}  (path_depth = {1})".format(rst_path, path_depth))
    node = dirpath.strip("/").split("/")[-1]
    node_index = template.substitute(title = node, 
                                     underline = 80*title_levels[path_depth])
    for d in dirnames:
      node_index += "   " + d + "/" + d + "\n"
    for f in filenames:
      nb = f[:-6]
      rst_back_path = "/".join([".."]*len(dirpath.strip(
                      "./").strip("/").split("/"))) + "/"
      nb_rst_path = ( rst_path.strip("/").strip("./")) +"/"+ nb +".rst"
      node_index += "   " + nb + "\n"
      os.system("jupyter-nbconvert {0}/{1}.ipynb --to rst --output {2}".format(
            dirpath, nb, rst_back_path+nb_rst_path))
      rst = ""
      rst += ".. Note::\n\n  This notebook can be downloaded here: "
      rst += ":download:`{2}.ipynb <{0}{1}/{2}.ipynb>` \n\n".format(
               rst_back_path, dirpath.strip("./"), nb)
      rst += ".. contents::\n   :depth: 2\n"
      rst += open(nb_rst_path).read()
      open(nb_rst_path, "w").write(rst)
    print("####", node)    
    open(rst_path + node + ".rst", "w").write(node_index)              
                       
