from enum import Enum


class VacationTypeEnum(str, Enum):
    PAID_LEAVE = "paid leave"
    UNPAID_LEAVE = "unpaid leave"

ALLOWED_VACATION_TYPE = [vacation_type.value for vacation_type in VacationTypeEnum]

