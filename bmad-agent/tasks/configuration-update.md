# Configuration Update Task

## Purpose

Apply the smallest safe edits or create new artefacts to fix issues uncovered during the audit or extend BMAD capabilities.

## Instructions

1. **Plan the Patch**  
   - Decide whether the fix requires:  
     a. Persona file modification  
     b. Checklist tweak  
     c. Task creation/update  
     d. Orchestrator config update  
     e. New tool registration

2. **Implement Edits**  
   - Edit Markdown files following BMAD style; keep diffs minimal.  
   - Reflect new tools both in persona definition and orchestrator `tools:` sections (if present).

3. **Update Checklist Mappings**  
   - If a new checklist is introduced, add an entry to `tasks/checklist-mappings.yml`.

4. **Report Changes Made**  
   - Provide to user a short summary describing the patch as part of the chat response.

## Output Deliverables

- Patched files ready for commit.  
- Changes summary provided to user. 
