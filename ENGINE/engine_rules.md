# The Engine: AI Proposal Protocol (v0.1)

## 1. Core Principle: Strict Asymmetry
An AI Agent (the Engine) is permitted to read, analyze, generate, and propose code. 
An AI Agent is FORBIDDEN from committing, merging, deploying, or judging its own output. 
The Human (holding the PGP Key) is the sole entity capable of cryptographic commitment.

## 2. The Workflow (The Loop)
1. **Propose**: The AI writes a patch or generates code in a temporary branch.
2. **Evaluate**: The CORE (Rust/WASM) checks the cryptographic integrity.
3. **Test**: The VALUE (Solidity/Anvil) runs deterministic tests on the economic logic.
4. **Review**: The AI must output a "Critique Manifest" explaining what it changed and why.
5. **Commit**: ONLY the Human can execute `git commit -S`.

## 3. The AI Constraints
- AI must NEVER have access to the Private PGP Key.
- AI must NEVER execute `git push` or `git commit`.
- If the CORE or VALUE tests fail, the AI's proposal is discarded automatically.

## 4. Verification of AI Actions
Every AI proposal must include a hash of its context and prompt. 
This ensures that if an AI hallucinates, we can trace exactly which version of the model and which prompt caused the error.
