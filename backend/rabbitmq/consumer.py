import json
import pika
import sys

sys.path.insert(0, '/app')

from rabbitmq.vault_helper import vault_helper
import requests

def get_vault_data():
    vault_credentials = vault_helper.get_rabbitmq_credentials()
    return vault_credentials

def handle_quote(params):
    count = params.get('count', '2')
    resp = requests.get(f"https://api.breakingbadquotes.xyz/v1/quotes/{count}")
    with open(f'/app/data/bb_{count}.json', 'w') as f:
        json.dump(resp.json(), f, indent=2)
    print(f"Quote saved")

def handle_cat_fact(params):
    count = params.get('count', '3')
    resp = requests.get(f"https://meowfacts.herokuapp.com/?count={count}")
    with open(f'/app/data/cat_fact_{count}.json', 'w') as f:
        json.dump(resp.json(), f, indent=2)
    print("Cat fact saved")

def callback(ch, method, properties, body):
    msg = json.loads(body)
    task = msg['task']
    params = msg.get('params', {})

    if task == 'quote':
        handle_quote(params)
    elif task == 'cat_fact':
        handle_cat_fact(params)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main(queue_name):
    secrets = get_vault_data()
    credentials = pika.PlainCredentials(
        **secrets
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rmq-rabbitmq.foodgram.svc.cluster.local',
            port="5672",
            credentials=credentials,
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange='tasks', exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='tasks', queue=queue_name, routing_key=queue_name)

    print(f"Listening for '{queue_name}'...")
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else 'quote'
    main(q)
