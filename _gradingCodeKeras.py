#This hasn't been seriously tested yet

import os
import pandas as pd
import subprocess
import hashlib
import time

files=[]

#removes pycache files and this file and nonpython files that may have snuck in
for f in os.listdir():
	if f[0] != '_' and f.endswith('.py'):
		files.append(f)

problemOne=pd.DataFrame(columns=['UID','accuracy','time'])
problemTwo=pd.DataFrame(columns=['UID','accuracy','time'])
problemThree=pd.DataFrame(columns=['UID','accuracy','time'])

dataFileNames=['breast-cancer-wisconsin.data','bezdekIris.data','test_images_mnist.csv', 'test_labels_mnist.csv']

#makes sure someone hasn't figured out how to edit the source files
def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

hashes=[]
for i in range(4):
	hashes[i]=sha256_checksum(dataFileNames[i])

def changedFiles():
	newHashes=[]
	for i in range(4):
		newHashes[i]=sha256_checksum(dataFileNames[i])
	for i in range(4):
		if newHashes[i]!=hashes[i]:
			return True
	return False
start=0
end=0

#things to add:
#bash calls need to be cleaned up much more and need to handle python errors
#cutoff after certain runtime

for i, file in enumerate(files):
	if file[-5]!='_':
		print(file+' has an irregular naming scheme based on missing underscore')
	elif len(file)>14:
		print(file+' has a file name longer than it should be')
	elif len(file)<14:
		print(file+ 'has a file name shorter than it should be')
	elif not file[0,8].isdigit():
		print(file+ ' has a UID comprised of values other than numbers')
	elif file.endswith('1.py'):
		start=time.time()
		output=subprocess.run(['python3',file,dataFileNames[0]], stdout=subprocess.PIPE)
		end=time.time()
		problemOne.loc[i]=[file[0:-6],output.stdout.decode('utf-8')[0:-2],str(end-start)] #-2 to remove \n, -6 to remove _n.py
		problemOne.to_csv('problemOne.csv', encoding='utf-8')		
	elif file.endswith('2.py'):
		start=time.time()
		output=subprocess.run(['python3',file,dataFileNames[1]], stdout=subprocess.PIPE)
		end=time.time()
		problemTwo.loc[i]=[file[0:-6],output.stdout.decode('utf-8')[0:-2],str(end-start)]
		problemTwo.to_csv('problemTwo.csv', encoding='utf-8')
	elif file.endswith('3.py'):
		start=time.time()
		output=subprocess.run(['python3',file,dataFileNames[2],dataFileNames[3]], stdout=subprocess.PIPE)
		end=time.time()
		problemThree.loc[i]=[file[0:-6],output.stdout.decode('utf-8')[0:-2],str(end-start)]
		problemThree.to_csv('problemThree.csv', encoding='utf-8')
	else:
		print(file+' has an irregular naming scheme based on last digit')

	if not changedFiles():
		print(file+' edited a local file')
		break
	else:
		print('ran '+file+'. '+str(100*i/len(files))+'% complete')
