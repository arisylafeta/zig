# Poetry PATH Configuration

**Ticket ID:** 20250622195316
**Created:** June 22, 2025, 19:53:16
**Status:** Resolved
**Priority:** Medium
**Assignee:** Dev Team
**Tags:** #devops #python #environment

## Issue

Poetry was installed on the system but not accessible from the command line without specifying the full path (`/Users/lobby/.local/bin/poetry`). This created friction in the development workflow, especially when running LangGraph development server and other Poetry-managed commands.

## Impact

- Developers had to use the full path to Poetry (`/Users/lobby/.local/bin/poetry`) for every command
- Commands like `poetry run langgraph dev` would fail unless the full path was specified
- Increased cognitive load and reduced developer productivity
- Potential for inconsistent environment usage across the team

## Root Cause

Poetry was installed correctly in `~/.local/bin/`, but this directory was not included in the system's PATH environment variable. As a result, the shell couldn't find the `poetry` command when executed without the full path.

## Resolution

Added Poetry's installation directory to the PATH environment variable by:

1. Appending the following line to the `.zshrc` file:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. Applying the changes to the current session:
   ```bash
   source ~/.zshrc
   ```

3. Verifying the fix by running:
   ```bash
   poetry --version
   ```
   Which successfully returned: `Poetry (version 2.1.3)`

## Verification

After implementing the fix:
- `poetry --version` works from any directory
- `poetry run langgraph dev --port 8123` successfully starts the LangGraph development server
- No need to specify the full path to Poetry anymore

## Lessons Learned

1. When installing development tools like Poetry, always verify they're added to PATH
2. Document environment setup steps for new team members to avoid similar issues
3. Consider adding this PATH configuration to the project's onboarding documentation

## Future Recommendations

1. Create a comprehensive environment setup script for new developers
2. Add environment verification steps to the project's README
3. Consider using direnv or a similar tool to automatically set up the environment when entering the project directory
