#!/usr/bin/env python3
"""Local static host. No model credentials, chat or notes are stored by this server."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse, functools, urllib.request, webbrowser
ROOT=Path(__file__).resolve().parent/'dist'
class Handler(SimpleHTTPRequestHandler):
 def end_headers(self):
  self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');super().end_headers()
 def log_message(self,*args):pass
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--open',action='store_true');p.add_argument('--port',type=int,default=8765);a=p.parse_args();url=f'http://127.0.0.1:{a.port}/'
 try:server=ThreadingHTTPServer(('127.0.0.1',a.port),functools.partial(Handler,directory=str(ROOT)))
 except OSError as e:
  try:
   with urllib.request.urlopen(url,timeout=2) as r:body=r.read(4096).decode('utf-8')
   if 'Picked' not in body:raise RuntimeError('端口已被其他应用占用')
   print('Picked 已在运行：'+url)
   if a.open:webbrowser.open(url)
  except Exception:print(f'端口不可用：{e}。可用 --port 8766 指定其他端口。')
 else:
  print('Picked 已启动：'+url+'\n关闭此窗口或按 Ctrl+C 停止。',flush=True)
  if a.open:webbrowser.open(url)
  try:server.serve_forever()
  except KeyboardInterrupt:server.server_close()
