class MQException(Exception):
    pass


class MQConnectionException(MQException):
    pass


class MQConsumeException(MQException):
    pass


class MQPublishException(MQException):
    pass


class SyncQueueException(Exception):
    pass


class VersionConflictError(Exception):
    pass


class VersionLowerThenExpected(Exception):
    pass
