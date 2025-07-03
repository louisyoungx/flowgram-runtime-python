"""
Test for basic LLM workflow schema.
"""
import unittest
import asyncio
import os
from typing import Dict, Any

from ....interface import IEngine, IContainer, IExecutor, WorkflowStatus
from ....domain.container import WorkflowRuntimeContainer
from ....nodes.llm import LLMExecutor
from ..utils.snapshot import snapshots_to_vo_data
from . import TestSchemas


class BasicLLMSchemaTest(unittest.TestCase):
    """Test for basic LLM workflow schema."""

    def setUp(self):
        """Set up the test environment."""
        self.container = WorkflowRuntimeContainer.instance()
        executor = self.container.get(IExecutor)
        executor.register(LLMExecutor())

    async def test_execute_workflow(self):
        """Test executing a workflow with a real LLM."""
        # Skip if not enabled
        if os.environ.get("ENABLE_MODEL_TEST") != "true":
            self.skipTest("Model test not enabled")
        
        # Check for required environment variables
        model_name = os.environ.get("MODEL_NAME")
        api_key = os.environ.get("API_KEY")
        api_host = os.environ.get("API_HOST")
        
        if not model_name or not api_key or not api_host:
            self.skipTest("Missing required environment variables")
        
        # Create an event loop for this test
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run the test
            engine = self.container.get(IEngine)
            task = engine.invoke({
                "schema": TestSchemas.basic_llm_schema,
                "inputs": {
                    "model_name": model_name,
                    "api_key": api_key,
                    "api_host": api_host,
                    "prompt": 'Just give me the answer of "1+1=?", just one number, no other words',
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
        
        # Check result structure and content
        self.assertIn("answer", result)
        self.assertIsInstance(result["answer"], str)
        self.assertEqual(result["answer"].strip(), "2")
        
        # Get snapshots from the context
        snapshots = snapshots_to_vo_data(context.snapshot_center.export_all())
        
        # Check that we have snapshots for all expected nodes
        node_ids = [snapshot["nodeID"] for snapshot in snapshots]
        self.assertIn("start_0", node_ids)
        self.assertIn("llm_0", node_ids)
        self.assertIn("end_0", node_ids)
        
        # Find the start node snapshot and verify its outputs
        start_snapshot = next((s for s in snapshots if s["nodeID"] == "start_0"), None)
        self.assertIsNotNone(start_snapshot)
        self.assertEqual(start_snapshot["outputs"]["model_name"], model_name)
        self.assertEqual(start_snapshot["outputs"]["api_key"], api_key)
        self.assertEqual(start_snapshot["outputs"]["api_host"], api_host)
        self.assertEqual(start_snapshot["outputs"]["prompt"], 
                         'Just give me the answer of "1+1=?", just one number, no other words')
        
        # Find the llm node snapshot and verify its inputs and outputs
        llm_snapshot = next((s for s in snapshots if s["nodeID"] == "llm_0"), None)
        self.assertIsNotNone(llm_snapshot)
        self.assertEqual(llm_snapshot["inputs"]["modelName"], model_name)
        self.assertEqual(llm_snapshot["inputs"]["apiKey"], api_key)
        self.assertEqual(llm_snapshot["inputs"]["apiHost"], api_host)
        self.assertEqual(llm_snapshot["inputs"]["temperature"], 0)
        self.assertEqual(llm_snapshot["inputs"]["prompt"], 
                         'Just give me the answer of "1+1=?", just one number, no other words')
        self.assertEqual(llm_snapshot["inputs"]["systemPrompt"], "You are a helpful AI assistant.")
        self.assertIn("result", llm_snapshot["outputs"])
        self.assertEqual(llm_snapshot["outputs"]["result"].strip(), "2")
        
        # Find the end node snapshot and verify its inputs and outputs
        end_snapshot = next((s for s in snapshots if s["nodeID"] == "end_0"), None)
        self.assertIsNotNone(end_snapshot)
        self.assertIn("answer", end_snapshot["inputs"])
        self.assertEqual(end_snapshot["inputs"]["answer"].strip(), "2")
        self.assertIn("answer", end_snapshot["outputs"])
        self.assertEqual(end_snapshot["outputs"]["answer"].strip(), "2")
        
        # Check report status
        report = context.reporter.export()
        self.assertEqual(report.workflow_status.status, WorkflowStatus.Success)
        self.assertEqual(report.reports["start_0"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["llm_0"].status, WorkflowStatus.Success)
        self.assertEqual(report.reports["end_0"].status, WorkflowStatus.Success)


if __name__ == "__main__":
    unittest.main()
