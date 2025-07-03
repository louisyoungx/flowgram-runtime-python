"""
Tests for the API functions.
"""
import json
import unittest
from unittest.mock import patch, MagicMock, AsyncMock

from ...interface.schema import TaskRunInput, TaskResultInput, TaskReportInput, TaskCancelInput
from ..task_run_api import TaskRunAPI
from ..task_result_api import TaskResultAPI
from ..task_report_api import TaskReportAPI
from ..task_cancel_api import TaskCancelAPI


class TestAPIs(unittest.IsolatedAsyncioTestCase):
    """Test case for API functions."""

    async def test_task_run_api(self):
        """Test the TaskRunAPI function."""
        # Prepare test data
        schema = {
            "nodes": [
                {
                    "id": "node1",
                    "type": "start",
                    "data": {},
                    "ports": {
                        "output": [
                            {
                                "id": "port1",
                                "type": "output",
                                "nodeId": "node1",
                                "key": "output"
                            }
                        ]
                    }
                }
            ],
            "edges": []
        }
        
        input_data: TaskRunInput = {
            "schema": json.dumps(schema),
            "inputs": {"key": "value"}
        }
        
        # Mock the WorkflowApplication.instance() method
        mock_app = MagicMock()
        mock_app.run.return_value = "task123"
        
        with patch("src.application.workflow_application.WorkflowApplication.instance", return_value=mock_app):
            # Call the API function
            result = await TaskRunAPI(input_data)
            
            # Check the result
            self.assertEqual(result, {"taskID": "task123"})
            
            # Check that the run method was called with the correct arguments
            mock_app.run.assert_called_once()
            args = mock_app.run.call_args[0][0]
            self.assertEqual(args["schema"], schema)
            self.assertEqual(args["inputs"], {"key": "value"})

    async def test_task_result_api(self):
        """Test the TaskResultAPI function."""
        # Prepare test data
        input_data: TaskResultInput = {
            "taskID": "task123"
        }
        
        # Mock the WorkflowApplication.instance() method
        mock_app = MagicMock()
        mock_app.result.return_value = {"outputs": {"key": "value"}}
        
        with patch("src.application.workflow_application.WorkflowApplication.instance", return_value=mock_app):
            # Call the API function
            result = await TaskResultAPI(input_data)
            
            # Check the result
            self.assertEqual(result, {"outputs": {"key": "value"}})
            
            # Check that the result method was called with the correct arguments
            mock_app.result.assert_called_once_with("task123")

    async def test_task_report_api(self):
        """Test the TaskReportAPI function."""
        # Prepare test data
        input_data: TaskReportInput = {
            "taskID": "task123"
        }
        
        # Mock the WorkflowApplication.instance() method
        mock_app = MagicMock()
        mock_app.report.return_value = {"report": "data"}
        
        with patch("src.application.workflow_application.WorkflowApplication.instance", return_value=mock_app):
            # Call the API function
            result = await TaskReportAPI(input_data)
            
            # Check the result
            self.assertEqual(result, {"report": "data"})
            
            # Check that the report method was called with the correct arguments
            mock_app.report.assert_called_once_with("task123")

    async def test_task_cancel_api(self):
        """Test the TaskCancelAPI function."""
        # Prepare test data
        input_data: TaskCancelInput = {
            "taskID": "task123"
        }
        
        # Mock the WorkflowApplication.instance() method
        mock_app = MagicMock()
        mock_app.cancel.return_value = True
        
        with patch("src.application.workflow_application.WorkflowApplication.instance", return_value=mock_app):
            # Call the API function
            result = await TaskCancelAPI(input_data)
            
            # Check the result
            self.assertEqual(result, {"success": True})
            
            # Check that the cancel method was called with the correct arguments
            mock_app.cancel.assert_called_once_with("task123")


if __name__ == "__main__":
    unittest.main()
