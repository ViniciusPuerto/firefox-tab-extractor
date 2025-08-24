"""
Custom exceptions for Firefox Tab Extractor
"""


class FirefoxTabExtractorError(Exception):
    """Base exception for Firefox Tab Extractor"""
    pass


class FirefoxProfileNotFoundError(FirefoxTabExtractorError):
    """Raised when Firefox profile cannot be found"""
    pass


class SessionDataError(FirefoxTabExtractorError):
    """Raised when session data cannot be read or parsed"""
    pass


class LZ4DecompressionError(FirefoxTabExtractorError):
    """Raised when LZ4 decompression fails"""
    pass


class NoTabsFoundError(FirefoxTabExtractorError):
    """Raised when no tabs are found in session data"""
    pass
