"""
VisiHealth AI - Input Validators
"""

from pathlib import Path


def validate_image_file(file):
    """
    Validate uploaded image file
    
    Args:
        file: Flask FileStorage object
        
    Returns:
        (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'dcm'}
    file_ext = Path(file.filename).suffix.lower().lstrip('.')
    
    if file_ext not in allowed_extensions:
        return False, f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
    
    return True, None


def validate_question(question):
    """
    Validate question text
    
    Args:
        question: Question string
        
    Returns:
        (is_valid, error_message)
    """
    if not question or not isinstance(question, str):
        return False, "Question must be a non-empty string"
    
    question = question.strip()
    
    if len(question) < 3:
        return False, "Question is too short (minimum 3 characters)"
    
    if len(question) > 500:
        return False, "Question is too long (maximum 500 characters)"
    
    return True, None


def sanitize_filename(filename):
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Remove path components
    filename = Path(filename).name
    
    # Remove potentially dangerous characters
    safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")
    filename = ''.join(c if c in safe_chars else '_' for c in filename)
    
    return filename
