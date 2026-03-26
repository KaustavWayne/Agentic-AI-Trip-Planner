# custom exception handling
class TripPlannerException(Exception):
    pass

class APICallFailed(TripPlannerException):
    pass

class InvalidQuery(TripPlannerException):
    pass