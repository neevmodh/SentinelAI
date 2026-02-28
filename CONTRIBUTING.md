# Contributing to SentinelAI

First off, thank you for considering contributing to SentinelAI! It's people like you that make SentinelAI such a great tool for cybersecurity education.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other tools**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message
6. Update documentation as needed

## Development Setup

1. Fork and clone the repository
```bash
git clone https://github.com/yourusername/sentinelai.git
cd sentinelai
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Train the model
```bash
cd model
python train.py
```

5. Run the application
```bash
python app.py
```

## Style Guidelines

### Python Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

### JavaScript Code Style
- Use ES6+ features
- Use meaningful variable names
- Add comments for complex logic
- Follow consistent indentation (2 spaces)

### Git Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

Example:
```
Add cognitive manipulation detection

- Implement 8 psychological trigger categories
- Add radar chart visualization
- Update documentation

Fixes #123
```

## Project Structure

```
sentinelai/
├── app.py              # Flask application
├── model/              # ML models and training
├── templates/          # HTML templates
├── static/             # CSS and JavaScript
└── data/               # Training datasets
```

## Testing

Before submitting a pull request:

1. Test the ML model training
2. Test the Flask application
3. Test all UI features
4. Test on different browsers
5. Check for console errors

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions
- Update comments for modified code
- Add examples for new features

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.

## Recognition

Contributors will be recognized in the README.md file.

Thank you for contributing to SentinelAI! 🛡️
