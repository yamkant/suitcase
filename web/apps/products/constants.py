from enum import Enum

class CategoryEnum(Enum):
    UNDEFINED   = 1
    PANTS       = 2
    TOPS        = 3
    SHOES       = 4

class ProductStatusEnum(Enum):
    DELETED     = "Y"
    NOT_DELETED = "N"

class ProductUploadedStatusEnum(Enum):
    NEED_ALARM      = "A"
    COMPLETED       = "Y"
    ERROR           = "E"
    NOT_COMPLETED   = "N"