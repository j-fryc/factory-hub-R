import asyncio
from enum import Enum
from typing import Union, Callable, Awaitable
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.exceptions import AMQPConnectionError, AMQPChannelError
from app.config import WorkerSettings
from app.db_sync.exceptions import MQConsumeException, MQException, MQConnectionException, MQPublishException


class ExchangeType(Enum):
    DIRECT = 'direct'
    FANOUT = 'fanout'
    TOPIC = 'topic'
    HEADERS = 'headers'


class AsyncMQClient:
    def __init__(
            self,
            exchange_type: ExchangeType,
            exchange_name: str,
            routing_key: str,
            exchange_name_dlx: str,
            routing_key_dlx: str,
            host: str,
            port: int,
            user: str,
            password: str,
            delay_ms_dlx: int
    ):
        self._asyncio_event_handler = asyncio.Event()
        self._exchange_type = exchange_type
        self._exchange_name = exchange_name
        self._exchange_name_dlx = exchange_name_dlx
        self._routing_key_dlx = routing_key_dlx
        self._routing_key = routing_key
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._delay_ms_dlx = delay_ms_dlx
        self._connection = None
        self._channel = None
        self._exchange = None
        self._queue = None
        self._exchange_dlx = None
        self._queue_dlx = None

    async def publish_data(self, msg: Union[bytes, str], dead_letter_queue: bool = False):
        if self._channel is None or self._channel.is_closed:
            raise MQConnectionException(
                "Not connected to RabbitMQ. Use 'async with AsyncMQClient(...) as client:'"
            )
        if not isinstance(msg, (bytes, str)):
            raise TypeError("Message must be bytes or str.")
        if isinstance(msg, str):
            msg = msg.encode('utf-8')

        try:
            message = aio_pika.Message(
                body=msg,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            if dead_letter_queue:
                await self._exchange_dlx.publish(
                    message=message,
                    routing_key=self._routing_key_dlx,
                    mandatory=True
                )
            else:
                await self._exchange.publish(
                    message=message,
                    routing_key=self._routing_key,
                    mandatory=True
                )
        except AMQPChannelError as e:
            raise MQPublishException(f"Channel error during publish: {e}") from e
        except AMQPConnectionError as e:
            raise MQConnectionException(f"Connection error during publish: {e}") from e
        except Exception as e:
            raise MQException(f"Unexpected error during publish: {e}") from e

    async def consume_data(self, callback_fn: Callable[[AbstractIncomingMessage], Awaitable[None]]) -> None:
        if self._channel is None or self._channel.is_closed:
            raise MQConnectionException(
                "Not connected to RabbitMQ. Use 'async with AsyncMQClient(...) as client:'"
            )
        try:
            await self._queue.consume(callback_fn)
            await self._asyncio_event_handler.wait()
        except AMQPChannelError as e:
            raise MQConsumeException(f"Channel error during consuming data: {e}") from e
        except AMQPConnectionError as e:
            raise MQConnectionException(f"Connection error during consuming data: {e}") from e
        except Exception as e:
            raise MQException(f"Unexpected error during consuming data: {e}") from e

    async def connect(self) -> None:
        try:
            self._connection = await aio_pika.connect_robust(
                host=self._host,
                port=self._port,
                login=self._user,
                password=self._password
            )
            self._channel = await self._connection.channel()
            await self._channel.set_qos(prefetch_count=1)

            self._exchange = await self._channel.declare_exchange(
                name=self._exchange_name,
                type=self._exchange_type.value,
                durable=True
            )

            self._exchange_dlx = await self._channel.declare_exchange(
                name=self._exchange_name_dlx,
                type=self._exchange_type.value,
                durable=True
            )

            self._queue = await self._channel.declare_queue(
                name="",
                exclusive=True
            )

            self._queue_dlx = await self._channel.declare_queue(
                name="",
                exclusive=True,
                arguments={
                    'x-message-ttl': self._delay_ms_dlx,
                    'x-dead-letter-exchange': self._exchange_name,
                    'x-dead-letter-routing-key': self._routing_key
                }
            )

            await self._queue.bind(
                exchange=self._exchange,
                routing_key=self._routing_key
            )

            await self._queue_dlx.bind(
                exchange=self._exchange_dlx,
                routing_key=self._routing_key_dlx
            )
        except AMQPConnectionError as e:
            raise MQConnectionException(f"Failed to connect to RabbitMQ: {e}") from e
        except Exception as e:
            raise MQConnectionException(f"Unexpected error connecting to RabbitMQ: {e}") from e

    async def disconnect(self):
        try:
            if self._connection and not self._connection.is_closed:
                await self._connection.close()
        except Exception:
            pass
        finally:
            self._connection = None
            self._channel = None
            self._exchange = None
            self._queue = None
            self._asyncio_event_handler.set()


def get_async_mq_client(
        settings: WorkerSettings,
        worker_type: str
) -> AsyncMQClient:
    return AsyncMQClient(
        exchange_type=ExchangeType.DIRECT,
        exchange_name=settings.rabbit_mq_exchange_name,
        routing_key=worker_type,
        exchange_name_dlx=settings.rabbit_mq_exchange_name_dlx,
        routing_key_dlx=f"{worker_type}_dlx",
        host=settings.rabbit_mq_host,
        port=settings.rabbit_mq_port,
        user=settings.rabbit_mq_user,
        password=settings.rabbit_mq_password,
        delay_ms_dlx=settings.delay_ms_dlx,
    )



if __name__ == "__main__":
    async def process_message(message: AbstractIncomingMessage):
        body = message.body.decode()
        print(f"Received: {body}")
        await asyncio.sleep(0.1)  # Symulacja async pracy
        await message.ack()


    async def main():
        consumer = AsyncMQClient(
            exchange_type=ExchangeType.DIRECT,
            exchange_name="s_test",
            routing_key="test22",
            host="localhost",
            port=5672,
            user='user',
            password='password'
        )

        try:
            async with consumer:
                print("Started consuming...")
                await consumer.consume_data(process_message)
                await asyncio.Future()
        except MQException as e:
            print(f"Error: {e}")

    async def example_without_context_manager():
        consumer = AsyncMQClient(
            exchange_type=ExchangeType.DIRECT,
            exchange_name="s_test",
            routing_key="test22",
            host="localhost",
            port=5672,
            user='user',
            password='password'
        )

        try:
            await consumer.connect()
            print("Connected to RabbitMQ")

            await consumer.publish_data("Test message")
            print("Message published")

            print("Started consuming...")
            await consumer.consume_data(process_message)

            await asyncio.Future()

        except MQException as e:
            print(f"Error: {e}")
        finally:
            await consumer.disconnect()
            print("Disconnected from RabbitMQ")


    asyncio.run(example_without_context_manager())