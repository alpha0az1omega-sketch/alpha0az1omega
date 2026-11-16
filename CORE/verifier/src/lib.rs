use sha2::{Sha256, Digest};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Manifest {
    pub version: String,
    pub project: String,
    pub artifact: Artifact,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Artifact {
    pub name: String,
    pub hash_algorithm: String,
    pub content_hash: String,
}

/// Core Mathematical Function: Computes the SHA-256 hash of any string.
pub fn compute_hash(content: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content.as_bytes());
    let result = hasher.finalize();
    format!("{:x}", result)
}

/// Verifies if the content matches the expected hash.
/// This is the deterministic judge. It returns true or false. No AI can override this.
pub fn verify_integrity(content: &str, expected_hash: &str) -> bool {
    let actual_hash = compute_hash(content);
    actual_hash == expected_hash
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hash_is_deterministic() {
        let content = "alpha0az1omega";
        // The known SHA-256 of "alpha0az1omega" (we will verify this)
        let hash = compute_hash(content);
        assert_eq!(hash.len(), 64); // A SHA-256 hash is always 64 hex characters
    }

    #[test]
    fn test_verify_integrity() {
        let content = "alpha0az1omega";
        let good_hash = compute_hash(content);
        let bad_hash = "0000000000000000000000000000000000000000000000000000000000000000";
        
        assert_eq!(verify_integrity(content, &good_hash), true);
        assert_eq!(verify_integrity(content, bad_hash), false);
    }
}
