cd /home/ubuntu/ECE-1779/intro-cloud-a1
source activate py3
gunicorn server:app --bind 0.0.0.0:5000 --workers=8 --worker-class gevent --access-logfile access.log --error-logfile error.log &