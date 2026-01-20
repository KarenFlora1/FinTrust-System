from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransferRequest(_message.Message):
    __slots__ = ("from_account_id", "to_account_id", "amount")
    FROM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TO_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    from_account_id: int
    to_account_id: int
    amount: float
    def __init__(self, from_account_id: _Optional[int] = ..., to_account_id: _Optional[int] = ..., amount: _Optional[float] = ...) -> None: ...

class TransferResponse(_message.Message):
    __slots__ = ("success", "transaction_id", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    transaction_id: str
    message: str
    def __init__(self, success: bool = ..., transaction_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class UserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class TransferItem(_message.Message):
    __slots__ = ("timestamp", "from_account_id", "to_account_id", "amount")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FROM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TO_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    from_account_id: int
    to_account_id: int
    amount: float
    def __init__(self, timestamp: _Optional[str] = ..., from_account_id: _Optional[int] = ..., to_account_id: _Optional[int] = ..., amount: _Optional[float] = ...) -> None: ...

class TransferHistoryResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[TransferItem]
    def __init__(self, items: _Optional[_Iterable[_Union[TransferItem, _Mapping]]] = ...) -> None: ...
