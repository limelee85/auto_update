CONFIG = {
    "Burp Suite Desktop": {
        "type": "json",
        "url": "https://portswigger.net/burp/releases/data?pageSize=6",
        "iter_path": ["ResultSet", "Results"],
        "select": "Professional",
        "ckey": "title",
        "result": {
            "download": (
                "https://portswigger-cdn.net/burp/releases/download"
                "?product=desktop&version={version}&type=WindowsX64"
            ),
            "filename": "burpsuite_desktop_windows-x64_v{version}.exe",
            "fields": ["title", "version"]
        },
        "savefolder":"Proxy/"
    },
    "sslscan": {
        "type": "json",
        "url" : "https://api.github.com/repos/rbsec/sslscan/releases/latest",
        "iter_path": ["assets"],
        "select": "sslscan-[0-9.]+.zip",
        "ckey": "name",
        "result": {
            "download": "{browser_download_url}",
            "filename": "{name}",
            "fields": ["browser_download_url", "name"]
        },
        "savefolder":"Network/"
    },
    "Apktool": {
        "type": "json",
        "url" : "https://api.github.com/repos/iBotPeaches/Apktool/releases/latest",
        "iter_path": ["assets"],
        "select": "apktool_[0-9.]+",
        "ckey": "name",
        "result": {
            "download": "{browser_download_url}",
            "filename": "{name}",
            "fields": ["browser_download_url", "name"]
        },
        "savefolder":"Mobile/"
    },
    "jadx": {
        "type": "json",
        "url" : "https://api.github.com/repos/skylot/jadx/releases/latest",
        "iter_path": ["assets"],
        "select": "jadx-gui-[0-9.]+-with-jre-win",
        "ckey": "name",
        "result": {
            "download": "{browser_download_url}",
            "filename": "{name}",
            "fields": ["browser_download_url", "name"]
        },
        "savefolder":"Mobile/"
    },
    "DBeaver": {
        "type": "json",
        "url" : "https://api.github.com/repos/dbeaver/dbeaver/releases/latest",
        "iter_path": ["assets"],
        "select": "dbeaver-ce-[0-9.]+-x86_64-setup.exe",
        "ckey": "name",
        "result": {
            "download": "{browser_download_url}",
            "filename": "{name}",
            "fields": ["browser_download_url", "name"]
        },
        "savefolder":"DB/"
    },
    "OpenJDK_Temurin": {
        "type": "json",
        "url" : "https://api.github.com/repos/adoptium/temurin8-binaries/releases/latest",
        "iter_path": ["assets"],
        "select": "OpenJDK8U-jdk_x64_windows_hotspot_[0-z]+.msi",
        "ckey": "name",
        "result": {
            "download": "{browser_download_url}",
            "filename": "{name}",
            "fields": ["browser_download_url", "name"]
        },
        "savefolder":"Language/"
    },
    "hashcat": {
        "type": "json",
        "url" : "https://api.github.com/repos/hashcat/hashcat/releases/latest",
        "iter_path": ["assets"],
        "select": "hashcat-[0-9.]+.7z",
        "ckey": "name",
        "result": {
            "download": "{browser_download_url}",
            "filename": "{name}",
            "fields": ["browser_download_url", "name"]
        },
        "savefolder":"Cracker/"
    },
    "WireShark": {
        "type": "default",
        "url" : "https://www.wireshark.org/download.html",
        "iter_path": ["href"],
        "select": "#download > ul > li:nth-child(1) > details > div > ul > a:nth-child(1)",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}"
        },
        "savefolder":"Network/"
    },
    "Nmap": {
        "type": "default",
        "url" : "https://nmap.org/download",
        "iter_path": ["href"],
        "select": "b > a",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}"
        },
        "savefolder":"Network/"
    },
    "ADB": {
        "type": "default",
        "url" : "https://developer.android.com/tools/releases/platform-tools?hl=ko",
        "iter_path": "text",
        "select": "h4",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>\\S+)",
            "download": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
            "filename": "platform-tools_r{filename}-windows.zip"
        },
        "savefolder":"Mobile/"
    },
    "3utools": {
        "type": "default",
        "url" : "https://url.3u.com/zmAJjyaa",
        "iter_path": "text",
        "select": "Location",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}"
        },
        "savefolder":"Mobile/"
    },
    "FireFox": {
        "type": "default",
        "url" : "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=ko",
        "iter_path": "text",
        "select": "Location",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}"
        },
        "savefolder":"Browser/"
    },

    #"Bitvise SSH Client": {
    #    "type": "default",
    #    "url" : "https://bitvise.com/ssh-client-download",
    #    "iter_path": "default",
    #    "select": "#content > div",
    #    "result": {
    #        "download_regex": '<a[^>]*href="(?P<download>[^"]+)"[^>]*>',
    #        "filename_regex": '<a[^>]*href="(https?://.*/)(?P<filename>[^/"]+)"[^>]*>.*?</a>.*?Current version:\\s*(?P<version>[0-9.]+)',
    #        "download": "{download}",
    #        "filename": "{filename}#{version}"
    #    },
    #    "savefolder":"SSH/"
    #},
    "Bitvise SSH Client": {
        "type": "default",
        "url" : "https://bitvise.com/ssh-client-download",
        "iter_path": "default",
        "select": "#content > div",
        "result": {
            "download_regex": '(?P<download>^.*)$',
            "filename_regex": '.*?Current version:\\s*(?P<version>[0-9.]+)',
            "download": "https://dl.bitvise.com/BvSshClient-Inst.exe",
            "filename": "BvSshClient-Inst.exe#{version}"
        },
        "savefolder":"SSH/"
    },
    "Putty": {
        "type": "default",
        "url" : "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html",
        "iter_path": "text",
        "select": "body > h1",
        "result": {
            "download_regex": '\((?P<version>[0-9.]+)\)',
            "filename_regex": '\((?P<version>[0-9.]+)\)',
            "download": "https://the.earth.li/~sgtatham/putty/{version}/w64/putty.exe",
            "filename": "putty.exe#{version}"
        },
        "savefolder":"SSH/"
    },
    "DB Browser": {
        "type": "default",
        "url" : "https://sqlitebrowser.org/dl/",
        "iter_path": ["href"],
        "select": "body > div > main > article > div > ul:nth-child(4) > li:nth-child(3) > a",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}"
        },
        "savefolder":"DB/"
    },
    "Sublime Text": {
        "type": "default",
        "url" : "https://www.sublimetext.com/download_thanks?target=win-x64",
        "iter_path": ["href"],
        "select": "#direct-downloads > li:nth-child(1) > a:nth-child(1)",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}"
        },
        "savefolder":"Editor/"
    },
    "PickPick": {
        "type": "default",
        "url" : "https://picpick.net/download/kr/",
        "iter_path": ["href"],
        "select": "#gatsby-focus-wrapper > div > div > div:nth-child(3) > div > p > a:nth-child(2)",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "https?://[^/]+/(?P<version>[0-9.]+)/(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}#{version}"
        },
        "savefolder":"Editor/"
    },
    "Python": {
        "type": "default",
        "url" : "https://www.python.org/downloads/",
        "iter_path": ["href"],
        "select": "#touchnav-wrapper > header > div > div.header-banner > div > div.download-os-windows > p:nth-of-type(2) > a",
        "result": {
            "download_regex": "(?P<download>^.*)$",
            "filename_regex": "(?P<filename>[^/]+)$",
            "download": "{download}",
            "filename": "{filename}"
        },
        "savefolder":"Language/"
    },
}
