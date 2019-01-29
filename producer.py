from kafka import KafkaProducer
import simplejson as json

def publish_message(producer,topic_name, key, value):
    try:
        data = { key : value }
        producer.send(topic_name, json.dumps(data).encode('utf-8'))
        producer.flush()
        print('Message published!')

    except Exception as e:
        print('Exception in publishing message')
        print(e)

def connect_kafka_producer():
    _producer = None
    try :
        _producer = KafkaProducer(bootstrap_servers= ['localhost:9092'], api_version = (0,10))
    except Exception as e :
        print('Exception while connecting kafka')
        print(e)
    return _producer 


if __name__ == "__main__":
    kafka_producer = connect_kafka_producer()
    publish_message(kafka_producer, 'hello-kafka', 'key', 'ina')
    if kafka_producer is not None:
        kafka_producer.close()
