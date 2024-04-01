import os
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import datetime
import json
import re
import shutil

path_public = os.getenv('PATH_PUBLIC')
version_path = os.path.dirname(__file__)+'/data/version/'
is_change = 0

def file_path_delete(prev_version,sub_path):

	check_str = ['-r ', '-rf ', '-f ', '..', '../', '\.\.', '\..', '.\.' , '*', '/bin', '/boot', '/dev', '/etc', '/home', '/root', '/usr', '/sys', '/var']
	warn = [s for s in check_str if s in prev_version]

	if (len(warn) > 0) :
		print('## Find Dangerous String [ {} ] : Skip Remove File'.format(prev_version))
	else : 
		try :
			os.remove(path_public+sub_path+prev_version)
		except FileNotFoundError :
			print('## Not Fonud [ {} ] : Skip Remove File'.format(prev_version))
		except IsADirectoryError :
			print('## Not Found [ {} ] : Skip Remove File'.format(prev_version))

def prev_version_parse(path):
	vf = open(version_path+path,'r')
	prev_version = vf.read().replace('\n', '')
	vf.close()
	return prev_version

def lastest_version_write(path, version):
	vf = open(version_path+path,'w')
	vf.write(version)
	vf.close()

def parser(url, select) :
	URL = url
	v = requests.get(URL , allow_redirects=False)
	if (select != 'Location') :
		result = bs(v.text, 'html.parser')
		return(result.select(select))
	else:
		return(v.headers[select])

def json_parse(url):
	URL = url
	v = requests.get(URL)
	#print(v.text)
	return(json.loads(v.text))

def burp_update(url,select):
	burp_parse = json_parse(url)
	for j in burp_parse['ResultSet']['Results']:
		for i in j['builds'] :
			if (i['ProductId'] == select) : 
				burp_version = i['Version']			
				return ['https://portswigger-cdn.net/burp/releases/download?product={}&version={}&type=WindowsX64'.format(select,burp_version),'burpsuite_{}_windows-x64_v{}.exe'.format(select,'_'.join(burp_version.split('.')))]

# github download 20230731
def github_update(url,select):
	git_parse = json_parse(url)
	regex = re.compile(select)
	for i in git_parse['assets']:
		try :
			regex.match(i['name']).start() 
			return [i['browser_download_url'],i['name']]
		except AttributeError :
			continue

def update(name,url,select,version_file,sub_path) :

	try: 
		if (name == 'Burp Suite Pro' or name == 'Burp Suite Community'):
			temp_result = burp_update(url,select)
			parse = temp_result[0]
			version = temp_result[1]
		elif (name == 'Bitvise SSH Client') :
			parse = parser(url,select)[0]
			parse = parse.find('a')['href']+'#'+parse.text.split(',')[0].split(':')[1].strip()
			version = parse.split('/')[-1]
		elif (name.find("github") != -1) :
			temp_result = github_update(url,select)
			parse = temp_result[0]
			version = temp_result[1]
		elif (name == 'PickPick') :
			parse = parser(url,select)[0]['href']
			version = parse.split('/')[-1]+'#'+parse.split('/')[-2]
		elif (name == 'Putty') :
			parse = parser(url,select)
			version = "putty.exe#"+re.sub(r'[^0-9\.]', '', parse[0].text)
			parse = 'https://the.earth.li/~sgtatham/putty/'+re.sub(r'[^0-9\.]', '', parse[0].text)+'/w64/'+version
		elif (name == 'ADB') :
			version = 'platform-tools_r{}-windows.zip'.format(parser(url,select)[0].text.split(' ')[0])
			parse = 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip'
		elif (name == '3utools') :
			parse = parser(url,select)
			version = parse.split('/')[-1]
		else :
			parse = parser(url,select)[0]['href']
			version = parse.split('/')[-1]
			
		prev_version = prev_version_parse(version_file)

		if (version != prev_version) :
			global is_change
			is_change = 1
			print('# {} Update {} to {}'.format(name,prev_version,version))
			print('## Remove previous version')
			file_path_delete(prev_version,sub_path)
			print('## Download lastest version')
			os.system('wget -O {}{}{} "{}"'.format(path_public,sub_path,version.split('#')[0],parse))
			lastest_version_write(version_file,version)
			print('## Complete!')
		else :
			print('# {} is latest version : Skip'.format(name))

	except IndexError as e:
		print('# {} occurs Error! : {}'.format(name,e))
	except KeyError as e :
		print('# {} occurs Error! : {}'.format(name,e))

def archive(path) :

	print('# Archive Tools folder : There is an update history')
	print('## Delete prev Tools Archive file')
	for f in os.listdir(path+'/../'):
		if re.search('tools_.*zip', f):
			print('## Remove file : {}'.format(f))
			os.remove(os.path.join(path+'/../', f))

	print('## Create New Archive file')
	date = str(datetime.datetime.now().strftime("%y%m%d"))
	shutil.make_archive('{}/../tools_{}'.format(path,date), 'zip', root_dir=path)
	print('## Create file : tools_{}.zip'.format(date))
	print('## Complete!')


print('\n\n\n#############################################')
print('# Update Start :{:^28}#'.format(str(datetime.datetime.now().strftime("%Y/%m/%d %H:%m"))))
print('#############################################')

update('Burp Suite Pro','https://portswigger.net/burp/releases/data?pageSize=6','pro','burppro_version','Proxy/')
update('Burp Suite Community','https://portswigger.net/burp/releases/data?pageSize=6','community','burpcom_version','Proxy/')
update('WireShark','https://www.wireshark.org/download.html','#download-accordion > div:nth-child(1) > details > div > ul > li:nth-child(1) > a','wireshark_version','Network/')
update('Nmap','https://nmap.org/download','b > a','nmap_version','Network/')
update('github_sslscan','https://api.github.com/repos/rbsec/sslscan/releases/latest','sslscan-[0-9.]+.zip','sslscan_version','Network/')
update('github_Apktool','https://api.github.com/repos/iBotPeaches/Apktool/releases/latest','apktool_[0-9.]+','apktool_version','Mobile/')
update('github_jadx','https://api.github.com/repos/skylot/jadx/releases/latest','jadx-gui-[0-9.]+-with-jre-win','jadx_version','Mobile/')
update('ADB', 'https://developer.android.com/tools/releases/platform-tools?hl=ko','h4','adb_version','Mobile/')
update('3utools','https://url.3u.com/zmAJjyaa','Location','3utools_version','Mobile/')
update('Bitvise SSH Client','https://www.bitvise.com/ssh-client-download','#content > div','bitvise_version','SSH/')
update('Putty','https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html','body > h1','putty_version','SSH/')
update('github_DBeaver','https://api.github.com/repos/dbeaver/dbeaver/releases/latest','dbeaver-ce-[0-9.]+-x86_64-setup.exe','DBeaver_version','DB/')
update('DB Browser', 'https://sqlitebrowser.org/dl/','body > div > main > article > div > ul:nth-child(4) > li:nth-child(3) > a','dbbrowser_version','DB/')
update('Sublime Text','https://www.sublimetext.com/download_thanks?target=win-x64','#direct-downloads > li:nth-child(1) > a:nth-child(1)','sublime_version','Editor/')
update('PickPick','https://picpick.net/download/kr/','#gatsby-focus-wrapper > div > div > div:nth-child(3) > div > p > a:nth-child(2)','pickpick_version','Editor/')
update('Python','https://www.python.org/downloads/','#touchnav-wrapper > header > div > div.header-banner > div > div.download-os-windows > p > a','python_version','Language/')
update('github_hashcat','https://api.github.com/repos/hashcat/hashcat/releases/latest','hashcat-[0-9.]+.7z','hashcat_version','Cracker/')

if is_change != 0 : archive(path_public)

print('#############################################')
print('#{:^43}#'.format('Update End'))
print('#############################################')
