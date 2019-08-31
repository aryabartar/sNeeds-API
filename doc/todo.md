## Celery config

sudo apt-get install -y erlang  
sudo apt-get install rabbitmq-server  
sudo systemctl enable rabbitmq-server  
sudo systemctl start rabbitmq-server  
sudo systemctl status rabbitmq-server # Check status  

Use redis as broker and make sure redis server is always up. 


#Redis 
 5044  src/redis-server ping
 5047  src/redis-server --daemonize yes
 5048  src/redis-cli ping

