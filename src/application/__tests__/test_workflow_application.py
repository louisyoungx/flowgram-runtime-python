"""
Test module for the WorkflowApplication class.
"""
import unittest
from unittest.mock import MagicMock, patch

from ...application.workflow_application import WorkflowApplication


class TestWorkflowApplication(unittest.TestCase):
    """Test case for the WorkflowApplication class."""

    def test_singleton_pattern(self):
        """Test that the WorkflowApplication class implements the singleton pattern correctly."""
        # 获取第一个实例
        instance1 = WorkflowApplication.instance()
        # 获取第二个实例
        instance2 = WorkflowApplication.instance()
        # 确保两个实例是同一个对象
        self.assertIs(instance1, instance2)

    @patch('src.domain.container.WorkflowRuntimeContainer')
    def test_run_method(self, mock_container):
        """Test the run method of the WorkflowApplication class."""
        # 创建模拟对象
        mock_engine = MagicMock()
        mock_task = MagicMock()
        mock_task.id = "test-task-id"
        mock_engine.invoke.return_value = mock_task
        mock_container.instance.get.return_value = mock_engine

        # 创建应用实例
        app = WorkflowApplication()
        app.container = mock_container.instance

        # 调用run方法
        params = {"inputs": {"key": "value"}}
        task_id = app.run(params)

        # 验证结果
        self.assertEqual(task_id, "test-task-id")
        mock_engine.invoke.assert_called_once_with(params)
        self.assertIn("test-task-id", app.tasks)
        self.assertEqual(app.tasks["test-task-id"], mock_task)

    def test_cancel_method(self):
        """Test the cancel method of the WorkflowApplication class."""
        # 创建应用实例
        app = WorkflowApplication()

        # 创建模拟任务
        mock_task = MagicMock()
        app.tasks["test-task-id"] = mock_task

        # 调用cancel方法
        result = app.cancel("test-task-id")

        # 验证结果
        self.assertTrue(result)
        mock_task.cancel.assert_called_once()

        # 测试取消不存在的任务
        result = app.cancel("non-existent-task-id")
        self.assertFalse(result)

    def test_report_method(self):
        """Test the report method of the WorkflowApplication class."""
        # 创建应用实例
        app = WorkflowApplication()

        # 创建模拟任务
        mock_task = MagicMock()
        mock_reporter = MagicMock()
        mock_reporter.export.return_value = {"report": "data"}
        mock_task.context.reporter = mock_reporter
        app.tasks["test-task-id"] = mock_task

        # 调用report方法
        report = app.report("test-task-id")

        # 验证结果
        self.assertEqual(report, {"report": "data"})
        mock_reporter.export.assert_called_once()

        # 测试获取不存在的任务的报告
        report = app.report("non-existent-task-id")
        self.assertIsNone(report)

    def test_result_method(self):
        """Test the result method of the WorkflowApplication class."""
        # 创建应用实例
        app = WorkflowApplication()

        # 创建模拟任务
        mock_task = MagicMock()
        mock_task.context.status_center.workflow.terminated = True
        mock_task.context.io_center.outputs = {"output": "data"}
        app.tasks["test-task-id"] = mock_task

        # 调用result方法
        result = app.result("test-task-id")

        # 验证结果
        self.assertEqual(result, {"output": "data"})

        # 测试获取未终止的任务的结果
        mock_task.context.status_center.workflow.terminated = False
        result = app.result("test-task-id")
        self.assertIsNone(result)

        # 测试获取不存在的任务的结果
        result = app.result("non-existent-task-id")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
