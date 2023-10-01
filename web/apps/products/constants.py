from enum import Enum

class CategoryEnum(Enum):
    UNDEFINED   = 1
    PANTS       = 2
    TOPS        = 3
    SHOES       = 4

class ProductStatusEnum(Enum):
    ACTIVE      = "Y"
    DEACTIVE    = "N"

class ProductDeleteEnum(Enum):
    DELETED     = "Y"
    NOT_DELETED = "N"