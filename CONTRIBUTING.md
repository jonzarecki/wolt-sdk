# Contributing to Wolt Restaurant Availability API

Thank you for your interest in contributing! This guide will help you get started.

## 🚀 Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Install** dependencies: `pip install -r requirements.txt`
4. **Run tests** to ensure everything works: `pytest tests/ -v`

## 🧪 Testing Guidelines

**CRITICAL**: This project tests against **real Wolt APIs**

- All tests use live API endpoints in Israel
- Tests must pass with actual restaurant data
- Never mock API responses - we test real functionality
- Be respectful of API rate limits (use delays between tests)

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_wolt_api.py::TestWoltAPI::test_get_nearby_restaurants_tel_aviv -v

# Run with slower rate limiting for stability
python -c "
from wolt_api import WoltAPI
api = WoltAPI(rate_limit_delay=2.0)
# Your test code here
"
```

## 📝 Code Style

- **Simplicity over complexity**: Clear, readable code
- **Type hints**: Use them where helpful
- **Docstrings**: Document public methods
- **Error handling**: Specific exceptions for different cases
- **Rate limiting**: Always respect API limits

## 🌍 Geographic Coverage

This API covers all of Israel. When adding new functionality:

- Ensure it works across different Israeli cities
- Test with both Hebrew and English location names
- Consider different restaurant types and cuisines

## 🐛 Bug Reports

When reporting bugs:

1. **Include the restaurant slug** that's causing issues
2. **Specify the location** (city, coordinates)
3. **Provide the full error message**
4. **Include the time** when you encountered the issue

## ✨ Feature Requests

Before submitting a feature request:

1. Check if it's already implemented
2. Consider if it fits the project's scope (Israeli restaurant availability)
3. Think about API rate limit implications

## 🔧 Development Setup

```bash
# Clone the repo
git clone https://github.com/your-username/wolt-access.git
cd wolt-access

# Install in development mode
pip install -e .

# Run a quick test
python -c "
from wolt_api import WoltAPI
api = WoltAPI()
print('API loaded successfully!')
"
```

## 📊 Testing New Features

When adding features:

1. **Write tests first** (TDD approach)
2. **Test with real restaurant slugs** in different cities
3. **Verify rate limiting** doesn't cause issues
4. **Check error handling** for various scenarios

## 🎯 Pull Request Guidelines

1. **Fork and create a feature branch**
2. **Write or update tests** for your changes
3. **Ensure all tests pass** with real API calls
4. **Update documentation** if needed
5. **Keep PRs focused** - one feature per PR

### PR Checklist

- [ ] Tests pass with real Wolt APIs
- [ ] Code follows project style guidelines
- [ ] Documentation updated if needed
- [ ] Rate limiting respected
- [ ] No hardcoded API keys or sensitive data

## 🤝 Community Guidelines

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Share knowledge** about Wolt's API behavior
- **Report issues** constructively

## ⚠️ Important Notes

- **Never commit API keys** or personal data
- **Respect Wolt's terms of service**
- **Don't abuse rate limits** - be a good API citizen
- **Test responsibly** - don't spam the APIs

## 📞 Getting Help

- **Open an issue** for bugs or questions
- **Check existing issues** before creating new ones
- **Be specific** about your use case and environment

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributor section
- CHANGELOG.md for significant contributions
- GitHub contributors page

Thank you for making this project better! 🎉