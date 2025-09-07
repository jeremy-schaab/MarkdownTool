# Contributing to Markdown Manager

Thank you for your interest in contributing to Markdown Manager! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Azure OpenAI account (for AI features)
- Azure Storage account (for sync features)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/MarkdownTool.git
   cd MarkdownTool
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev,test]"
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Create environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

6. **Run tests to verify setup**
   ```bash
   pytest
   ```

## 📁 Project Structure

```
MarkdownTool/
├── src/markdown_manager/    # Main application code
│   ├── __init__.py
│   ├── app.py              # Main Streamlit application
│   ├── ai_service.py       # AI summarization service
│   ├── azure_sync_service.py # Azure storage sync
│   └── cli.py              # Command-line interface
├── tests/                  # Test suite
├── docs/                   # Documentation
├── config/                 # Configuration files
├── scripts/                # Utility scripts
├── deployment/             # Deployment configurations
└── test_files/             # Sample files for testing
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/markdown_manager --cov-report=html

# Run specific test file
pytest tests/test_ai_service.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Follow the naming convention `test_*.py`
- Use descriptive test method names
- Include docstrings for complex tests
- Mock external dependencies (Azure services, file system, etc.)

Example test structure:
```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test input"
    expected_output = "expected result"
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_output
```

## 🎨 Code Style

We use several tools to maintain consistent code style:

### Formatting
- **Black**: Code formatter
- **isort**: Import sorting

```bash
# Format code
black src/ tests/
isort src/ tests/
```

### Linting
- **flake8**: Style guide enforcement
- **mypy**: Type checking

```bash
# Lint code
flake8 src/ tests/
mypy src/
```

### Pre-commit Hooks
The project uses pre-commit hooks to automatically run these tools:
```bash
pre-commit run --all-files
```

## 📝 Documentation

### Docstring Style
Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of the function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: If param1 is empty.
    """
    pass
```

### API Documentation
- Document all public functions and classes
- Include examples in docstrings where helpful
- Update README.md for user-facing changes

## 🌟 Feature Development

### Adding New Features

1. **Create an issue** describing the feature
2. **Create a feature branch** from main:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Implement the feature** with tests
4. **Update documentation** if needed
5. **Ensure all tests pass**
6. **Submit a pull request**

### Feature Guidelines

- Follow existing code patterns and architecture
- Add comprehensive tests for new functionality
- Update relevant documentation
- Consider backward compatibility
- Add configuration options when appropriate

## 🐛 Bug Reports

### Reporting Bugs

When reporting bugs, please include:

- **Environment details** (OS, Python version, package versions)
- **Steps to reproduce** the issue
- **Expected behavior**
- **Actual behavior**
- **Error messages or logs**
- **Screenshots** (if applicable)

### Bug Fix Process

1. **Create an issue** for the bug
2. **Create a bugfix branch**:
   ```bash
   git checkout -b bugfix/issue-number-description
   ```
3. **Write a failing test** that reproduces the bug
4. **Fix the bug** and make the test pass
5. **Verify the fix** doesn't break existing functionality
6. **Submit a pull request**

## 📦 Pull Request Process

### Before Submitting

- [ ] Tests pass locally (`pytest`)
- [ ] Code is formatted (`black`, `isort`)
- [ ] Code passes linting (`flake8`, `mypy`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)

### PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes.

## Screenshots
If applicable, add screenshots.

## Checklist
- [ ] Tests pass
- [ ] Code is formatted
- [ ] Documentation updated
```

### Review Process

1. **Automated checks** must pass (GitHub Actions)
2. **Code review** by maintainers
3. **Address feedback** if requested
4. **Merge** after approval

## 🔒 Security

### Reporting Security Issues

Please report security vulnerabilities privately by emailing [security@example.com]. Do not create public issues for security problems.

### Security Guidelines

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all user inputs
- Follow OWASP security guidelines

## 📋 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release after merge
5. Deploy to PyPI (automated)

## 💬 Communication

### Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code review and discussion

### Code of Conduct

Please be respectful and professional in all interactions. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## 🎯 Areas for Contribution

We welcome contributions in these areas:

### High Priority
- **Performance improvements**
- **Bug fixes**
- **Test coverage improvements**
- **Documentation enhancements**

### Medium Priority
- **New AI summarization templates**
- **Additional file format support**
- **UI/UX improvements**
- **Accessibility improvements**

### Low Priority
- **Code refactoring**
- **Development tooling**
- **Example applications**

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Azure OpenAI Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Python Testing with pytest](https://docs.pytest.org/)
- [Git Flow Workflow](https://nvie.com/posts/a-successful-git-branching-model/)

## 🙋‍♀️ Getting Help

If you need help:

1. Check existing [GitHub Issues](https://github.com/jeremy-schaab/MarkdownTool/issues)
2. Review the [documentation](README.md)
3. Create a new issue with the "question" label

Thank you for contributing to Markdown Manager! 🎉