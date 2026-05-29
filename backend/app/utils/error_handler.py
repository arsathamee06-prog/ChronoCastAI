"""
Error handling utilities
"""
from flask import jsonify

def handle_error(message, status_code=500, data=None):
    """
    Standardized error response handler
    
    Args:
        message: Error message
        status_code: HTTP status code
        data: Additional error data
    
    Returns:
        Flask response tuple
    """
    response = {
        'success': False,
        'error': message,
        'status_code': status_code
    }
    
    if data:
        response['data'] = data
    
    return jsonify(response), status_code

def success_response(data=None, message="Success", status_code=200):
    """
    Standardized success response handler
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
    
    Returns:
        Flask response tuple
    """
    response = {
        'success': True,
        'message': message,
        'status_code': status_code
    }
    
    if data:
        response['data'] = data
    
    return jsonify(response), status_code
