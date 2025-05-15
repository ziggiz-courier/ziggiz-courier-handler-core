# Commit Message Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

We support the following commit types:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit
- **decoder**: Changes to decoder functionality
- **encoder**: Changes to encoder functionality
- **model**: Changes to data models

## Examples

```
feat(decoder): add space-after-priority support for RFC3164 decoder
```

```
fix(decoder): handle null hostnames in syslog messages
```

```
docs: update README.md with example usage
```

```
test(decoder): add test cases for RFC3164 decoder
```

## Usage with Pre-commit

This repository uses pre-commit to enforce conventional commit messages. When you commit changes, the message will be validated against the conventional commit format.

To install pre-commit:

```bash
pip install pre-commit
pre-commit install --hook-type commit-msg
```

## Writing Good Commit Messages

1. Use the imperative mood in the subject line ("Add feature" not "Added feature")
2. Do not end the subject line with a period
3. Keep the subject line to 72 characters or less
4. Separate subject from body with a blank line
5. Use the body to explain what and why vs. how
6. Reference issues and pull requests in the footer
