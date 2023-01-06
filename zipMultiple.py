import sys
import os
import stat
import shutil

###
# wanted: the zip file to be created
# have  : The directory to be zipped
###
def zipped(wanted, have):
  # Zip the given directory
  shutil.make_archive(wanted, 'zip', have)
  # Needs to change permissions
  os.chmod(wanted + '.zip', stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

###
# Create a new absolute path. Give everyone access to the directory.
# Move the zip file into the new absolute path.
# target: directory to be moved to
# bullet: file to be moved into new directory
def make_dir_move(target, bullet):
  os.mkdir(target)
  os.chmod(target, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
  shutil.move(bullet, target)
###
# Tests if the OS is Windows or not.
# 'nt' = Windows. 'posix' = Unix/Linux
def test_os():
  clean = '/'
  if os.name == 'nt':
    clean = '\\'
  return clean

# python3 zpiMultiple.py complete_dir_to_be_zipped [-z | -u]
n = len(sys.argv)
if n < 2 or n > 3:
  sys.exit("\nError: Need complete path of directory to be zipped\n")
# Get the directory to be zipped
dir_name = sys.argv[1]
dirSymble = test_os()
# Get the original directory's name
org_name = dir_name.split(dirSymble)[-1]
# Make sure the directory actually exists
if os.path.exists(dir_name) == False:
  sys.exit("\nError: Given directory/file needs to exist\n")
# Get the current working directory of the CMD line
cwd = os.getcwd()
# this is the name of the new directory to be used
new_dir = 'no_name'
# Zip the original directory & change permissions for everyone
zipped(cwd + dirSymble + org_name, dir_name)
# Create FLAG directory that will be used to stop the unzipping process
# Give everyone access to the directory
# Move the original zip file into the new 'stop' directory
make_dir_move(cwd + dirSymble + 'stop', cwd + dirSymble + org_name + '.zip') 
# zip the FLAG directory & change permissions for everyone
zipped(cwd + dirSymble + 'stop', cwd + dirSymble + 'stop')
# Need to delete the 'stop' directory
shutil.rmtree(cwd + dirSymble + 'stop')
# New absolute path
path = os.path.join(cwd, new_dir)
make_dir_move(path, cwd + dirSymble + 'stop.zip')
# zip a LOT more times
for i in range(29):
  zipped(cwd + '/' + new_dir, path)
  shutil.rmtree(path)
  make_dir_move(path, cwd + dirSymble + 'no_name.zip')
# zip one more time and delete the last directory
zipped(cwd + dirSymble + 'no_name', path)
shutil.rmtree(path)

exit(0)