
import os
import time

httpd_p = os.popen("python -m http.server 5678")
time.sleep(20)
httpd_p._proc.kill()
httpd_p.close()
