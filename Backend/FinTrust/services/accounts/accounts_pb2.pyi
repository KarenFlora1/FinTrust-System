from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Account(_message.Message):
    __slots__ = ("id", "user_id", "balance")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: str
    balance: float
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[str] = ..., balance: _Optional[float] = ...) -> None: ...

class UserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class AccountsResponse(_message.Message):
    __slots__ = ("accounts",)
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[Account]
    def __init__(self, accounts: _Optional[_Iterable[_Union[Account, _Mapping]]] = ...) -> None: ...

class UpdateBalanceRequest(_message.Message):
    __slots__ = ("account_id", "amount")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    amount: float
    def __init__(self, account_id: _Optional[int] = ..., amount: _Optional[float] = ...) -> None: ...

class UpdateBalanceResponse(_message.Message):
    __slots__ = ("success", "new_balance", "message", "user_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    NEW_BALANCE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    new_balance: float
    message: str
    user_id: str
    def __init__(self, success: bool = ..., new_balance: _Optional[float] = ..., message: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...
