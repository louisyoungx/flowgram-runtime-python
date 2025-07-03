"""
Workflow runtime validation implementation.
"""
from typing import Dict, Any

from ...interface import IValidation, ValidationResult, WorkflowSchema


class WorkflowRuntimeValidation(IValidation):
    """
    Implementation of the IValidation interface for workflow schema validation.
    """
    
    def validate(self, schema: WorkflowSchema) -> ValidationResult:
        """
        Validates a workflow schema.
        
        Args:
            schema: The workflow schema to validate.
            
        Returns:
            A validation result object.
        """
        errors = []
        
        # 获取节点和边
        nodes = schema.get("nodes", [])
        edges = schema.get("edges", [])
        
        # 创建节点ID到节点的映射
        node_map = {node["id"]: node for node in nodes}
        
        # 检查边的节点是否存在
        for edge in edges:
            source_id = edge.get("source", {}).get("id")
            target_id = edge.get("target", {}).get("id")
            
            if source_id not in node_map:
                errors.append(f"Edge source node '{source_id}' does not exist")
            
            if target_id not in node_map:
                errors.append(f"Edge target node '{target_id}' does not exist")
        
        # 检查是否只有一个开始节点和一个结束节点
        start_nodes = [node for node in nodes if node.get("type") == "flowgram.start"]
        end_nodes = [node for node in nodes if node.get("type") == "flowgram.end"]
        
        if len(start_nodes) == 0:
            errors.append("No start node found in workflow")
        elif len(start_nodes) > 1:
            errors.append(f"Multiple start nodes found: {[node['id'] for node in start_nodes]}")
        
        if len(end_nodes) == 0:
            errors.append("No end node found in workflow")
        elif len(end_nodes) > 1:
            errors.append(f"Multiple end nodes found: {[node['id'] for node in end_nodes]}")
        
        # 检查开始节点和结束节点是否在根层级
        for node in start_nodes + end_nodes:
            parent_id = node.get("parentId")
            if parent_id is not None and parent_id != "":
                errors.append(f"Node '{node['id']}' of type '{node['type']}' must be at root level")
        
        # 检查成环
        # 构建图的邻接表
        graph = {}
        for node_id in node_map:
            graph[node_id] = []
        
        for edge in edges:
            source_id = edge.get("source", {}).get("id")
            target_id = edge.get("target", {}).get("id")
            if source_id in graph and target_id in graph:
                graph[source_id].append(target_id)
        
        # 使用DFS检查环
        visited = set()
        path = set()
        
        def has_cycle(node_id):
            if node_id in path:
                return True
            if node_id in visited:
                return False
            
            visited.add(node_id)
            path.add(node_id)
            
            for neighbor in graph.get(node_id, []):
                if has_cycle(neighbor):
                    return True
            
            path.remove(node_id)
            return False
        
        for node_id in graph:
            if node_id not in visited:
                if has_cycle(node_id):
                    errors.append(f"Cycle detected in workflow starting from node '{node_id}'")
                    break
        
        # 检查跨层级连线
        for edge in edges:
            source_id = edge.get("source", {}).get("id")
            target_id = edge.get("target", {}).get("id")
            
            if source_id in node_map and target_id in node_map:
                source_parent = node_map[source_id].get("parentId", "")
                target_parent = node_map[target_id].get("parentId", "")
                
                # 如果父节点不同，且都不为空，则是跨层级连线
                if source_parent != target_parent and source_parent != "" and target_parent != "":
                    errors.append(f"Cross-level connection detected between '{source_id}' and '{target_id}'")
        
        # 返回验证结果
        return {
            "valid": len(errors) == 0,
            "errors": errors if errors else None
        }
