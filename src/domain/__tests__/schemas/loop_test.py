"""
Test for loop workflow schema.
"""
import unittest
import asyncio
from typing import Dict, Any, List

from ....interface import IEngine, IContainer, WorkflowStatus
from ....domain.container import WorkflowRuntimeContainer
from ..utils.snapshot import snapshots_to_vo_data
from . import TestSchemas


class LoopSchemaTest(unittest.TestCase):
    """Test for loop workflow schema."""

    def setUp(self):
        """Set up the test environment."""
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    async def test_execute_workflow_with_input(self):
        """Test executing a workflow with input."""
        # Create an event loop for this test
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            task = self.engine.invoke({
                "schema": TestSchemas.loop_schema,
                "inputs": {
                    "prompt": "How are you?",
                    "system_prompt": "You are a helpful AI assistant.",
                    "tasks": [
                        "TASK - A",
                        "TASK - B",
                        "TASK - C",
                        "TASK - D",
                        "TASK - E",
                        "TASK - F",
                        "TASK - G",
                        "TASK - H",
                    ],
                },
            })
            
            context = task.context
            self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Processing)
            
            # Run the task and wait for it to complete
            result = await task.processing
        finally:
            # Clean up the event loop
            loop.close()
        
        # Check if the workflow completed successfully
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Success)
        
        # Get snapshots from the context
        snapshots = snapshots_to_vo_data(context.snapshot_center.export_all())
        
        # Verify we have the expected nodes in the snapshots
        node_ids = [snapshot["nodeID"] for snapshot in snapshots]
        self.assertIn("start_0", node_ids)
        self.assertIn("loop_0", node_ids)
        self.assertIn("llm_0", node_ids)
        self.assertIn("end_0", node_ids)
        
        # Find the start node snapshot and verify its outputs
        start_snapshots = [s for s in snapshots if s["nodeID"] == "start_0"]
        self.assertEqual(len(start_snapshots), 1)
        start_snapshot = start_snapshots[0]
        self.assertEqual(start_snapshot["outputs"]["prompt"], "How are you?")
        self.assertEqual(start_snapshot["outputs"]["system_prompt"], "You are a helpful AI assistant.")
        self.assertEqual(len(start_snapshot["outputs"]["tasks"]), 8)
        
        # Find the loop node snapshot and verify its data
        loop_snapshots = [s for s in snapshots if s["nodeID"] == "loop_0"]
        self.assertEqual(len(loop_snapshots), 1)
        loop_snapshot = loop_snapshots[0]
        self.assertEqual(loop_snapshot["data"]["batchFor"]["type"], "ref")
        self.assertEqual(loop_snapshot["data"]["batchFor"]["content"], ["start_0", "tasks"])
        
        # Find all LLM node snapshots and verify their inputs and outputs
        llm_snapshots = [s for s in snapshots if s["nodeID"] == "llm_0"]
        self.assertEqual(len(llm_snapshots), 8)  # One for each task
        
        # Verify each LLM snapshot
        for i, llm_snapshot in enumerate(llm_snapshots):
            task_name = f"TASK - {chr(65 + i)}"  # A, B, C, ...
            self.assertEqual(llm_snapshot["inputs"]["modelName"], "AI_MODEL_1")
            self.assertEqual(llm_snapshot["inputs"]["temperature"], 0.6)
            self.assertEqual(llm_snapshot["inputs"]["systemPrompt"], "You are a helpful AI assistant.")
            self.assertEqual(llm_snapshot["inputs"]["prompt"], task_name)
            self.assertIn(task_name, llm_snapshot["outputs"]["result"])
            self.assertIn("AI_MODEL_1", llm_snapshot["outputs"]["result"])
        
        # Find the end node snapshot
        end_snapshots = [s for s in snapshots if s["nodeID"] == "end_0"]
        self.assertEqual(len(end_snapshots), 1)
        
        # Verify the report
        report = context.reporter.export()
        self.assertEqual(report.workflow_status.status, WorkflowStatus.Success)
        
        # Check node statuses in report
        self.assertEqual(report.reports["start_0"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["loop_0"].status, WorkflowStatus.Success)
        
        # Verify LLM node reports exist and are successful
        for i in range(8):
            task_name = f"TASK - {chr(65 + i)}"  # A, B, C, ...
            llm_reports = [r for node_id, r in report.reports.items() 
                          if node_id == "llm_0" and 
                          any(s.inputs.get("prompt") == task_name for s in r.snapshots)]
            self.assertTrue(len(llm_reports) > 0, f"No report found for LLM with task {task_name}")
            for llm_report in llm_reports:
                self.assertEqual(llm_report.status, WorkflowStatus.Success)
        
        self.assertEqual(report.reports["end_0"].status, WorkflowStatus.Success)


if __name__ == "__main__":
    unittest.main()
