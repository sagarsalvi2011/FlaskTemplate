"""
This is a custom exception to pass on all database failures for better handling and messaging.
"""

class DatabaseOperationFailedError(Exception):
    """
    DatabaseOperationFailedError is a custom exception class used to handle all database failures.
    """

    def __init__(self, error, **kwargs):
        """
        Add custom arguments to an error
        ideally you should use explicit
        inputs for readability

        However in a jam this works nicely
        """
        self.__dict__.update(kwargs)
        Exception.__init__(self, error)
