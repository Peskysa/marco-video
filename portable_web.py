"""Read-only loopback launcher. Files chosen in the browser never reach this server."""
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json, sys, threading, webbrowser
import tkinter as tk
from tkinter import ttk

ROOT=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))
TRANSLATIONS=json.loads((ROOT/'translations.json').read_text(encoding='utf-8'))

class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
    def list_directory(self,path): self.send_error(403)
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Cache-Control','no-store')
        super().end_headers()

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT/'dist/web')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/'
    if '--serve-test' in sys.argv:
        target=Path(sys.argv[sys.argv.index('--serve-test')+1]); target.write_text(json.dumps({'url':url,'pid':__import__('os').getpid()}),encoding='utf-8')
        try: threading.Event().wait(120)
        finally: server.shutdown();server.server_close()
        return
    window=tk.Tk();window.title('Marco Vídeo · Web portable');window.geometry('540x235');window.resizable(False,False)
    language=tk.StringVar(value='Español');combo=ttk.Combobox(window,values=['Español','English','Français'],state='readonly',textvariable=language);combo.pack(pady=(20,12))
    note=ttk.Label(window,wraplength=480,justify='center');note.pack(padx=20,pady=12)
    open_button=ttk.Button(window,command=lambda:webbrowser.open(url));open_button.pack(pady=6)
    close_button=ttk.Button(window,command=window.destroy);close_button.pack(pady=6)
    def translate(*_):
        tr=TRANSLATIONS[{'Español':'es','English':'en','Français':'fr'}[language.get()]];note.config(text=tr['portable']);open_button.config(text=tr['openBrowser']);close_button.config(text=tr['close'])
    combo.bind('<<ComboboxSelected>>',translate);translate();window.after(400,lambda:webbrowser.open(url))
    try: window.mainloop()
    finally: server.shutdown();server.server_close()

if __name__=='__main__':main()
