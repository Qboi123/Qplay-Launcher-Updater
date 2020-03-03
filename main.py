import wx
import wx._core
import io

from typing import Iterable, Union


class Checker(object):
    def __init__(self, state='a'):
        import xml.etree.ElementTree as ET
        import urllib.request
        import urllib.error
        import urllib.parse
        print("[Checker]: State: %s" % state)
        # noinspection PyExceptClausesOrder
        url = urllib.request.urlopen(
            "https://github.com/Qboi123/Qplay-Launcher/raw/master/updates.xml"
        )
        output = url.read().decode()
        self._has_internet = True
        # except urllib.error.URLError:
        #     self._has_internet = False
        #     return
        # except urllib.error.HTTPError:
        #     self._has_internet = False
        #     return

        root = ET.fromstring(output)
        for index in range(len(root)):
            if root[index].attrib["state"] >= state:
                item_i = index
                break

        try:
            self.newest = root[item_i]
        except NameError:
            self.newest = root[0]
        print(self.newest)
        #
        # for index in range(len(root)-1, -1, -1):
        #     print(root[index].attrib["state"])
        #     if root[index].attrib["state"] >= state:
        #         item_i = index
        #         print(root[index].attrib)
        self.updates_xml = output

    def isNewest(self):
        import xml.etree.ElementTree as ET
        import os
        if os.path.exists(os.getcwd().replace("\\", "/") + "/updates.xml"):
            with open(os.getcwd().replace("\\", "/") + "/updates.xml", "r") as file:
                root = ET.fromstring(file.read())
                file.close()
            for child in root:
                print(child.tag, child.attrib)

            self.current = root[0]
            if self.newest.attrib["time"] <= self.current.attrib["time"]:
                return True
            else:
                return False
        else:
            return False

    def getNewestRelease(self):
        import xml.etree.ElementTree as ET
        import os
        if os.path.exists(os.getcwd().replace("\\", "/") + "/updates.xml"):
            with open(os.getcwd().replace("\\", "/") + "/updates.xml", "r") as file:
                root = ET.fromstring(file.read())
                file.close()
            for child in root:
                print(child.tag, child.attrib)

            self.current = root[0]

            if self.newest.attrib["time"] <= self.current.attrib["time"]:
                return True
            else:
                return False
        else:
            return False

    def hasInternet(self):
        return self._has_internet

    def _getCurrent(self):
        pass

    def getXML(self):
        return self.updates_xml

    def getUpdateURL(self):
        try:
            return self.newest.attrib["url"]
        except AttributeError:
            self.__init__('r')
            return self.newest.attrib["url"]


class Updater(wx.Panel):
    def __init__(self, url, xml, version, subversion, release, state, statebuild):
        import os
        v = version
        sv = subversion
        r = release
        st = state
        stb = statebuild

        if (((not os.path.exists("%s/game/downloaded" % os.getcwd().replace("\\", "/"))) or not checker.isNewest()) or
                not (os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")))) or (
                not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/"))) or (
                not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/"))):
            self.load = wx.ProgressDialog("Please Wait...", "")

        if (not os.path.exists("%s/game/downloaded" % os.getcwd().replace("\\", "/"))) or not checker.isNewest():
            print("[Updater]: Downloading Launcher")
            launcher = self.download(url, "Downloading Launcher")
        if not os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Downloading Runtime")
            runtime = self.download("https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-amd64.zip",
                                    message="Downloading Runtime")
        if not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Downloading Tkinter")
            tkinter = self.download("https://github.com/Qboi123/Tkinter-Python/archive/8.6.9.zip",
                                    message="Downloading Tkinter")
        if not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Downloading Pip Installer")
            pip = self.download("https://bootstrap.pypa.io/get-pip.py", fp="get-pip.py",
                                message="Downloading Pip Installer")

        if (not os.path.exists("%s/game/downloaded" % os.getcwd().replace("\\", "/"))) or not checker.isNewest():
            print("[Updater]: Extracting Launcher")
            self.extract(launcher, "%s/game" % os.getcwd().replace("\\", "/"), "Extracting Launcher",
                         "Qplay-Launcher-",
                         v, sv, r, st, stb)
            with open("%s/game/downloaded" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
        if not os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Extracting Runtime")
            self.extract(runtime, "%s/runtime" % os.getcwd().replace("\\", "/"), "Extracting Runtime")
            with open("%s/runtime/downloaded" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
        if not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Extracing Tkinter")
            self.extract(tkinter, "%s/runtime" % os.getcwd().replace("\\", "/"), "Extracting Tkinter",
                         "Tkinter-Python-", 8, 6, 9, 'r')
            with open("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
        if not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/")):
            import shutil
            self.load.SetTitle("Installing...")
            self.load.SetRange(100)
            self.load.Update(0, "Installing...\nInstalling Pip")

            runtime_dir = "%s/runtime" % os.getcwd().replace("\\", "/")

            print("[Updater]: Extracing from './runtime/python37.zip' to './runtime/Lib'")
            self.extract(runtime_dir+"/python37.zip", runtime_dir+"/Lib/", "Extracing...\nExtracting Python Runtime Library")

            exitcode = 1

            print("[Updater]: Executing Pip Installer")
            while exitcode == 1:
                exitcode = os.system("runtime\\python.exe temp/get-pip.py")
            print("Pip exited with code: %s" % exitcode)

            self.load.Update(66, "Installing...\nInstalling Pip")

            self.replace_in_file("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), "#import site", "import site")
            self.replace_in_file("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), ".\n",
                                 "./Lib\n./DLLs")
            dlls = """runtime/_sqlite3.pyd
runtime/_lzma.pyd
runtime/_hashlib.pyd
runtime/_decimal.pyd
runtime/select.pyd
runtime/_socket.pyd
runtime/_elementtree.pyd
runtime/_multiprocessing.pyd
runtime/_overlapped.pyd
runtime/_asyncio.pyd
runtime/_msi.pyd
runtime/_queue.pyd
runtime/_ctypes.pyd
runtime/_bz2.pyd
runtime/libcrypto-1_1.dll
runtime/libssl-1_1.dll
runtime/pyexpat.pyd
runtime/_tkinter.pyd
runtime/_ssl.pyd
runtime/tk86t.dll
runtime/tcl86t.dll
runtime/unicodedata.pyd
runtime/winsound.pyd"""
            dlls = dlls.split("\n")
            if not os.path.exists("%s/runtime/DLLs/" % os.getcwd().replace("\\", "/")):
                os.makedirs("%s/runtime/DLLs/" % os.getcwd().replace("\\", "/"))
                self.load.Update(70, "Installing...\nInstalling Pip")

            for file in dlls:
                dst = file.replace("runtime/", "runtime/DLLs/")
                shutil.copy(("%s/"+file) % os.getcwd().replace("\\", "/"), ("%s/"+dst) % os.getcwd().replace("\\", "/"))
            self.load.Update(81, "Installing...\nInstalling Pip")


            if not os.path.exists(runtime_dir+'/Lib/tkinter'):
                shutil.move(runtime_dir+"/tkinter", runtime_dir+"/Lib")
            # with open("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), "r") as file:
            #     a = file.read()
            #     self.load.Update(77, "Installing...\nInstalling Pip")
            # with open("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), "w") as file:
            #     a = a.replace("#import site", "import site")
            #     file.write(a)
            #     self.load.Update(88, "Installing...\nInstalling Pip")
            # with open("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/"), "w+") as file:
            #     file.write("True")

            self.load.Update(82, "Installing...\nInstalling Pip: \nExtracing Python Runtime Library")


            with open("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
                file.close()

        if (not os.path.exists("%s/game/downloaded" % os.getcwd().replace("\\", "/")) or not (
                os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")))) or (
                not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/"))) or (
                not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/"))):
            self.load.Destroy()

        if (not os.path.exists("%s/game/patched" % os.getcwd().replace("\\", "/")))  or not checker.isNewest():
            print("[Updater]: Patching Launcher")
            add = """import sys, os
sys.path.append(os.getcwd().replace("\\\\", "/"))
"""
            with open("%s/game/launcher.pyw" % os.getcwd().replace("\\", "/"), "r") as file:
                file_launcher = file.read()
            with open("%s/game/launcher.pyw" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write(add + file_launcher)
            with open("%s/game/patched" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
                file.close()
        if not os.path.exists("%s/runtime/packages_installed" % os.getcwd().replace("\\", "/")):
            with open("%s/game/requirements.txt" % os.getcwd().replace("\\", "/"), "r") as file:
                print("[Updater]: Installing Libraries")
                self.install_libraries(file.read())
                file.close()
            with open("%s/runtime/packages_installed" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
                file.close()

        with open("%s/updates.xml" % os.getcwd().replace("\\", "/"), "w+") as file:
            file.write(xml)

    def replace_in_file(self, fp, old, new):
        with open(fp, "r") as file:
            d = file.read()
        with open(fp, "w") as file:
            d = d.replace(old, new)
            file.write(d)

    def extract(self, file, dir, message, folder=None, v=None, sv=None, r=None, st=None, stb=None):
        import zipfile
        import os
        import shutil

        if st == "a":
            copy = "%s.%s.%s-%s.%s" % (v, sv, r, "alpha", stb)
        elif st == "b":
            copy = "%s.%s.%s-%s.%s" % (v, sv, r, "beta", stb)
        elif st == "c":
            copy = "%s.%s.%s-%s.%s" % (v, sv, r, "rc", stb)
        elif st == "r":
            copy = "%s.%s.%s" % (v, sv, r)
        else:
            copy = None

        self.load.SetTitle("Extracting...")
        self.load.SetRange(100)
        self.load.Update(0, "Extracing...\n" + message)

        zip_file = zipfile.ZipFile(file)
        if copy is not None:
            print("[Checking]:", folder == "Qplay-Launcher-")
            print("[Checking]:", folder)
            if folder == "Qplay-Launcher-":
                shutil.rmtree('%s/game' % os.getcwd().replace("\\", "/"), ignore_errors=True)
            self.load.Update(1, "Extracing...\n" + message)
            zip_file.extractall("%s/temp" % os.getcwd().replace("\\", "/"))
            self.load.Update(98, "Extracing...\n" + message)
            print(("%s/temp/" + folder + "%s") % (os.getcwd().replace("\\", "/"), copy), dir)
            if folder == "Tkinter-Python-":
                for item in os.listdir(("%s/temp/" + folder + "%s") % (os.getcwd().replace("\\", "/"), copy)):
                    shutil.move(("%s/temp/" + folder + "%s/" + item) % (os.getcwd().replace("\\", "/"), copy),
                               dir + "/" + item)
            else:
                shutil.move(("%s/temp/" + folder + "%s") % (os.getcwd().replace("\\", "/"), copy), dir)

            while not os.path.exists(dir):
                time.sleep(1)
        else:
            if not os.path.exists(dir):
                os.makedirs(dir)
            self.load.Update(99, "Extracing...\n" + message)
            zip_file.extractall(dir)

        self.load.Update(100, "Extracing...\n" + message)

    def download(self, url, message="Downloading Launcher", wait=False, fp=None):
        import random
        import os

        self.load.SetTitle("Downloading...")
        self.load.SetRange(100)
        self.load.Update(0, "Downloading...\n" + message)

        value = random.randint(0x100000000000, 0xffffffffffff)
        if fp is None:
            filepath = hex(value)[2:] + ".tmp"
        else:
            filepath = fp

        if not os.path.exists("%s/temp" % os.getcwd().replace("\\", "/")):
            os.makedirs("%s/temp" % os.getcwd().replace("\\", "/"))

        download = Download(url, "%s/temp/%s" % (os.getcwd().replace("\\", "/"), filepath))
        # Thread(None, download.download, "DownloadThread")

        self.load.SetRange(download.file_total_bytes + 1)
        while not download.downloaded:
            # print("Downloaded: ", download.file_downloaded_bytes)
            # print("Total: ", download.file_total_bytes)
            try:
                self.load.SetRange(download.file_total_bytes + 1)
                self.load.Update(download.file_downloaded_bytes, "Downloading...\n" + message)
            except wx._core.wxAssertionError:
                pass

        # load.Destroy()

        return "%s/temp/%s" % (os.getcwd().replace("\\", "/"), filepath)

    def install_libraries(self, requirements: str):
        import os
        import subprocess

        req = requirements.replace("\n", ", ")

        requirements = requirements.replace("\n", " ")
        print("[Run-Pip]: Installing Packages: %s" % req)
        application = '"%s/runtime/python.exe"' % os.getcwd().replace("\\", "/")
        args = " -m pip install "+requirements
        cmd = application+args

        print("[Run-Pip]: %s" % cmd)

        process = os.system(cmd)
        print("[Run-Pip]: Process Returned: %s" % process)
        if process != 0:
            print('[Run-Pip]: Retrying with subprocess...')
            process = subprocess.call([application, "-m", "pip", "install", *requirements.split(" ")])
            while process is None:
                time.sleep(1)
            print("[Run-Pip]: Process Returned: %s" % process)

    def run(self):
        import os
        # import subprocess

        os.chdir("%s/game" % os.getcwd().replace("\\", "/"))

        import subprocess
        file = '%s/../runtime/python.exe' % os.getcwd().replace("\\", "/")
        py = '%s/launcher.pyw' % os.getcwd().replace("\\", "/")
        # print('[Run]: "{file}" "{py}"'.format(file=file, py=py))
        cmd = '"{file}" "{py}"'.format(file=file, py=py)

        print("[Run-Game]: %s" % cmd)

        process = os.system(cmd)
        print("[Run-Game]: Process Returned: %s" % process)
        if process != 0:
            print('[Run-Game]: Retrying with subprocess...')
            subprocess.call([file, py])
            while process is None:
                time.sleep(1)
            print("[Run-Game]: Process Returned: %s" % process)

        # print("[Run]: \"%s/../runtime/python.exe\" \"%s/launcher.pyw\"" % (
        #     os.getcwd().replace("\\", "/"), os.getcwd().replace("\\", "/")))
        #
        # subprocess.run(("%s/../runtime/python.exe"% os.getcwd().replace("\\", "/"),
        #                "%s/launcher.pyw\"" % os.getcwd().replace("\\", "/")), stderr=stderr, stdout=stdout)


class Process():
    def __init__(self):

        self.process = None
        # self.process.Bind(wx.EVT_IDLE, self.OnIdle)

        # We can either derive from wx.Process and override OnTerminate
        # or we can let wx.Process send this window an event that is
        # caught in the normal way...
        # self.process.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)

    def OnExecuteBtn(self, cmd):

        self.process = wx.Process(self)
        self.process.Redirect()
        pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
        print('OnExecuteBtn: "%s" pid: %s\n' % (cmd, pid))
        #
        # self.inp.Enable(True)
        # self.sndBtn.Enable(True)
        # self.termBtn.Enable(True)
        # self.cmd.Enable(False)
        # self.exBtn.Enable(False)
        # self.inp.SetFocus()

    def Execute(self, command):
        self.OnExecuteBtn(command)

    def OnSendText(self, text):
        print('OnSendText: "%s"\n' % text)
        text += '\n'
        self.process.GetOutputStream().write(text.encode('utf-8'))

    def Send(self, text):
        self.OnSendText(text)

    def OnCloseStream(self):
        print('OnCloseStream\n')
        self.process.CloseOutput()

    def Close(self):
        self.OnCloseStream()

    def OnIdle(self):
        if self.process is not None:
            stream = self.process.GetInputStream()
            errstream = self.process.GetErrorStream()

            if stream.CanRead():
                text = stream.read()
                sys.stdout.write(text)
            if stream.CanRead():
                stderr = errstream.read()
                sys.stderr.write(stderr)

    def OnProcessEnded(self, evt):
        print('OnProcessEnded, pid:%s,  exitCode: %s\n' %
              (evt.GetPid(), evt.GetExitCode()))

        stream = self.process.GetInputStream()
        errstream = self.process.GetErrorStream()

        if stream.CanRead():
            text = stream.read()
            sys.stdout.write(text)
        if stream.CanRead():
            stderr = errstream.read()
            sys.stderr.write(stderr)

        self.process.Destroy()
        self.process = None
        import os
        os.kill(os.getpid(), 0)

    def ShutdownDemo(self):
        # Called when the demo application is switching to a new sample. Tell
        # the process to close (by closign its output stream) and then wait
        # for the termination signals to be received and processed.
        if self.process is not None:
            self.process.CloseOutput()
            wx.MilliSleep(250)
            wx.Yield()
            self.process = None


class Download:
    def __init__(self, url, fp):
        from threading import Thread
        self._url = url
        self._fp = fp
        self.file_total_bytes = 1
        self.file_downloaded_bytes = 0
        self.downloaded: bool = False

        Thread(None, self.download).start()

    # noinspection PyUnboundLocalVariable
    def download(self):
        import urllib.request
        import os

        self.downloaded = False

        global active
        global total
        global spd
        global h, m, s
        global load
        h = "23"
        m = "59"
        s = "59"
        spd = 0
        total = 0

        dat = None

        while dat is None:
            # Get the total number of bytes of the file to download before downloading
            u = urllib.request.urlopen(str(self._url))
            if os.path.exists(self._fp):
                os.remove(self._fp)
            meta = u.info()
            dat = meta["Content-Length"]
        self.file_total_bytes = int(dat)

        data_blocks = []
        total = 0

        # Thread(None, lambda: speed(), "SpeedThread").start()

        while True:
            block = u.read(1024)
            data_blocks.append(block)
            self.file_downloaded_bytes += len(block)
            _hash = ((60 * self.file_downloaded_bytes) // self.file_total_bytes)
            if not len(block):
                active = False
                break

            try:
                with open(self._fp, "ab+") as f:
                    f.write(block)
                    f.close()
            except FileNotFoundError:
                os.makedirs("%s/temp/" % os.getcwd().replace("\\", "/"))
                with open(self._fp, "ab+") as f:
                    f.write(block)
                    f.close()

        # data = b''.join(data_blocks)
        u.close()

        self.downloaded = True


class Log(io.IOBase):
    def __init__(self, file, std, name="Out"):
        self.file = file
        self.std = std
        self.name = name
        self.old = "\n"
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def write(self, o: str):
        if self.old[-1] == "\n":
            self.std.write("[" + time.ctime(time.time()) + "] [" + self.name + "]: " + o)
            self.fp = open(self.file, "a+")
            self.fp.write("[" + time.ctime(time.time()) + "] [" + self.name + "]: " + o)
            self.fp.close()
        else:
            self.std.write(o)
            self.fp = open(self.file, "a+")
            self.fp.write(o)
            self.fp.close()
        self.old = o

    def writelines(self, lines: Iterable[Union[bytes, bytearray]]) -> None:
        for line in lines:
            self.write(line)

    def potato(self, exefile):
        self.flush()

    def flush(self):
        pass

    def fileno(self):
        self.fp = open(self.file, "a+")
        return self.fp.fileno()

    def read(self):
        import time
        a = self.std.read()
        self.fp = open(self.file, "a+")
        self.fp.write("[{time}] [In]: ".format(time=time.ctime(time.time())) + a)
        self.fp.close()


if __name__ == '__main__':
    import sys, os, time

    startup = time.time()
    startup2 = time.ctime(startup).replace(" ", "-").replace(":", ".")

    if not os.path.exists("%s/logs" % os.getcwd().replace("\\", "/")):
        os.makedirs("%s/logs" % os.getcwd().replace("\\", "/"))

    if not os.path.exists("%s/errors" % os.getcwd().replace("\\", "/")):
        os.makedirs("%s/errors" % os.getcwd().replace("\\", "/"))

    log_file = time.strftime("%m-%d-%Y %H.%M.%S.log", time.gmtime(startup))

    # stderr = open(os.getcwd().replace("\\", "/") + "/logs/stderr-" + hex(int(startup))[2:]+".log", "w+")
    # stdout = open(os.getcwd().replace("\\", "/") + "/logs/stdout-" + hex(int(startup))[2:]+".log", "w+")
    stderr = Log(os.getcwd().replace("\\", "/") + "/errors/" + log_file, sys.__stderr__,
                 "Err")
    stdout = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__)
    stdin = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__)
    sys.stderr = stderr
    sys.stdout = stdout
    sys.stdin = stdin

    checker = Checker(state="r")
    print("[Updater]: hasInternet()=%s" % checker.hasInternet())
    print("[Updater]: isNewest()=%s" % checker.isNewest())
    print("[Updater]: getUpdateURL()=%s" % checker.getUpdateURL())

    b = checker.newest.attrib

    if (not checker.isNewest()) or (not checker.hasInternet()) or \
            ((not os.path.exists("%s/game/downloaded" % os.getcwd().replace("\\", "/")) or not (
                    os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")))) or (
            not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/"))) or (
            not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/")))):
        app = wx.App()
        # root = wx.Frame()
        # root.Show(False)
        a = Updater(checker.getUpdateURL(), checker.getXML(), b["version"], b["subversion"], b["release"],
                    b["state"],
                    b["statebuild"])
        app.Destroy()
        a.run()
    else:
        Updater.run(Updater)
