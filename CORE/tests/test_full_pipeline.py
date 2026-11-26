"""
Full pipeline tests for ALPHA0AZ1OMEGA.
Verifies: Z3 + PGP + Epistemic + Studio
"""
import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch


class TestPGPSigner(unittest.TestCase):
    """PGP module tests."""
    
    def test_sign_response(self):
        from CORE.pgp.signer import sign_response
        import CORE.pgp.signer as signer_module
        original_file = signer_module.NEURON_CHAIN_FILE
        signer_module.NEURON_CHAIN_FILE = Path(tempfile.mktemp(suffix=".json"))
        
        try:
            neuron = sign_response("Test response content")
            self.assertIn("content_hash", neuron)
            self.assertIn("index", neuron)
            self.assertEqual(neuron["index"], 0)
            self.assertIsNotNone(neuron["content_hash"])
        finally:
            signer_module.NEURON_CHAIN_FILE.unlink(missing_ok=True)
            signer_module.NEURON_CHAIN_FILE = original_file
    
    def test_chain_integrity(self):
        from CORE.pgp.signer import sign_response, _verify_full_chain
        import CORE.pgp.signer as signer_module
        signer_module.NEURON_CHAIN_FILE = Path(tempfile.mktemp(suffix=".json"))
        
        try:
            sign_response("First")
            sign_response("Second")
            sign_response("Third")
            self.assertTrue(_verify_full_chain())
        finally:
            signer_module.NEURON_CHAIN_FILE.unlink(missing_ok=True)


class TestEpistemicEngine(unittest.TestCase):
    """Epistemic module tests."""
    
    def test_high_confidence(self):
        from CORE.epistemic.engine import compute_epistemic_score
        result = compute_epistemic_score(
            verification={"accepted": True, "status": "CONSISTENT"},
            claims=[{"text": "test", "evidence": "test"}],
            response_text="This is a coherent test response with enough length.",
            pgp_neuron={"pgp_signature": "fake_sig", "index": 0}
        )
        self.assertGreater(result["index_C"], 0.7)
        self.assertIn(result["confidence"], ["HIGH", "MEDIUM"])
    
    def test_low_confidence(self):
        from CORE.epistemic.engine import compute_epistemic_score
        result = compute_epistemic_score(
            verification={"accepted": False, "status": "CONTRADICTION"},
            claims=[],
            response_text=""
        )
        self.assertLess(result["index_C"], 0.5)
    
    def test_failure_tree_structure(self):
        from CORE.epistemic.engine import compute_epistemic_score
        result = compute_epistemic_score(
            verification={"accepted": True, "status": "CONSISTENT"},
            claims=[{"text": "a", "evidence": "b"}],
            response_text="Valid response."
        )
        tree = result["failure_tree"]
        self.assertEqual(tree["node_id"], "ROOT")
        self.assertTrue(len(tree["children"]) >= 3)


class TestCreationStudio(unittest.TestCase):
    """Creation Studio module tests."""
    
    def test_create_node(self):
        from CORE.studio.engine import CreationStudio, NodeType
        import CORE.studio.engine as studio_module
        
        original_file = studio_module.GRAPH_FILE
        studio_module.GRAPH_FILE = Path(tempfile.mktemp(suffix=".json"))
        
        try:
            cs = CreationStudio(operator_id="test")
            result = cs.create("Test artifact", NodeType.ARTIFACT, is_human=True)
            self.assertEqual(result["status"], "created")
            self.assertIn("node", result)
        finally:
            studio_module.GRAPH_FILE.unlink(missing_ok=True)
            studio_module.GRAPH_FILE = original_file
    
    def test_record_response(self):
        from CORE.studio.engine import CreationStudio
        import CORE.studio.engine as studio_module
        
        original_file = studio_module.GRAPH_FILE
        studio_module.GRAPH_FILE = Path(tempfile.mktemp(suffix=".json"))
        
        try:
            cs = CreationStudio(operator_id="test")
            result = cs.record_response(
                prompt="What is 2+2?",
                response="4",
                verification={"status": "CONSISTENT"}
            )
            self.assertEqual(result["status"], "recorded")
            self.assertIn("prompt_node", result)
            self.assertIn("response_node", result)
        finally:
            studio_module.GRAPH_FILE.unlink(missing_ok=True)
            studio_module.GRAPH_FILE = original_file
    
    def test_graph_summary(self):
        from CORE.studio.engine import CreationStudio, NodeType
        import CORE.studio.engine as studio_module
        
        original_file = studio_module.GRAPH_FILE
        studio_module.GRAPH_FILE = Path(tempfile.mktemp(suffix=".json"))
        
        try:
            cs = CreationStudio(operator_id="test")
            cs.create("Node 1", NodeType.PROMPT, is_human=True)
            cs.create("Node 2", NodeType.RESPONSE, is_human=False)
            summary = cs.explore()
            self.assertEqual(summary["total_nodes"], 2)
            self.assertEqual(summary["human_contributions"], 1)
            self.assertEqual(summary["ai_contributions"], 1)
        finally:
            studio_module.GRAPH_FILE.unlink(missing_ok=True)
            studio_module.GRAPH_FILE = original_file


if __name__ == "__main__":
    unittest.main()
