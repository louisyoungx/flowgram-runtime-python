"""
Test for branch workflow schema.
"""
import unittest
import asyncio
from typing import Dict, Any

from ....interface import IEngine, IContainer, WorkflowStatus
from ....domain.container import WorkflowRuntimeContainer
from ..utils.snapshot import snapshots_to_vo_data
from . import TestSchemas


class BranchSchemaTest(unittest.TestCase):
    """Test for branch workflow schema."""

    def setUp(self):
        """Set up the test environment."""
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    async def test_execute_workflow_with_branch_1(self):
        """Test executing a workflow with branch 1."""
        # Create an event loop for this test
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            task = self.engine.invoke({
                "schema": TestSchemas.branch_schema,
                "inputs": {
                    "model_id": 1,
                    "prompt": "Tell me a joke",
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
        
        # Check the result contains expected output for branch 1
        self.assertIn("m1_res", result)
        self.assertIsInstance(result["m1_res"], str)
        self.assertIn("AI_MODEL_1", result["m1_res"])
        self.assertIn("Tell me a joke", result["m1_res"])
        
        # Get snapshots from the context
        snapshots = snapshots_to_vo_data(context.snapshot_center.export_all())
        
        # Check that we have snapshots for all expected nodes
        node_ids = [snapshot["nodeID"] for snapshot in snapshots]
        self.assertIn("start_0", node_ids)
        self.assertIn("condition_0", node_ids)
        self.assertIn("llm_1", node_ids)
        self.assertIn("end_0", node_ids)
        
        # Find the condition_0 snapshot and check its branch
        condition_snapshot = next((s for s in snapshots if s["nodeID"] == "condition_0"), None)
        self.assertIsNotNone(condition_snapshot)
        self.assertIn("branch", condition_snapshot)
        self.assertEqual(condition_snapshot["branch"], "if_1")
        
        # Find the llm_1 snapshot and check its inputs and outputs
        llm_snapshot = next((s for s in snapshots if s["nodeID"] == "llm_1"), None)
        self.assertIsNotNone(llm_snapshot)
        self.assertIn("inputs", llm_snapshot)
        self.assertIn("outputs", llm_snapshot)
        
        # Check key LLM inputs
        llm_inputs = llm_snapshot["inputs"]
        self.assertEqual(llm_inputs.get("modelName"), "AI_MODEL_1")
        self.assertEqual(llm_inputs.get("temperature"), 0.5)
        self.assertEqual(llm_inputs.get("prompt"), "Tell me a joke")
        
        # Check LLM output contains the expected result
        llm_outputs = llm_snapshot["outputs"]
        self.assertIn("result", llm_outputs)
        self.assertIn("AI_MODEL_1", llm_outputs["result"])
        self.assertIn("Tell me a joke", llm_outputs["result"])
        
        # Check workflow status in report
        report = context.reporter.export()
        self.assertEqual(report.workflow_status.status, WorkflowStatus.Success)
        
        # Check node statuses in report
        self.assertEqual(report.reports["start_0"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["condition_0"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["llm_1"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["end_0"].status, WorkflowStatus.Success)

    async def test_execute_workflow_with_branch_2(self):
        """Test executing a workflow with branch 2."""
        # Create an event loop for this test
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            task = self.engine.invoke({
                "schema": TestSchemas.branch_schema,
                "inputs": {
                    "model_id": 2,
                    "prompt": "Tell me a story",
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
        
        # Check the result contains expected output for branch 2
        self.assertIn("m2_res", result)
        self.assertIsInstance(result["m2_res"], str)
        self.assertIn("AI_MODEL_2", result["m2_res"])
        self.assertIn("Tell me a story", result["m2_res"])
        
        # Get snapshots from the context
        snapshots = snapshots_to_vo_data(context.snapshot_center.export_all())
        
        # Check that we have snapshots for all expected nodes
        node_ids = [snapshot["nodeID"] for snapshot in snapshots]
        self.assertIn("start_0", node_ids)
        self.assertIn("condition_0", node_ids)
        self.assertIn("llm_2", node_ids)
        self.assertIn("end_0", node_ids)
        
        # Find the condition_0 snapshot and check its branch
        condition_snapshot = next((s for s in snapshots if s["nodeID"] == "condition_0"), None)
        self.assertIsNotNone(condition_snapshot)
        self.assertIn("branch", condition_snapshot)
        self.assertEqual(condition_snapshot["branch"], "if_2")
        
        # Find the llm_2 snapshot and check its inputs and outputs
        llm_snapshot = next((s for s in snapshots if s["nodeID"] == "llm_2"), None)
        self.assertIsNotNone(llm_snapshot)
        self.assertIn("inputs", llm_snapshot)
        self.assertIn("outputs", llm_snapshot)
        
        # Check key LLM inputs
        llm_inputs = llm_snapshot["inputs"]
        self.assertEqual(llm_inputs.get("modelName"), "AI_MODEL_2")
        self.assertEqual(llm_inputs.get("temperature"), 0.6)
        self.assertEqual(llm_inputs.get("prompt"), "Tell me a story")
        
        # Check LLM output contains the expected result
        llm_outputs = llm_snapshot["outputs"]
        self.assertIn("result", llm_outputs)
        self.assertIn("AI_MODEL_2", llm_outputs["result"])
        self.assertIn("Tell me a story", llm_outputs["result"])
        
        # Check workflow status in report
        report = context.reporter.export()
        self.assertEqual(report.workflow_status.status, WorkflowStatus.Success)
        
        # Check node statuses in report
        self.assertEqual(report.reports["start_0"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["condition_0"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["llm_2"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["end_0"].status, WorkflowStatus.Success)


if __name__ == "__main__":
    unittest.main()
