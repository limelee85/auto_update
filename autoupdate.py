import os
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import datetime
import json
import re
import shutil
from config import CONFIG
import traceback
import json
import os

path_public = os.getenv('PATH_PUBLIC')
DEBUG = os.getenv("DEBUG", 'prod')
version_file = os.path.dirname(__file__)+'/data/versions.json'
prev_versions = {}
is_change = 0

def debug_print(*args, **kwargs):
	if DEBUG == 'dev':
		print("[DEBUG]", *args, **kwargs)

def check_str(string):
	check_str = ['-r ', '-rf ', '-f ', '..', '../', '\\.\\.', '\\..', '.\\.' , '*', '/bin', '/boot', '/dev', '/etc', '/home', '/root', '/usr', '/sys', '/var', '"', '\\', ';', '\n', '\x00']
	warn = [s for s in check_str if s in string]
	if (len(warn) > 0) :
		print('## Find Dangerous String [ {} ] : Skip Download/Remove File'.format(string))
		return False
	else :
		return True

def file_path_delete(prev_version,sub_path):

	if (check_str(prev_version)) :
		try :
			os.remove(path_public+sub_path+prev_version)
		except FileNotFoundError :
			print('## Not Fonud [ {} ] : Skip Remove File'.format(prev_version))
		except IsADirectoryError :
			print('## Not Found [ {} ] : Skip Remove File'.format(prev_version))

def load_versions():
	if not os.path.exists(version_file):
		return {}
	with open(version_file, "r", encoding="utf-8") as f:
		return json.load(f)

def save_versions():
	with open(version_file, "w", encoding="utf-8") as f:
		json.dump(prev_versions, f, indent=2, ensure_ascii=False)


def parser(cfg) :
	v = requests.get(cfg["url"] , allow_redirects=False)
	if (cfg["select"] != 'Location') :
		result = bs(v.text, 'html.parser')
		select_result = result.select(cfg["select"])[0]

		debug_print('select_result=', select_result)
		iter_path = cfg["iter_path"]
		if isinstance(iter_path, list):
			for key in iter_path:
				if isinstance(select_result, dict):
					select_result = select_result[key]
				else:
					select_result = select_result.get(key)
		elif isinstance(iter_path, str):
			if iter_path == "text":
				select_result = select_result.text 
			else :
				select_result = str(select_result)

		debug_print('select=', cfg["select"], 'result=', select_result)
	else:
		select_result = v.headers[cfg["select"]]

	download_select = re.compile(cfg["result"]["download_regex"], re.DOTALL).search(select_result).groupdict()
	filename_select = re.compile(cfg["result"]["filename_regex"], re.DOTALL).search(select_result).groupdict()

	debug_print(download_select, filename_select)
	download = cfg["result"]["download"].format(**download_select)
	filename = cfg["result"]["filename"].format(**filename_select)

	debug_print("[*] Parse Result : download url= ", download,", filename= ", filename)
	return [download,filename]

def json_parse(cfg):
	debug_print("=== JSON Load Start ===")
	v = requests.get(cfg["url"])
	data = json.loads(v.text)

	target = data
	for p in cfg["iter_path"]:
		target = target[p]

	debug_print("Find Lastest File Info", target)
	regex = re.compile(cfg["select"])
	for item in target:
		if re.match(regex, item[cfg["ckey"]]):
			values = {}
			for f in cfg["result"]["fields"]:
				if f == "VersionUnderscore":
					values[f] = "_".join(item["Version"].split("."))
				else:
					values[f] = item.get(f, "")

			download = cfg["result"]["download"].format(**values)
			filename = cfg["result"]["filename"].format(**values)

			debug_print("[*] JSON Parse Result : download url= ", download,", filename= ", filename)
			return [download,filename]

def update(name) :

	try: 
		cfg = CONFIG[name]
		debug_print("[*] Config Load :", cfg)

		if (cfg and cfg['type'] == "json"):
			parse, version = json_parse(cfg)
		else :
			parse, version = parser(cfg)

		
		if name in prev_versions:
			prev_version = prev_versions[name]
		else:
			prev_version = ""

		debug_print("[*] Compare Version : ",prev_version," -> ", version)

		if (version != prev_version) :
			if (check_str(version.split('#')[0]) and check_str(parse)) :
				global is_change
				is_change = 1
				print('# {} Update {} to {}'.format(name,prev_version,version))
				print('## Remove previous version')
				file_path_delete(prev_version,cfg['savefolder'])
				print('## Download lastest version : {}'.format(parse))
				if not os.path.exists("{}{}".format(path_public,cfg['savefolder'])):
					os.makedirs("{}{}".format(path_public,cfg['savefolder']))
				os.system('wget -q -O "{}{}{}" "{}"'.format(path_public,cfg['savefolder'],version.split('#')[0],parse))
				prev_versions[name] = version
				save_versions()
				print('## Complete!')
		else :
			print('# {} is latest version : Skip'.format(name))

	except IndexError as e:
		print('# {} occurs Error! : {}'.format(name,e))
		debug_print(traceback.print_exc())
	except KeyError as e :
		print('# {} occurs Error! : {}'.format(name,e))
		debug_print(traceback.print_exc())
	except TypeError as e :
		print('# {} occurs Error! : {}'.format(name,e))
		debug_print(traceback.print_exc())

def archive(path) :
	print('# Archive Tools folder : There is an update history')
	print('## Delete prev Tools Archive file')
	for f in os.listdir(path+'/../'):
		if re.search('tools_.*zip', f):
			print('## Remove file : {}'.format(f))
			os.remove(os.path.join(path+'/../', f))

	print('## Create New Archive file')
	date = str(datetime.datetime.now().strftime('%y%m%d'))
	shutil.make_archive('{}/../tools_{}'.format(path,date), 'zip', root_dir=path)
	print('## Create file : tools_{}.zip'.format(date))
	print('## Complete!')


print('\n\n\n#############################################')
print('# Update Start :{:^28}#'.format(str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'))))
print('# DEBUG MODE : {}'.format("ON" if DEBUG == "dev" else "OFF"))
print('#############################################')

prev_versions = load_versions()

update('Burp Suite Pro')
update('Burp Suite Community')
update('WireShark')
update('Nmap')
update('sslscan')
update('Apktool')
update('jadx')
update('ADB')
update('3utools')
update('Bitvise SSH Client')
update('Putty')
update('DBeaver')
update('DB Browser')
update('Sublime Text')
update('PickPick')
update('Python')
update('OpenJDK_Temurin')
update('hashcat')
update('FireFox')

if is_change != 0 : archive(path_public)

print('#############################################')
print('# Update End :{:^30}#'.format(str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'))))
print('#############################################')
