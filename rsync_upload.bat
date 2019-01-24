@echo off

C:
chdir C:\Users\Administrator\cygwin\bin

chmod -R 600 /home/Administrator/.ssh/id_rsa
rsync -avP  -e './ssh -p 873' --delete /cygdrive/e/data/ec_thin/ root@119.163.126.132:/home/DATA/ECMWF/
exit