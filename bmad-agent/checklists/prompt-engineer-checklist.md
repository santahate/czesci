# Prompt Engineer Operational Checklist

This checklist ensures that all necessary artefacts and integrations for the Prompt Engineer persona are present and valid.

## 1. SETUP VERIFICATION

- [ ] Persona file `prompt-engineer.md` exists under `bmad-agent/personas/`
- [ ] Task files (`persona-audit.md`, `configuration-update.md`, `validate-integration.md`) exist under `bmad-agent/tasks/`
- [ ] Checklist file `prompt-engineer-checklist.md` exists under `bmad-agent/checklists/`
- [ ] Checklist is registered in `tasks/checklist-mappings.yml`

## 2. ORCHESTRATOR INTEGRATION

- [ ] Persona entry added to all relevant orchestrator configuration files (`*-orchestrator*.cfg.md`)
- [ ] Task links in orchestrator configs resolve to existing files
- [ ] Checklist link added where orchestrators support `checklists:` section (e.g., web config)

## 3. TOOL REGISTRATION (IF APPLICABLE)

- [ ] New tools required by Prompt Engineer are listed in her persona definition
- [ ] Tools are also declared in orchestrator `tools:` sections when present

## 4. VALIDATION

- [ ] Dry-run simulation of the original issue passes with updated Prompt Engineer
- [ ] No linter errors for any modified files inside `bmad-agent/` 
