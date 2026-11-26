"""
Creation Studio — ALPHA0AZ1OMEGA
Creative terminal with graphical canvas and shared fabrication graph
for humans and AI agents.

Each creation is a node in the graph.
Connections represent dependency/filiation relationships.
"""
import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from enum import Enum

GRAPH_FILE = Path(__file__).parent / "fabrication_graph.json"


class NodeType(Enum):
    """Node types in the fabrication graph."""
    PROMPT = "prompt"
    RESPONSE = "response"
    ARTIFACT = "artifact"
    DECISION = "decision"
    HUMAN_INPUT = "human_input"
    AI_GENERATION = "ai_generation"
    VERIFICATION = "verification"


class AgentType(Enum):
    """Creator agent type."""
    HUMAN = "human"
    AI = "ai"
    HYBRID = "hybrid"


@dataclass
class GraphNode:
    """Node in the fabrication graph."""
    node_id: str
    node_type: NodeType
    content: str
    creator: AgentType
    creator_id: str
    timestamp: float = field(default_factory=time.time)
    parent_ids: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    verification: dict | None = None
    epistemic_score: float | None = None
    
    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "type": self.node_type.value,
            "content": self.content,
            "creator": self.creator.value,
            "creator_id": self.creator_id,
            "timestamp": self.timestamp,
            "parents": self.parent_ids,
            "metadata": self.metadata,
            "verification": self.verification,
            "epistemic_score": self.epistemic_score
        }


@dataclass
class GraphEdge:
    """Connection between two nodes."""
    source_id: str
    target_id: str
    relation: str  # "inspires", "refines", "verifies", "produces", "depends_on"
    weight: float = 1.0
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "source": self.source_id,
            "target": self.target_id,
            "relation": self.relation,
            "weight": self.weight,
            "metadata": self.metadata
        }


class FabricationGraph:
    """
    Shared fabrication graph.
    Stores the complete history of human and AI creations.
    """
    
    def __init__(self):
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []
        self._load()
    
    def _load(self) -> None:
        """Loads the graph from file."""
        if GRAPH_FILE.exists():
            try:
                data = json.loads(GRAPH_FILE.read_text())
                for n in data.get("nodes", []):
                    node = GraphNode(
                        node_id=n["node_id"],
                        node_type=NodeType(n["type"]),
                        content=n["content"],
                        creator=AgentType(n["creator"]),
                        creator_id=n["creator_id"],
                        timestamp=n.get("timestamp", time.time()),
                        parent_ids=n.get("parents", []),
                        metadata=n.get("metadata", {}),
                        verification=n.get("verification"),
                        epistemic_score=n.get("epistemic_score")
                    )
                    self.nodes[node.node_id] = node
                for e in data.get("edges", []):
                    self.edges.append(GraphEdge(
                        source_id=e["source"],
                        target_id=e["target"],
                        relation=e["relation"],
                        weight=e.get("weight", 1.0),
                        metadata=e.get("metadata", {})
                    ))
            except (json.JSONDecodeError, KeyError):
                pass
    
    def _save(self) -> None:
        """Persists the graph."""
        data = {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "last_updated": time.time()
        }
        GRAPH_FILE.write_text(json.dumps(data, indent=2))
    
    def add_node(
        self,
        content: str,
        node_type: NodeType,
        creator: AgentType,
        creator_id: str,
        parent_ids: list[str] | None = None,
        metadata: dict | None = None
    ) -> GraphNode:
        """Adds a node to the graph."""
        node_id = str(uuid.uuid4())[:12]
        node = GraphNode(
            node_id=node_id,
            node_type=node_type,
            content=content,
            creator=creator,
            creator_id=creator_id,
            parent_ids=parent_ids or [],
            metadata=metadata or {}
        )
        self.nodes[node_id] = node
        
        # Create edges to parents
        for pid in (parent_ids or []):
            if pid in self.nodes:
                self.edges.append(GraphEdge(
                    source_id=pid,
                    target_id=node_id,
                    relation="produces"
                ))
        
        self._save()
        return node
    
    def add_edge(self, source_id: str, target_id: str, relation: str) -> GraphEdge:
        """Adds a connection between nodes."""
        edge = GraphEdge(source_id=source_id, target_id=target_id, relation=relation)
        self.edges.append(edge)
        self._save()
        return edge
    
    def get_subgraph(self, node_id: str, depth: int = 2) -> dict:
        """Returns the subgraph around a node."""
        visited = set()
        to_visit = [(node_id, 0)]
        
        while to_visit:
            nid, d = to_visit.pop(0)
            if nid in visited or d > depth:
                continue
            visited.add(nid)
            
            # Find neighbors
            for edge in self.edges:
                if edge.source_id == nid and edge.target_id not in visited:
                    to_visit.append((edge.target_id, d + 1))
                if edge.target_id == nid and edge.source_id not in visited:
                    to_visit.append((edge.source_id, d + 1))
        
        sub_nodes = {nid: self.nodes[nid].to_dict() for nid in visited if nid in self.nodes}
        sub_edges = [e.to_dict() for e in self.edges 
                     if e.source_id in visited and e.target_id in visited]
        
        return {"nodes": sub_nodes, "edges": sub_edges}
    
    def summary(self) -> dict:
        """Graph summary."""
        human_nodes = sum(1 for n in self.nodes.values() if n.creator == AgentType.HUMAN)
        ai_nodes = sum(1 for n in self.nodes.values() if n.creator == AgentType.AI)
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "human_contributions": human_nodes,
            "ai_contributions": ai_nodes,
            "node_types": {t.value: sum(1 for n in self.nodes.values() if n.node_type == t) 
                          for t in NodeType},
            "graph_file": str(GRAPH_FILE)
        }


class CreationStudio:
    """
    Creative terminal: high-level interface for fabrication.
    Each interaction creates nodes in the shared graph.
    """
    
    def __init__(self, operator_id: str = "alpha0az1omega"):
        self.graph = FabricationGraph()
        self.operator_id = operator_id
    
    def create(
        self,
        content: str,
        node_type: NodeType = NodeType.ARTIFACT,
        is_human: bool = True,
        parent_ids: list[str] | None = None,
        metadata: dict | None = None
    ) -> dict:
        """Creates a new artifact in the graph."""
        creator = AgentType.HUMAN if is_human else AgentType.AI
        
        node = self.graph.add_node(
            content=content,
            node_type=node_type,
            creator=creator,
            creator_id=self.operator_id,
            parent_ids=parent_ids,
            metadata=metadata
        )
        
        return {
            "status": "created",
            "node": node.to_dict(),
            "graph_summary": self.graph.summary()
        }
    
    def record_response(
        self,
        prompt: str,
        response: str,
        verification: dict | None = None,
        epistemic: dict | None = None
    ) -> dict:
        """
        Records a complete interaction (prompt + response) in the graph.
        Creates 2 nodes: human prompt and AI response.
        """
        # Prompt node (human)
        prompt_node = self.graph.add_node(
            content=prompt,
            node_type=NodeType.PROMPT,
            creator=AgentType.HUMAN,
            creator_id=self.operator_id
        )
        
        # Response node (AI)
        response_node = self.graph.add_node(
            content=response,
            node_type=NodeType.RESPONSE,
            creator=AgentType.AI,
            creator_id="qwen2.5:7b",
            parent_ids=[prompt_node.node_id],
            metadata={
                "verification": verification,
                "epistemic_score": epistemic.get("index_C") if epistemic else None
            }
        )
        
        # Verification edge if available
        if verification:
            self.graph.add_node(
                content=json.dumps(verification),
                node_type=NodeType.VERIFICATION,
                creator=AgentType.AI,
                creator_id="Z3",
                parent_ids=[response_node.node_id]
            )
        
        return {
            "status": "recorded",
            "prompt_node": prompt_node.node_id,
            "response_node": response_node.node_id,
            "graph_summary": self.graph.summary()
        }
    
    def explore(self, node_id: str | None = None, depth: int = 2) -> dict:
        """Explores the graph or a subgraph."""
        if node_id:
            return self.graph.get_subgraph(node_id, depth)
        return self.graph.summary()
