from producer_interface import mqProducerInterface
import pika
import os


class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str):
        # Save parameters to class variables
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        # Call setupRMQConnection
        self.setupRMQConnection()
    
    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service 
        # Setting up paramaters to rabbit 
        self.con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=self.con_params)

        # Establish Channel @ RMQ
        self.channel = self.connection.channel()
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name)
        

    def publishOrder(self, message: str) -> None:  
        # Exchange is where it routes 
        # Routing key is where it should route to 
        # Message is what we're sending 
        # Basic Publish to Exchange
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )
        
        # Close Channel
        self.channel.close()
        # Close Connection
        self.connection.close()

        
        

