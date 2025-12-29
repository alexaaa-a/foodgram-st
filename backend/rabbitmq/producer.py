import json
import pika
import sys

sys.path.insert(0, '/app')

from rabbitmq.vault_helper import vault_helper

def get_vault_data():
    vault_credentials = vault_helper.get_rabbitmq_credentials()
    return vault_credentials

def send_task(task_name, params=None):
    secrets = get_vault_data()
    credentials = pika.PlainCredentials(
        **secrets
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq.foodgram.svc.cluster.local',
            port=5672,
            credentials=credentials,
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="tasks", exchange_type="direct", durable=True)

    message = {"task": task_name, "params": params or {}}

    channel.basic_publish(
        exchange="tasks",
        routing_key=task_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print(f"Sent task: {message}")
    connection.close()

