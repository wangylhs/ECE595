#path_test_Ver2.py path_test_Ver2
#Guanshi He (he95)
#Output the paths to specific websites

import random
import matplotlib.pyplot as plt
import sys

websites = []
pathnum = []

#read all the websites data
with open('traceable_us.txt') as websitefile:
	counter = 0
	readbox = websitefile.readline()
	while readbox:
		websites.append(readbox.split()[0])
		#print 'websites[',counter,'] =====',websites[counter]
		readbox =websitefile.readline()
		counter = counter  + 1

timecount = dict()
avgdelay = dict()
avgdelay1 = dict()
avgdelay2 = dict()
databox = []


countercopy = counter
counter = 0
while counter < countercopy:
	targetwebsite = websites[counter].rstrip()
	print 'targetwebsite = ',targetwebsite
	path = []
	path_len = []
	
	node_count = 0
	path_count = 0
	i = 1
	firsttimeflag = 0
	with open('final_ecn_data_us') as f:
		#print 'starting analyzing...'
		f.seek(0,0)
		databox = []
		databoxline1 = f.readline()
		#print databoxline1
		databoxline2 = f.readline()
		#print databoxline2
		databox.append(databoxline1)
		databox.append(databoxline2)
		while databoxline2:

			while(len(databoxline2.split())!=6):
				i = i + 1
				databoxline2 = f.readline()
				databox.append(databoxline2)
				if(databoxline2 == ''):
					break
			#get one chunk of traceroute info
			#for j in range (0,i):
				#print j
				#print j,databox[j]

			if databox[1].split()[0] == targetwebsite:
				print i
				time = databox[0].split()[3]
				webip = databox[1].split()[1]
				webip = webip[0:len(webip)-1]
				k = 2  #index for checking three components
				hour = int(time.split(':')[0])
				if firsttimeflag == 0:
					print '======firsttime======'
					while len(databox[k].split()) == 3:
						iplen = len(databox[k].split()[1])
						path.append(databox[k].split()[1][1:iplen-1])
						node_count = node_count + 1
						k = k + 1
					path_len.append(node_count)			
					path_count = path_count + 1
					firsttimeflag = 1
					print 'nodecount',node_count
					
				else:

					print '======NOTfirsttime======'
					checkpath_index = 0
					checknode_index = 0
					diffflag = 0
					tempk = k
					sameflag = 0
					for index in range(0,path_count):
						#check every set of path
						print 'Checking route #',index,'......' 

						if index == 0:
							nodesnum = path_len[index]
						else:
							nodesnum = path_len[index] - path_len[index - 1]
						sameflagcheck = 0
						print 'This route has',nodesnum,'nodes'
						# if i > node_count:
						# 	diffflag = 1
						if diffflag != 1:	
							while len(databox[k].split()) == 3:
								iplen = len(databox[k].split()[1])
								ip = databox[k].split()[1][1:iplen-1]
								if ip != path[checknode_index]:
									#print 'different path'
									diffflag = 1
									checknode_index = checknode_index + 1
									break
								else:
									#print 'same'
									k = k + 1
									sameflagcheck = sameflagcheck + 1
									checknode_index = checknode_index + 1

						if (diffflag == 1) & (index == path_count):
							break
						#print 'sameflagcheck = ',sameflagcheck

						if sameflagcheck == nodesnum:
							sameflag = 1
							#print 'Same route FOUND!!!!!!'

						k = tempk
					if (diffflag == 1) & (sameflag == 0):
						#print 'Different route FOUND, STORING.......'
						k = tempk
						#node_count = 0
						while len(databox[k].split()) == 3:
							iplen = len(databox[k].split()[1])
							ip = databox[k].split()[1][1:iplen-1]
							#print ip
							path.append(databox[k].split()[1][1:iplen-1])
							node_count = node_count + 1
							k = k + 1
						path_len.append(node_count)
						path_count = path_count + 1

			#process the next chunk of info
			databoxline1 = databoxline2
			databoxline2 = f.readline()
			
			i = 1
			databox = []
			databox.append(databoxline1)
			databox.append(databoxline2)

		#print out the paths
		index2 = 0
		tempindex2 = 0

		for index1 in range(0,path_count):
			#print 'path ',index1
			pathsentence = ''
			for index2 in range(index2,path_len[index1]):
				#print 'index2 = ',index2
				#print tempindex2+path_len[index1]-1
				if index2 == path_len[index1]-1:
					print path[index2].rstrip(),
					#pathsentence = pathsentence + path[index2]
				else:
					print path[index2],'=>',
					#pathsentence = pathsentence + '==>'
			print
			#pathfile = open('pathfile.txt','w')
			#pathfile.write('\n')
			#pathfile.write(pathsentence)
			index2 = index2 + 1
			tempindex2 = index2




		pathnum.append(path_count)
		path_count = 0

	counter = counter + 1


counter = 0

while counter < countercopy:
	print websites[counter].rstrip(),'has',pathnum[counter],'path(s)'
	counter = counter + 1

counter = 0
target = open('output2.txt', 'w')
while counter < countercopy:
	sentence = str(websites[counter].rstrip())+' '+str(pathnum[counter])
	target.write(sentence)
	target.write('\n')
	counter = counter + 1



xaxis = []
for y in range(0,counter):
	xaxis.append(y)

plt.plot(xaxis,pathnum,'r')
plt.xticks(rotation = 90)
plt.xticks(xaxis,websites)
plt.ylabel('# of paths')
plt.title('Website vs. # of paths')
plt.show()








