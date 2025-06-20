# Validate Integration Task

## Purpose

Verify that all changes are correctly wired throughout the BMAD ecosystem and that the updated agent set passes its own quality gate.

## Instructions

1. **Orchestrator Consistency Check**  
   - Confirm the persona entry exists in all orchestrator configs.  
   - Ensure all task links resolve to existing files.

2. **Self-Test Simulation**  
   - Execute a dry-run conversation simulating the original failure scenario.  
   - Verify the Prompt Engineer behaves as expected.

3. **Checklist Review**  
   - Run `prompt-engineer-checklist` to make sure nothing is missed.

4. **Close the Loop**  
   - Report results back to the reporting user.  
   - If issues remain, loop back to Step 1 with updated insights.

## Output Deliverable

- Validation report summarising pass/fail status and next steps. 
