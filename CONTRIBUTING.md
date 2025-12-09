# Contributing to AI Code Review Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/aaahkt.git`
3. Install dependencies: `npm install`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites
- Node.js 18+ (ES Modules support required)
- npm 9+

### Running the Project
```bash
# Install dependencies
npm install

# Run the tool
npm start <file-to-analyze>

# Run tests
npm test

# Run demo
npm run demo
```

## Adding New Features

### Adding a New Analysis Rule

1. **Security Rules**: Add to `checkSecurity()` method in `index.js`
```javascript
{
  pattern: /your-pattern/g,
  message: 'Your security warning',
  severity: 'high' // critical, high, medium, low
}
```

2. **Quality Rules**: Add to `checkCodeQuality()` method
3. **Best Practice Rules**: Add to `checkBestPractices()` method

### Adding Language Support

To add support for a new programming language:

1. Add language-specific patterns to analysis methods
2. Update the file extension handling in `analyzeFile()`
3. Add test cases for the new language
4. Update documentation

Example:
```javascript
if (fileExt === '.py') {
  // Python-specific checks
  this.checkPythonPatterns(content);
}
```

## Testing

### Running Tests
```bash
npm test
```

### Writing Tests
Add test cases to `test.js`:

```javascript
test('Should detect your new pattern', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = 'your test code';
  analyzer.analyzeContent(testCode, '.js');
  assert(/* your assertion */);
});
```

### Test Coverage
- Aim for 80%+ code coverage
- Test both positive and negative cases
- Include edge cases

## Code Style

- Use ES Modules syntax (`import`/`export`)
- Follow existing naming conventions
- Add JSDoc comments for public methods
- Keep functions focused and small
- Use meaningful variable names

## Commit Messages

Follow the conventional commits format:

```
feat: Add Python language support
fix: Correct complexity calculation for nested loops
docs: Update README with installation instructions
test: Add tests for security pattern detection
refactor: Simplify report generation logic
```

## Pull Request Process

1. Update tests to cover your changes
2. Run `npm test` to ensure all tests pass
3. Update documentation if needed
4. Update ARCHITECTURE.md if adding major features
5. Create a pull request with a clear description

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Feature Requests

Have an idea? Open an issue with:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach (optional)

## Bug Reports

Found a bug? Open an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Sample code that triggers the bug
- Your environment (Node.js version, OS)

## Questions?

Feel free to open a discussion or issue for questions about:
- How to contribute
- Architecture decisions
- Implementation details
- Feature ideas

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to making code reviews smarter and more accessible!
