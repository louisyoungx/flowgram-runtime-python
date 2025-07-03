"""
Test script to verify that the branch workflow works correctly.
"""
import asyncio
import sys
from src.interface import IEngine, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer
from src.domain.__tests__.schemas import TestSchemas
from src.domain.__tests__.utils.snapshot import snapshots_to_vo_data


def main():
    # Get the container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Test branch 1
    print("Testing branch 1 (model_id=1)...")
    task = engine.invoke({
        "schema": TestSchemas.branch_schema,
        "inputs": {
            "model_id": 1,
            "prompt": "Tell me a joke",
        },
    })
    
    context = task.context
    print(f"Workflow status: {context.status_center.workflow.status}")
    
    # Run the task and wait for it to complete
    result = asyncio.run(task.processing)
    print(f"Final workflow status: {context.status_center.workflow.status}")
    
    # Check the result
    if "m1_res" in result:
        print(f"Found m1_res in result: {result['m1_res']}")
    else:
        print(f"m1_res not found in result: {result}")
        return False
    
    # Get snapshots
    snapshots = snapshots_to_vo_data(context.snapshot_center.export_all())
    node_ids = [snapshot["nodeID"] for snapshot in snapshots]
    print(f"Node IDs in snapshots: {node_ids}")
    
    # Find the condition_0 snapshot and check its branch
    condition_snapshot = next((s for s in snapshots if s["nodeID"] == "condition_0"), None)
    if condition_snapshot:
        print(f"Condition snapshot branch: {condition_snapshot.get('branch')}")
    else:
        print("Condition snapshot not found")
        return False
    
    # Get report
    report = context.reporter.export()
    print(f"Report type: {type(report)}")
    print(f"Report attributes: {dir(report)}")
    
    # Check workflowStatus
    if hasattr(report, 'workflowStatus'):
        print(f"workflowStatus: {report.workflowStatus}")
        if isinstance(report.workflowStatus, dict):
            status = report.workflowStatus.get("status")
            print(f"Status from report: {status}")
            if status == WorkflowStatus.Success:
                print("Test passed!")
                return True
            else:
                print(f"Unexpected status: {status}")
                return False
        else:
            print(f"workflowStatus is not a dict: {type(report.workflowStatus)}")
            return False
    else:
        print("Report does not have workflowStatus attribute")
        print(f"Available attributes: {dir(report)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)