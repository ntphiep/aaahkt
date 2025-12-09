#!/usr/bin/env node

/**
 * AI-Powered Code Review Assistant
 * AssembleHack25 Hackathon Project
 * 
 * This tool analyzes code files and provides intelligent feedback on:
 * - Code quality and best practices
 * - Security vulnerabilities
 * - Performance improvements
 * - Maintainability suggestions
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { program } from 'commander';
import chalk from 'chalk';

class CodeAnalyzer {
  constructor() {
    this.issues = [];
    this.suggestions = [];
    this.metrics = {
      lines: 0,
      functions: 0,
      complexity: 0,
      comments: 0
    };
  }

  /**
   * Analyze a code file and generate insights
   */
  analyzeFile(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const ext = path.extname(filePath);
      
      console.log(chalk.blue.bold(`\n🔍 Analyzing: ${filePath}\n`));
      
      this.analyzeContent(content, ext);
      this.generateReport();
      
      return {
        issues: this.issues,
        suggestions: this.suggestions,
        metrics: this.metrics
      };
    } catch (error) {
      console.error(chalk.red(`Error reading file: ${error.message}`));
      return null;
    }
  }

  /**
   * Perform various code analysis checks
   */
  analyzeContent(content, fileExt) {
    const lines = content.split('\n');
    this.metrics.lines = lines.length;
    
    // Count functions and methods
    const functionPattern = /function\s+\w+|const\s+\w+\s*=\s*\(.*\)\s*=>|def\s+\w+|func\s+\w+|public\s+\w+\s+\w+\(/g;
    const functions = content.match(functionPattern);
    this.metrics.functions = functions ? functions.length : 0;
    
    // Count comments
    const commentPattern = /\/\/.*|\/\*[\s\S]*?\*\/|#.*|"""[\s\S]*?"""/g;
    const comments = content.match(commentPattern);
    this.metrics.comments = comments ? comments.length : 0;
    
    // Security checks
    this.checkSecurity(content);
    
    // Code quality checks
    this.checkCodeQuality(content, lines);
    
    // Best practices
    this.checkBestPractices(content, fileExt);
    
    // Calculate complexity score
    this.calculateComplexity(content);
  }

  /**
   * Check for common security issues
   */
  checkSecurity(content) {
    const securityPatterns = [
      { pattern: /eval\s*\(/g, message: 'Use of eval() detected - potential security risk', severity: 'high' },
      { pattern: /innerHTML\s*=/g, message: 'Direct innerHTML assignment - risk of XSS attacks', severity: 'medium' },
      { pattern: /password\s*=\s*['"][^'"]+['"]/gi, message: 'Hardcoded password detected', severity: 'critical' },
      { pattern: /api[_-]?key\s*=\s*['"][^'"]+['"]/gi, message: 'Hardcoded API key detected', severity: 'critical' },
      { pattern: /exec\s*\(/g, message: 'Use of exec() - potential command injection risk', severity: 'high' }
    ];

    securityPatterns.forEach(({ pattern, message, severity }) => {
      if (pattern.test(content)) {
        this.issues.push({ type: 'security', severity, message });
      }
    });
  }

  /**
   * Check code quality metrics
   */
  checkCodeQuality(content, lines) {
    // Check for very long functions
    let inFunction = false;
    let functionLength = 0;
    
    lines.forEach(line => {
      if (/function\s+\w+|const\s+\w+\s*=.*=>|def\s+\w+/.test(line)) {
        inFunction = true;
        functionLength = 0;
      }
      
      if (inFunction) {
        functionLength++;
        if (functionLength > 50) {
          this.issues.push({
            type: 'quality',
            severity: 'medium',
            message: 'Function exceeds 50 lines - consider refactoring for better maintainability'
          });
          inFunction = false;
        }
      }
      
      if (line.trim() === '}' || line.trim() === 'end') {
        inFunction = false;
      }
    });

    // Check for very long lines
    lines.forEach((line, idx) => {
      if (line.length > 120) {
        this.issues.push({
          type: 'quality',
          severity: 'low',
          message: `Line ${idx + 1} exceeds 120 characters - consider breaking it up`
        });
      }
    });

    // Check for TODO/FIXME comments
    const todoPattern = /TODO|FIXME|HACK|XXX/gi;
    if (todoPattern.test(content)) {
      this.suggestions.push('Found TODO/FIXME comments - consider addressing technical debt');
    }
  }

  /**
   * Check for best practices
   */
  checkBestPractices(content, fileExt) {
    // Check for proper error handling
    if ((fileExt === '.js' || fileExt === '.ts') && content.includes('try')) {
      if (!content.includes('catch')) {
        this.issues.push({
          type: 'best-practice',
          severity: 'medium',
          message: 'Try block without catch - ensure proper error handling'
        });
      }
    }

    // Check for console.log in production code
    const consolePattern = /console\.log\(/g;
    const consoleLogs = content.match(consolePattern);
    if (consoleLogs && consoleLogs.length > 5) {
      this.suggestions.push('Multiple console.log statements found - consider using a proper logging library');
    }

    // Check for magic numbers (excluding common values like 0, 1, 2, 10, 100, 1000)
    const lines = content.split('\n');
    let hasMagicNumbers = false;
    lines.forEach(line => {
      // Match numbers that are not 0, 1, 2, 10, 100, or 1000
      const matches = line.match(/\b\d{2,}\b/g);
      if (matches) {
        const filtered = matches.filter(n => !['10', '100', '1000'].includes(n));
        if (filtered.length > 0) {
          hasMagicNumbers = true;
        }
      }
    });
    if (hasMagicNumbers) {
      this.suggestions.push('Magic numbers detected - consider using named constants');
    }

    // Check comment ratio
    const commentRatio = this.metrics.comments / this.metrics.lines;
    if (commentRatio < 0.1 && this.metrics.lines > 50) {
      this.suggestions.push('Low comment ratio - consider adding more documentation');
    }
  }

  /**
   * Calculate code complexity
   */
  calculateComplexity(content) {
    // Simple cyclomatic complexity estimation
    const complexityPatterns = [
      /if\s*\(/g,
      /else\s+if/g,
      /while\s*\(/g,
      /for\s*\(/g,
      /case\s+/g,
      /catch\s*\(/g,
      /&&/g,
      /\|\|/g
    ];

    let complexity = 1; // Base complexity
    
    complexityPatterns.forEach(pattern => {
      const matches = content.match(pattern);
      if (matches) {
        complexity += matches.length;
      }
    });

    this.metrics.complexity = complexity;

    if (complexity > 20) {
      this.issues.push({
        type: 'complexity',
        severity: 'high',
        message: `High cyclomatic complexity (${complexity}) - consider refactoring`
      });
    } else if (complexity > 10) {
      this.suggestions.push(`Moderate complexity (${complexity}) - keep an eye on this as the code evolves`);
    }
  }

  /**
   * Generate and display the analysis report
   */
  generateReport() {
    console.log(chalk.cyan.bold('📊 Code Metrics:'));
    console.log(`  Lines of Code: ${this.metrics.lines}`);
    console.log(`  Functions: ${this.metrics.functions}`);
    console.log(`  Comments: ${this.metrics.comments}`);
    console.log(`  Complexity Score: ${this.metrics.complexity}`);
    
    // Calculate quality score
    let qualityScore = 100;
    qualityScore -= this.issues.filter(i => i.severity === 'critical').length * 20;
    qualityScore -= this.issues.filter(i => i.severity === 'high').length * 10;
    qualityScore -= this.issues.filter(i => i.severity === 'medium').length * 5;
    qualityScore -= this.issues.filter(i => i.severity === 'low').length * 2;
    qualityScore = Math.max(0, qualityScore);

    const scoreColor = qualityScore >= 80 ? chalk.green : qualityScore >= 60 ? chalk.yellow : chalk.red;
    console.log(`  ${scoreColor.bold(`Quality Score: ${qualityScore}/100`)}`);

    // Display issues
    if (this.issues.length > 0) {
      console.log(chalk.red.bold('\n⚠️  Issues Found:'));
      this.issues.forEach((issue, idx) => {
        const icon = issue.severity === 'critical' ? '🔴' : 
                     issue.severity === 'high' ? '🟠' : 
                     issue.severity === 'medium' ? '🟡' : '🔵';
        console.log(`  ${icon} [${issue.severity.toUpperCase()}] ${issue.message}`);
      });
    } else {
      console.log(chalk.green.bold('\n✅ No critical issues found!'));
    }

    // Display suggestions
    if (this.suggestions.length > 0) {
      console.log(chalk.yellow.bold('\n💡 Suggestions:'));
      this.suggestions.forEach((suggestion, idx) => {
        console.log(`  ${idx + 1}. ${suggestion}`);
      });
    }

    // AI-powered recommendations
    console.log(chalk.magenta.bold('\n🤖 AI-Powered Recommendations:'));
    this.generateAIRecommendations();
  }

  /**
   * Generate AI-like recommendations based on analysis
   */
  generateAIRecommendations() {
    const recommendations = [];

    if (this.metrics.complexity > 15) {
      recommendations.push('Consider applying the Single Responsibility Principle to reduce complexity');
    }

    if (this.metrics.functions > 10 && this.metrics.comments < 5) {
      recommendations.push('Add JSDoc/docstring comments to document function purposes and parameters');
    }

    if (this.issues.some(i => i.type === 'security')) {
      recommendations.push('Security issues detected - prioritize fixing these before deployment');
    }

    const functionDensity = this.metrics.functions / (this.metrics.lines || 1);
    if (functionDensity < 0.05 && this.metrics.lines > 100) {
      recommendations.push('Consider breaking down large code blocks into smaller, reusable functions');
    }

    if (recommendations.length === 0) {
      recommendations.push('Code looks good! Continue following current practices');
      recommendations.push('Consider adding unit tests if not already present');
    }

    recommendations.forEach((rec, idx) => {
      console.log(`  ${idx + 1}. ${rec}`);
    });
  }
}

/**
 * Main CLI program
 */
program
  .name('ai-code-review')
  .description('AI-Powered Code Review Assistant for AssembleHack25')
  .version('1.0.0')
  .argument('<file>', 'Path to the code file to analyze')
  .action((file) => {
    console.log(chalk.bold.cyan('\n🚀 AI Code Review Assistant'));
    console.log(chalk.gray('AssembleHack25 Hackathon Project\n'));
    
    if (!fs.existsSync(file)) {
      console.error(chalk.red(`Error: File '${file}' not found`));
      process.exit(1);
    }

    const analyzer = new CodeAnalyzer();
    const results = analyzer.analyzeFile(file);
    
    if (results) {
      console.log(chalk.green.bold('\n✨ Analysis complete!\n'));
    }
  });

// If run directly (not imported)
const currentFile = fileURLToPath(import.meta.url);
if (process.argv[1] === currentFile) {
  program.parse();
}

export default CodeAnalyzer;
