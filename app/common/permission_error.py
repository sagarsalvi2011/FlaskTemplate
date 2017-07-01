"""
Permission
"""


class PermissionError(Exception):
    """
    Error for permission denied to a feature
    """

    def __init__(self, message, status_code=403):
        """
           permission error error with specified information.
           :param message: Error message
           :param status_code: Status error code.
           :param headers: Headers for admin errors.
           """
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """
        :return:
        """
        permission_dict = dict()
        permission_dict['message'] = self.message
        permission_dict['status_code'] = self.status_code
        return permission_dict
