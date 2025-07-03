"""
Test for basic workflow schema.
"""
import unittest
import asyncio
from typing import Dict, Any

from ....interface import IEngine, IContainer, WorkflowStatus
from ....domain.container import WorkflowRuntimeContainer
from ..utils.snapshot import snapshots_to_vo_data
from . import TestSchemas


class BasicSchemaTest(unittest.TestCase):
    """Test for basic workflow schema."""

    async def test_execute_workflow_with_input(self):
        """Test executing a workflow with input."""
        container: IContainer = WorkflowRuntimeContainer.instance()
        engine = container.get(IEngine)
        
        # Create an event loop for this test
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            task = engine.invoke({
                "schema": TestSchemas.basic_schema,
                "inputs": {
                    "model_name": "ai-model",
                    "llm_settings": {
                        "temperature": 0.5,
                    },
                    "prompt": "How are you?",
                },
            })
            
            context = task.context
            self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Processing)
            
            # Run the task and wait for it to complete
            result = await task.processing
        finally:
            # Clean up the event loop
            loop.close()
        
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Success)
        
        # Check result contains expected keys
        self.assertIn("llm_res", result)
        self.assertIn("llm_prompt", result)
        
        # Check llm_prompt value
        self.assertEqual(result["llm_prompt"], "How are you?")
        
        # Check llm_res contains expected information
        self.assertIsInstance(result["llm_res"], str)
        self.assertIn("ai-model", result["llm_res"])
        self.assertIn("How are you?", result["llm_res"])
        
        # Get actual snapshots from the context
        snapshots = snapshots_to_vo_data(context.snapshot_center.export_all())
        
        # Verify we have the expected nodes in the snapshots
        node_ids = [snapshot["nodeID"] for snapshot in snapshots]
        self.assertIn("start_0", node_ids)
        self.assertIn("llm_0", node_ids)
        self.assertIn("end_0", node_ids)
        
        # Find the start node snapshot and verify its outputs
        start_snapshots = [s for s in snapshots if s["nodeID"] == "start_0"]
        self.assertEqual(len(start_snapshots), 1)
        start_snapshot = start_snapshots[0]
        self.assertEqual(start_snapshot["outputs"]["model_name"], "ai-model")
        self.assertEqual(start_snapshot["outputs"]["prompt"], "How are you?")
        self.assertEqual(start_snapshot["outputs"]["llm_settings"]["temperature"], 0.5)
        
        # Find the llm node snapshot and verify its inputs and outputs
        llm_snapshots = [s for s in snapshots if s["nodeID"] == "llm_0"]
        self.assertEqual(len(llm_snapshots), 1)
        llm_snapshot = llm_snapshots[0]
        self.assertEqual(llm_snapshot["inputs"]["modelName"], "ai-model")
        self.assertEqual(llm_snapshot["inputs"]["temperature"]["temperature"], 0.5)
        self.assertEqual(llm_snapshot["inputs"]["prompt"], "How are you?")
        self.assertEqual(llm_snapshot["inputs"]["systemPrompt"], "You are a helpful AI assistant.")
        self.assertIn("ai-model", llm_snapshot["outputs"]["result"])
        self.assertIn("How are you?", llm_snapshot["outputs"]["result"])
        
        # Find the end node snapshot and verify its inputs
        end_snapshots = [s for s in snapshots if s["nodeID"] == "end_0"]
        self.assertEqual(len(end_snapshots), 1)
        end_snapshot = end_snapshots[0]
        self.assertEqual(end_snapshot["inputs"]["llm_prompt"], "How are you?")
        self.assertIn("ai-model", end_snapshot["inputs"]["llm_res"])
        
        report = context.reporter.export()
        self.assertEqual(report.workflowStatus["status"], WorkflowStatus.Success)
        self.assertEqual(report.reports["start_0"]["status"], WorkflowStatus.Success)
        self.assertEqual(report.reports["llm_0"]["status"], WorkflowStatus.Success)
        self.assertEqual(report.reports["end_0"]["status"], WorkflowStatus.Success)


if __name__ == "__main__":
    unittest.main()
