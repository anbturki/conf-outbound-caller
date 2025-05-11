"""
Exceptions for the application
"""

from enum import Enum
from typing import Any, Dict, Optional, Union

from fastapi import HTTPException, status


class ErrorCode(Enum):
    """
    Error codes for the application
    """

    INVALID_INPUT = "INVALID_INPUT"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_EXISTS = "RESOURCE_EXISTS"
    BAD_REQUEST = "BAD_REQUEST"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class AppException(HTTPException):
    """
    Base application exception with standardized error codes.
    """

    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        message: str,
        error_details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.error_details = error_details
        super().__init__(status_code=status_code, detail=message, headers=headers)


class ValidationException(AppException):
    """
    Exception for validation errors with field-specific details.
    """

    def __init__(
        self,
        message: str = "Invalid input",
        field_errors: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        error_details = {"message": message, "details": field_errors or {}}
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ErrorCode.INVALID_INPUT,
            message=message,
            error_details=error_details,
        )


class AuthenticationException(AppException):
    """
    Exception for authentication errors.
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        error_details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.AUTHENTICATION_ERROR,
            message=message,
            error_details=error_details,
            headers=headers,
        )


class AuthorizationException(AppException):
    """
    Exception for authorization errors.
    """

    def __init__(
        self,
        message: str = "You don't have permission to perform this action",
        error_details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ErrorCode.PERMISSION_DENIED,
            message=message,
            error_details=error_details,
        )


class ResourceNotFoundException(AppException):
    """
    Exception for resource not found errors.
    """

    def __init__(
        self,
        resource_type: str,
        resource_id: Optional[Union[str, int]] = None,
        message: Optional[str] = None,
    ):
        if not message:
            message = f"{resource_type} not found"
            if resource_id:
                message = f"{resource_type} with id {resource_id} not found"

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.RESOURCE_NOT_FOUND,
            message=message,
        )


class ResourceExistsException(AppException):
    """
    Exception for resource already exists errors.
    """

    def __init__(
        self,
        resource_type: str,
        identifier: Optional[str] = None,
        identifier_value: Optional[str] = None,
        message: Optional[str] = None,
    ):
        if not message:
            message = f"{resource_type} already exists"
            if identifier and identifier_value:
                message = f"{resource_type} with {identifier} '{identifier_value}' already exists"

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCode.RESOURCE_EXISTS,
            message=message,
        )


class BadRequestException(AppException):
    """
    Exception for bad request errors.
    """

    def __init__(
        self,
        message: str = "Bad request",
        error_details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ErrorCode.BAD_REQUEST,
            message=message,
            error_details=error_details,
        )


class ServerException(AppException):
    """
    Exception for server errors.
    """

    def __init__(
        self,
        message: str = "Internal server error",
        error_details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=message,
            error_details=error_details,
        )


class RateLimitException(AppException):
    """
    Exception for rate limit errors.
    """

    def __init__(
        self,
        message: str = "Too many requests",
        error_details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            message=message,
            error_details=error_details,
        )
