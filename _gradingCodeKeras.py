#This hasn't been seriously tested yet

import os
import pandas as pd
import subprocess
import hashlib
import time

tempFiles=os.listdir()
files=[]

#removes pycache files and this file and nonpython files that may have snuck in
for i in range(len(tempFiles)):
	if tempFiles[i][0] != '_' and tempFiles[i][-3:-1]=='.py':
		files.append(tempFiles[i])

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
for i in [0,1,2,3]:
	hashes[i]=sha256_checksum(dataFileNames[i])

def changedFiles():
	newHashes=[]
	for i in [0,1,2,3]:
		newHashes[i]=sha256_checksum(dataFileNames[i])
	for i in [0,1,2,3]:
		if newHashes[i]!=hashes[i]:
			return True
	return False
start=0
end=0
for i in range(len(files)):
	if files[i][-5]!='_':
		print(file+' has an irregular naming scheme based on missing underscore')
	elif files[i][-4]!='1' and files[i][-3]!='2' and files[i][-3]!='3':
		print(file+' has an irregular naming scheme based on last digit')
	elif files[i][-4]=='1':
		start=time.time()
		output=subprocess.run(['python3',files[i],dataFileNames[0]], stdout=subprocess.PIPE)
		end=time.time()
		problemOne.loc[i]=[files[i][0:-6],output.stdout.decode('utf-8')[0:-2],str(end-start)] #-2 to remove \n, -6 to remove _n.py
		problemOne.to_csv('problemOne.csv', encoding='utf-8')		
	elif files[i][-4]=='2':
		start=time.time()
		output=subprocess.run(['python3',files[i],dataFileNames[1]], stdout=subprocess.PIPE)
		end=time.time()
		problemTwo.loc[i]=[files[i][0:-6],output.stdout.decode('utf-8')[0:-2],str(end-start)]
		problemTwo.to_csv('problemTwo.csv', encoding='utf-8')
	elif files[i][-4]=='3':
		start=time.time()
		output=subprocess.run(['python3',files[i],dataFileNames[2],dataFileNames[3]], stdout=subprocess.PIPE)
		end=time.time()
		problemThree.loc[i]=[files[i][0:-6],output.stdout.decode('utf-8')[0:-2],str(end-start)]
		problemThree.to_csv('problemThree.csv', encoding='utf-8')
	if not changedFiles():
		print(file+' edited a local file')
		break
	else:
		print('ran '+file+'. '+str(100*i/len(files))+'$ complete')

#timing execution 