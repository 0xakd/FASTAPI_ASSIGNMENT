from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

class BooklyException(Exception):
    """This is the base class for all bookly errors"""
    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""
    pass


class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""
    pass


class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""
    pass


class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""
    pass


class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sign up."""
    pass


class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during log in."""
    pass


class InsufficientPermission(BooklyException):
    """User does not have the neccessary permissions to perform an action."""
    pass


class BookNotFound(BooklyException):
    """Book Not found"""
    pass


class TagNotFound(BooklyException):
    """Tag Not found"""
    pass


class TagAlreadyExists(BooklyException):
    """Tag already exists"""
    pass


class UserNotFound(BooklyException):
    """User Not found"""

    pass


class AccountNotVerified(BooklyException):
    """Account not yet verified"""
    pass


class AlreadyFollowing(BooklyException):
    """User already follows this author"""
    pass

class NotFollowing(BooklyException):
    """User is not following this author"""
    pass

class CannotFollowYourself(BooklyException):
    """User tried to follow themselves"""
    pass

class LikeNotFound(BooklyException):
    pass

class PostNotFound(BooklyException):
    pass

class CommentNotFound(BooklyException):
    pass

class MaxImagesExceeded(BooklyException):
    pass



def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler


def register_all_errors(app: FastAPI):

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists(request, exc):
        return JSONResponse(
            content={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
        
    @app.exception_handler(UserNotFound)
    async def user_not_found(request, exc):
        return JSONResponse(
            content={
                "message": "User not found",
                "error_code": "user_not_found",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
        
    @app.exception_handler(BookNotFound)
    async def book_not_found(request, exc):
        return JSONResponse(
            content={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    @app.exception_handler(TagNotFound)
    async def tag_not_found(request, exc):
        return JSONResponse(
            content={
                "message": "Tag not found",
                "error_code": "tag_not_found",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    @app.exception_handler(TagAlreadyExists)
    async def tag_exists(request, exc):
        return JSONResponse(
            content={
                "message": "Tag already exists",
                "error_code": "tag_exists"
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials(request, exc):
        return JSONResponse(
            content={
                "message": "Invalid email or password",
                "error_code": "invalid_email_or_password",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # 🔐 AUTH ERRORS
    @app.exception_handler(InvalidToken)
    async def invalid_token(request, exc):
        return JSONResponse(
            content={
                "message": "Token is invalid or expired",
                "resolution": "Please get a new token",
                "error_code": "invalid_token",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    @app.exception_handler(RevokedToken)
    async def revoked_token(request, exc):
        return JSONResponse(
            content={
                "message": "Token has been revoked",
                "resolution": "Please get a new token",
                "error_code": "token_revoked",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    @app.exception_handler(AccessTokenRequired)
    async def access_token_required(request, exc):
        return JSONResponse(
            content={
                "message": "Access token required",
                "error_code": "access_token_required",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    @app.exception_handler(RefreshTokenRequired)
    async def refresh_token_required(request, exc):
        return JSONResponse(
            content={
                "message": "Refresh token required",
                "error_code": "refresh_token_required",
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
    @app.exception_handler(InsufficientPermission)
    async def insufficient_permission(request, exc):
        return JSONResponse(
            content={
                "message": "Insufficient permissions",
                "error_code": "insufficient_permissions",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    @app.exception_handler(AccountNotVerified)
    async def account_not_verified(request, exc):
        return JSONResponse(
            content={
                "message": "Account not verified",
                "resolution": "Please check your email",
                "error_code": "account_not_verified",
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
    # 🔥 AUTHORS FEATURE ERRORS
    @app.exception_handler(AlreadyFollowing)
    async def already_following(request, exc):
        return JSONResponse(
            content={
                "message": "You are already following this author",
                "error_code": "already_following",
            },
            status_code=status.HTTP_409_CONFLICT,
        )
    @app.exception_handler(NotFollowing)
    async def not_following(request, exc):
        return JSONResponse(
            content={
                "message": "You are not following this author",
                "error_code": "not_following",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    @app.exception_handler(CannotFollowYourself)
    async def cannot_follow_self(request, exc):
        return JSONResponse(
            content={
                "message": "You cannot follow yourself",
                "error_code": "self_follow",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # 💥 DATABASE ERROR
    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        print(str(exc))  # optional logging
        return JSONResponse(
            content={
                "message": "Database error occurred",
                "error_code": "db_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    # 💀 GENERIC 500 ERROR
    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    
    # 📌 POSTS FEATURE ERRORS

    @app.exception_handler(PostNotFound)
    async def post_not_found(request, exc):
        return JSONResponse(
            content={
                "message": "Post not found",
                "error_code": "post_not_found",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )


    @app.exception_handler(CommentNotFound)
    async def comment_not_found(request, exc):
        return JSONResponse(
            content={
                "message": "Comment not found",
                "error_code": "comment_not_found",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )


    @app.exception_handler(MaxImagesExceeded)
    async def max_images_exceeded(request, exc):
        return JSONResponse(
            content={
                "message": "You can upload a maximum of 4 images per post",
                "error_code": "max_images_exceeded",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        
    @app.exception_handler(LikeNotFound)
    async def like_not_found(request, exc):
        return JSONResponse(
            content={
                "message": "Like not found",
                "error_code": "like_not_found",
            },
            status_code=status.HTTP_404_NOT_FOUND
        )