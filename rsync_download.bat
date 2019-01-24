@echo off

C:
chdir C:\Users\Administrator\cygwin\bin

chmod -R 600 /home/Administrator/.ssh/id_rsa
rsync -avP -e './ssh -p 22' --delete ylj@10.76.108.5:/home/ylj/data/ec_thin/ /cygdrive/e/data/ec_thin/
exit