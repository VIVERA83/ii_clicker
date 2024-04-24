# ii_crauler
______
Запуск приложения:
```bash
cd rpc_clicker && python main.py
```

---

```bash
docker build -t rpc_clicker .
```

```bash
docker run --rm --name ii_rpc_clicker rpc_clicker       
```

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



```bash
docker build -t vivera83/ii_magnum:1 .
```  

```bash
docker push vivera83/ii_magnum:1
```  


https://www.rabbitmq.com/tutorials

pip install aio-pika
http://<i>{node-hostname}</i>:15672/
http://localhost:15672/