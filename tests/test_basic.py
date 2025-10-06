# ================================
# tests/test_basic.py
# ================================
"""Basic tests for PyLoggerX functionality."""
import pytest
import tempfile
import os
import json
import time
from pyloggerx import PyLoggerX, log

class TestBasicFunctionality:
    """Test basic logging functionality."""
    
    def test_default_logger_creation(self):
        """Test that default logger can be created without errors."""
        logger = PyLoggerX(console=False)  # Disable console for testing
        assert logger.name == "PyLoggerX"
        assert logger.logger.level == 20  # INFO level
    
    def test_basic_logging_methods(self):
        """Test all basic logging methods work without errors."""
        logger = PyLoggerX(console=False)
        
        # These should not raise any exceptions
        logger.debug("Debug message")
        logger.info("Info message") 
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_global_logger_instance(self):
        """Test that global log instance works."""
        # Should not raise exceptions
        log.info("Global logger test")
        log.error("Global error test")
    
    def test_log_level_setting(self):
        """Test log level can be changed."""
        logger = PyLoggerX(console=False, level="ERROR")
        assert logger.logger.level == 40  # ERROR level
        
        logger.set_level("DEBUG")
        assert logger.logger.level == 10  # DEBUG level
    
    def test_json_file_logging(self):
        """Test JSON file logging functionality."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name
        
        try:
            logger = PyLoggerX(console=False, json_file=json_file)
            test_message = "JSON test message"
            test_extra = {"test_key": "test_value", "number": 42}
            
            logger.info(test_message, **test_extra)
            
            # Verify JSON file was created and contains expected data
            assert os.path.exists(json_file)
            
            with open(json_file, 'r') as f:
                log_line = f.readline().strip()
                assert log_line  # File should not be empty
                
                log_data = json.loads(log_line)
                assert log_data['level'] == 'INFO'
                assert log_data['message'] == test_message
                assert log_data['test_key'] == 'test_value'
                assert log_data['number'] == 42
                
        finally:
            if os.path.exists(json_file):
                os.unlink(json_file)
    
    def test_text_file_logging(self):
        """Test text file logging functionality."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            text_file = f.name
        
        try:
            logger = PyLoggerX(console=False, text_file=text_file)
            test_message = "Text log test message"
            
            logger.info(test_message)
            
            # Verify text file was created and contains expected data
            assert os.path.exists(text_file)
            
            with open(text_file, 'r') as f:
                content = f.read()
                assert test_message in content
                assert 'INFO' in content
                
        finally:
            if os.path.exists(text_file):
                os.unlink(text_file)
    
    def test_performance_tracking(self):
        """Test performance tracking functionality."""
        logger = PyLoggerX(console=False, performance_tracking=True)
        
        with logger.timer("test_operation"):
            time.sleep(0.01)  # Sleep for 10ms
        
        stats = logger.get_performance_stats()
        
        assert stats['total_operations'] == 1
        assert stats['avg_duration'] >= 0.01  # Should be at least 10ms
        assert 'test_operation' in stats['operations']
        assert stats['operations']['test_operation'] >= 0.01
    
    def test_context_management(self):
        """Test context management functionality."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name
        
        try:
            logger = PyLoggerX(console=False, json_file=json_file)
            
            # Add context
            logger.add_context(app_version="1.0.0", environment="test")
            logger.info("Test with context")
            
            # Verify context appears in JSON log
            with open(json_file, 'r') as f:
                log_line = f.readline().strip()
                log_data = json.loads(log_line)
                
                # Context should be present
                assert 'app_version' in log_data or 'environment' in log_data
                
        finally:
            if os.path.exists(json_file):
                os.unlink(json_file)
    
    def test_exception_logging(self):
        """Test exception logging."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name
        
        try:
            logger = PyLoggerX(console=False, json_file=json_file)
            
            try:
                raise ValueError("Test exception")
            except ValueError:
                logger.exception("An error occurred")
            
            # Verify exception was logged
            with open(json_file, 'r') as f:
                log_line = f.readline().strip()
                log_data = json.loads(log_line)
                
                assert 'exception' in log_data
                assert 'ValueError' in log_data['exception']
                assert 'Test exception' in log_data['exception']
                
        finally:
            if os.path.exists(json_file):
                os.unlink(json_file)


class TestAdvancedFeatures:
    """Test advanced features."""
    
    def test_multiple_outputs(self):
        """Test logging to multiple destinations simultaneously."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            text_file = f.name
        
        try:
            logger = PyLoggerX(
                console=False,
                json_file=json_file,
                text_file=text_file
            )
            
            test_message = "Multi-output test"
            logger.info(test_message)
            
            # Verify both files exist and contain the message
            assert os.path.exists(json_file)
            assert os.path.exists(text_file)
            
            with open(json_file, 'r') as f:
                json_content = f.read()
                assert test_message in json_content
            
            with open(text_file, 'r') as f:
                text_content = f.read()
                assert test_message in text_content
                
        finally:
            for filepath in [json_file, text_file]:
                if os.path.exists(filepath):
                    os.unlink(filepath)
    
    def test_caller_information(self):
        """Test caller information tracking."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name
        
        try:
            logger = PyLoggerX(
                console=False,
                json_file=json_file,
                include_caller=True
            )
            
            logger.info("Test caller info")
            
            with open(json_file, 'r') as f:
                log_line = f.readline().strip()
                log_data = json.loads(log_line)
                
                # Should have caller information
                assert 'filename' in log_data
                assert 'function' in log_data
                assert 'line_number' in log_data
                
        finally:
            if os.path.exists(json_file):
                os.unlink(json_file)
    
    def test_performance_stats_clearing(self):
        """Test clearing performance statistics."""
        logger = PyLoggerX(console=False, performance_tracking=True)
        
        with logger.timer("operation1"):
            time.sleep(0.01)
        
        stats = logger.get_performance_stats()
        assert stats['total_operations'] == 1
        
        # Clear stats
        logger.clear_performance_stats()
        stats = logger.get_performance_stats()
        assert stats['total_operations'] == 0
    
    def test_timer_context_with_exception(self):
        """Test timer context manager with exceptions."""
        logger = PyLoggerX(console=False, performance_tracking=True)
        
        try:
            with logger.timer("failing_operation"):
                raise ValueError("Test error")
        except ValueError:
            pass  # Expected
        
        stats = logger.get_performance_stats()
        assert 'failing_operation' in stats['operations']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])