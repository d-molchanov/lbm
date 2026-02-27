import enum

class TestEnum(enum.Enum):
    ONE = '1'
    TWO = '2'

    def __str__(self):
        return self.value

class TestStrEnum(enum.StrEnum):
    ONE = '1'
    TWO = '2'

class MCURequests(enum.Enum):
    # CHECKSTATE = '!QP%'.encode('utf-8')
    # SETZERO = '!ZE%'.encode('utf-8')
    # STOP = '!ST%'.encode('utf-8')
    CHECKSTATE = b'!QP%'
    SETZERO = b'!ZE%'
    STOP = b'!ST%'

    def __str__(self):
        return self.value.decode('utf-8')


if __name__ == '__main__':
    print(TestEnum.ONE, TestStrEnum.TWO.value)
    print(MCURequests.STOP)