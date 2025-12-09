# 🤖 AI Code Review Assistant

**AssembleHack25 Hackathon Project**

An intelligent, AI-powered code review assistant that analyzes your code for quality, security vulnerabilities, and best practices. Built for developers who want instant feedback on their code without waiting for human reviewers.

## 🌟 Features

- **Security Analysis**: Detects hardcoded credentials, XSS vulnerabilities, dangerous functions like `eval()`, and command injection risks
- **Code Quality Metrics**: Measures lines of code, function count, comment ratio, and calculates quality scores
- **Complexity Analysis**: Calculates cyclomatic complexity to identify overly complex functions
- **Best Practices**: Checks for proper error handling, excessive console logs, magic numbers, and documentation
- **AI-Powered Recommendations**: Provides intelligent suggestions based on code patterns and metrics
- **Beautiful CLI Output**: Color-coded results with icons for easy readability

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ntphiep/aaahkt.git
cd aaahkt

# Install dependencies
npm install
```

### Usage

Analyze any code file:

```bash
npm start <path-to-your-file>
```

Or use the direct command:

```bash
node index.js <path-to-your-file>
```

### Examples

Try it with the included sample files:

```bash
# Analyze code with issues
npm start examples/bad-code.js

# Analyze clean code
npm start examples/good-code.js
```

## 📊 What It Analyzes

### Security Issues (Critical/High Priority)
- Hardcoded passwords and API keys
- XSS vulnerabilities (innerHTML usage)
- Dangerous functions (eval, exec)
- Command injection risks

### Code Quality
- Function length (flags functions >50 lines)
- Line length (warns on lines >120 characters)
- Technical debt markers (TODO, FIXME)
- Comment ratio and documentation

### Best Practices
- Error handling patterns
- Console.log overuse
- Magic numbers
- Code complexity

### Metrics
- Lines of code
- Number of functions
- Comment count
- Cyclomatic complexity
- Overall quality score (0-100)

## 🎯 Sample Output

```
🔍 Analyzing: examples/bad-code.js

📊 Code Metrics:
  Lines of Code: 58
  Functions: 2
  Comments: 4
  Complexity Score: 23
  Quality Score: 35/100

⚠️  Issues Found:
  🔴 [CRITICAL] Hardcoded password detected
  🔴 [CRITICAL] Hardcoded API key detected
  🟠 [HIGH] Use of eval() detected - potential security risk
  🟡 [MEDIUM] Direct innerHTML assignment - risk of XSS attacks
  🔵 [LOW] Line 52 exceeds 120 characters - consider breaking it up

💡 Suggestions:
  1. Found TODO/FIXME comments - consider addressing technical debt
  2. Multiple console.log statements found - consider using a proper logging library
  3. Magic numbers detected - consider using named constants

🤖 AI-Powered Recommendations:
  1. Consider applying the Single Responsibility Principle to reduce complexity
  2. Security issues detected - prioritize fixing these before deployment
```

## 🛠️ Technical Details

### Built With
- **Node.js**: Runtime environment
- **Commander.js**: CLI framework
- **Chalk**: Terminal styling

### Architecture
- **CodeAnalyzer Class**: Core analysis engine
- **Pattern Matching**: Uses regex for security and quality checks
- **Metrics Calculation**: Real-time computation of complexity and quality scores
- **Modular Design**: Easy to extend with new analysis rules

## 🎓 How It Works

1. **File Parsing**: Reads and tokenizes the input file
2. **Pattern Detection**: Uses regex patterns to identify issues
3. **Metrics Calculation**: Counts functions, lines, complexity
4. **Scoring Algorithm**: Calculates quality score based on findings
5. **Report Generation**: Produces color-coded, organized output

## 🔮 Future Enhancements

- Support for more languages (Python, Java, Go, etc.)
- Integration with actual AI/LLM APIs for deeper analysis
- Fix suggestions with code snippets
- CI/CD integration
- Web UI dashboard
- VS Code extension
- Git hooks integration

## 📝 License

MIT License - feel free to use this in your projects!

## 🏆 AssembleHack25

This project was built for the AssembleHack25 hackathon, demonstrating practical AI application in software development tools. It combines static analysis with AI-inspired recommendations to help developers write better, more secure code.

## 👨‍💻 Author

Built with ❤️ for AssembleHack25

---

**Try it now and get instant feedback on your code!**