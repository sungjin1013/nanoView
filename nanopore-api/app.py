from flask import Flask, render_template, request
from FAST5_api import Fast5Event
from flask_cors import CORS, cross_origin
import os, errno, sys, h5py, pickle, simplejson, json, jsonify
from os import listdir
from os.path import isfile, join
import pandas as pd
from operator import itemgetter
from SAMParse import *
from extract_tombo import Fast5Events
import numpy as np

app = Flask(__name__)
cors = CORS(app)


@app.route('/test/<path:sam>', methods = ['GET'])
def test(sam):

	return str(len(cigar)), 201


@app.route('/generatejson/<string:name>&<path:directory>&<path:ref>&<path:sam>', methods = ['GET'])
def generatejson(name, directory, ref, sam):
	name = name[5:]
	directory = directory[10:]
	ref = ref[4:]
	sam = sam[4:]
	dir_path = "./data/"+name
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	else:
		return 'Project Already Exists', 406
	for i in listdir(directory):
		if isfile(join(directory, i)):
			base = i.split('.fast')[0]
			path = "./data/"+name+"/"+base+".record"
			f = Fast5Event(directory+"/"+i)
			record, max_min,a, pos = f.get_list_event_data(file_path=sam)
			for i in range(len(record)):
				if i % 2 == 1 or i == 0:
					continue
				else:
					leng = len(record[i])
					diff = 1.0/float(leng)
					for id in range(leng):
						record[i][id][0] = float(record[i-1]) + float(diff)*float(id)
			record.append(max_min)
			with open(path, 'wb') as outfile:
				pickle.dump(record, outfile)
				pickle.dump(max_min, outfile)
	return json.dumps(record), 201


@app.route('/removeproject/<string:existing>', methods = ['POST'])
def removeproject(existing):
	name = existing[9:]
	try:
		os.system('rm -rf data/'+name)
		return 'Project Successfully Removed', 201
	except ValueError:
		return 'Error Removing Project:' + name, 406


@app.route('/getrange/<string:start>&<string:end>&<string:name>', methods = ['GET'])
def getrange(start, end, name):
	mami = []
	start = start[6:]
	end = end[4:]
	start_i = int(start)
	end_i = int(end)
	name = name[5:]
	started = 0
	directory = "./data/"+name
	final_record = "["
	first = 0
	for i in listdir(directory):
		if isfile(join(directory, i)):
			with open(directory+"/"+i, 'rb') as infile:
				record = pickle.load(infile)
	# 		mami.append(record[-1])
			final_record +=   json.dumps(record[0]) + ","
			final_record += json.dumps(record[(start_i*2)+1:(end_i*2)+1]) + ","
	# max_mami = max(mami,key=itemgetter(1))[0]
	# min_mami = min(mami,key=itemgetter(1))[1]
	# final_record += "["+max_mami+", "+min_mami+"]]"
	final_record += "]"
	return final_record, 201


@app.route('/getprojects/', methods = ['GET'])
def dataselect():
	sub = os.listdir('./data')
	projects = {}
	for i in range(len(sub)):
		projects[i] = sub[i]
	return json.dumps(projects), 200


@app.route('/tombo/<string:name>&<path:directory>&<path:sam>', methods = ['GET'])
def tombo(name, directory, sam):
	name = name[5:]
	directory = directory[10:]
	sam = sam[4:]
	dir_path = "./data/"+name
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	for i in listdir(directory):
		if isfile(join(directory, i)):
			base = i.split('.fast')[0]
			path = "./data/"+name+"/"+base+".tombo.record"
			f = Fast5Events(directory+"/"+i)
			record, max_min,a, pos = f.get_list_event_data(file_path=sam)
			d_counter = 0
			for i in range(len(a)):
				if a[i][1] == 'i':
					record[1][((a[i][0]-(d_counter+1)) * 2) - 1][0][-1] = 'i'
				elif a[i][1] == 'd':
					d_counter += 1
					record[1][((a[i][0]-(d_counter+1)) * 2) - 1][0][-1] = 'd'
			record.append(max_min)
			with open(path, 'wb') as outfile:
				pickle.dump(record, outfile)
				pickle.dump(max_min, outfile)
	return json.dumps(record), 201


@app.route('/getall/<string:name>&<string:data>', methods = ['GET'])
def getall(name, data):
	mami = []
	data = data[-1]
	name = name[5:]
	started = 0
	directory = "./data/"+name
	final_record = "["
	first = 0
	if data == '1':
		for i in listdir(directory):
			if isfile(join(directory, i)):
				if i.endswith(".tombo.record"):
					with open(directory+"/"+i, 'rb') as infile:
						record = pickle.load(infile)
					mami.append(record[-1])
					final_record +=   json.dumps(record[0]) + ","
					final_record += json.dumps(record[1:-1]) + ","
	elif data == '2':
		for i in listdir(directory):
			if isfile(join(directory, i)):
				if i.endswith(".normed.record"):
					with open(directory+"/"+i, 'rb') as infile:
						record = pickle.load(infile)
					final_record += json.dumps(record[0]) + ","
					final_record += json.dumps(record[1:]) + ","
	else:
		for i in listdir(directory):
			if isfile(join(directory, i)):
				if not i.endswith(".tombo.record") and not i.endswith(".normed.record"):
					with open(directory+"/"+i, 'rb') as infile:
						record = pickle.load(infile)
					mami.append(record[-1])
					final_record +=   json.dumps(record[0]) + ","
					final_record += json.dumps(record[1:-1]) + ","
	try:
		max_mami = max(mami,key=itemgetter(1))[0]
		min_mami = min(mami,key=itemgetter(1))[1]
		final_record += "["+max_mami+", "+min_mami+"]]"
	except :
		pass
	finally:
		final_record = final_record[:-1]
		final_record += "]"
	return final_record, 201


@app.route('/normed/<string:name>&<path:directory>&<path:sam>', methods = ['GET'])
def normed(name, directory, sam):
	name = name[5:]
	directory = directory[10:]
	sam = sam[4:]
	dir_path = "./data/"+name
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	for i in listdir(directory):
		if isfile(join(directory, i)):
			base = i.split('.fast')[0]
			path = "./data/"+name+"/"+base+".normed.record"
			f = Fast5Events(directory+"/"+i)
			shift0, scale0, bprime0, b_a0, record, mapped_start, bases = get_data(directory+'/'+i)
			final_r0 = index_record(record, mapped_start)
			final_r = base_record(final_r0, bases)
			with open(path, 'wb') as outfile:
				pickle.dump(record, outfile)
	return json.dumps(final_r), 201

def get_data(file):
    f = h5py.File(file, 'r')
    read = file.split('_read')[1]
    read = read.split('_')[0]
    a = f['Raw/Reads/Read_'+read+'/Signal']
    b = []
    for item in a:
        b.append(item)
    digi = f['UniqueGlobalKey/channel_id'].attrs['digitisation']
    parange = f['UniqueGlobalKey/channel_id'].attrs['range']
    offset = f['UniqueGlobalKey/channel_id'].attrs['offset']
    events = f['/Analyses/RawGenomeCorrected_000/BaseCalled_template/Events']
    start = []
    for item in events:
        start.append((item['start'], item['length']))
    shift = np.median(b)
    scale = np.median(np.abs(b - shift))
    bprime = (b - shift)
    b_a = (b - shift) / scale
    record, mapped_start, bases = get_list_values(start, b_a, file)
    return shift, scale, bprime, b_a, record, mapped_start, bases


def get_list_values(start, b_a, file):
    record = []
    f = Fast5Events(file)
    qname = f.get_qname()
    offset = f.get_offset()
    mapped_start = f.get_mapped_start()
    bases = f.get_base()
    record.append(qname)
    counter = 0
    len_counter = 0
    sub0 = []
    for i in range(0, len(start)):
        length = start[i][1]
        sub0.append(i+int(offset)+int(mapped_start))
        sub1 = []
        for a in range(length):
            sub1.append([b_a[a + start[i][0]+offset]])
        sub0.append(sub1)
    record.append(sub0)
    return record, mapped_start, bases


def index_record(record, mapped_start):
	c = 0
	for item in record[1][1::2]:
		length = len(item)
		counter = 0
		for i in item:
			i.append(c + (float(counter)/float(length))+int(mapped_start))
			counter += 1
		c += 1
	return record


def base_record(record, bases):
	counter = 0
	for item in record[1][1::2]:
		base = bases[counter]
		for i in item:
			i.append(base.decode('utf-8'))
		counter += 1
	return record


@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
