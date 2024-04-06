# ii_crauler


it 


```bash
cd crawler 
alembic revision --autogenerate -m "Initial tables"
```

```bash
cd crawler 
alembic upgrade head
```

запустить контейнер Rabbit MQ после использования удалить 
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

```bash
docker run -it --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

https://www.rabbitmq.com/tutorials

pip install aio-pika