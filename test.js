#!/usr/bin/env node

/**
 * Simple test suite for AI Code Review Assistant
 */

import CodeAnalyzer from './index.js';
import fs from 'fs';
import path from 'path';

console.log('🧪 Running tests for AI Code Review Assistant...\n');

let passed = 0;
let failed = 0;

function test(description, fn) {
  try {
    fn();
    console.log(`✅ ${description}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${description}`);
    console.error(`   Error: ${error.message}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed');
  }
}

// Test 1: CodeAnalyzer instantiation
test('CodeAnalyzer should instantiate correctly', () => {
  const analyzer = new CodeAnalyzer();
  assert(analyzer !== null, 'Analyzer should not be null');
  assert(analyzer.issues !== undefined, 'Should have issues array');
  assert(analyzer.suggestions !== undefined, 'Should have suggestions array');
  assert(analyzer.metrics !== undefined, 'Should have metrics object');
});

// Test 2: Security detection - hardcoded password
test('Should detect hardcoded passwords', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = 'const password = "admin123";';
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.issues.some(i => i.message.includes('password')), 'Should detect hardcoded password');
});

// Test 3: Security detection - eval usage
test('Should detect eval() usage', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = 'eval(userInput);';
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.issues.some(i => i.message.includes('eval')), 'Should detect eval usage');
});

// Test 4: Security detection - innerHTML
test('Should detect innerHTML XSS risk', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = 'element.innerHTML = userData;';
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.issues.some(i => i.message.includes('innerHTML')), 'Should detect innerHTML usage');
});

// Test 5: Metrics calculation
test('Should calculate basic metrics', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = `function test() {
    return true;
  }
  // A comment
  function another() {
    return false;
  }`;
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.metrics.lines > 0, 'Should count lines');
  assert(analyzer.metrics.functions === 2, 'Should count 2 functions');
  assert(analyzer.metrics.comments === 1, 'Should count 1 comment');
});

// Test 6: Complexity calculation
test('Should calculate complexity score', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = `if (x) {
    if (y) {
      while (z) {
        for (let i = 0; i < 10; i++) {
          // complexity
        }
      }
    }
  }`;
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.metrics.complexity > 1, 'Should calculate complexity > 1');
});

// Test 7: TODO detection
test('Should detect TODO comments', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = '// TODO: fix this later';
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.suggestions.some(s => s.includes('TODO')), 'Should suggest addressing TODO comments');
});

// Test 8: Long line detection
test('Should detect long lines', () => {
  const analyzer = new CodeAnalyzer();
  const longLine = 'a'.repeat(130);
  analyzer.analyzeContent(longLine, '.js');
  assert(analyzer.issues.some(i => i.message.includes('exceeds 120 characters')), 'Should detect long lines');
});

// Test 9: API key detection
test('Should detect hardcoded API keys', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = 'const api_key = "sk-123456789";';
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.issues.some(i => i.message.includes('API key')), 'Should detect API keys');
});

// Test 10: File analysis
test('Should analyze example files without errors', () => {
  const analyzer = new CodeAnalyzer();
  const badCodePath = './examples/bad-code.js';
  
  if (fs.existsSync(badCodePath)) {
    const result = analyzer.analyzeFile(badCodePath);
    assert(result !== null, 'Should return analysis result');
    assert(result.issues.length > 0, 'Bad code should have issues');
  }
});

// Test 11: Clean code analysis
test('Good code should have fewer issues', () => {
  const badAnalyzer = new CodeAnalyzer();
  const goodAnalyzer = new CodeAnalyzer();
  
  const badCode = 'const password = "admin"; eval(x); element.innerHTML = data;';
  const goodCode = 'const USER_CONFIG = {}; function validate() { return true; }';
  
  badAnalyzer.analyzeContent(badCode, '.js');
  goodAnalyzer.analyzeContent(goodCode, '.js');
  
  assert(badAnalyzer.issues.length > goodAnalyzer.issues.length, 
    'Bad code should have more issues than good code');
});

// Test 12: Console.log detection
test('Should suggest replacing multiple console.log calls', () => {
  const analyzer = new CodeAnalyzer();
  const testCode = `
    console.log('1');
    console.log('2');
    console.log('3');
    console.log('4');
    console.log('5');
    console.log('6');
  `;
  analyzer.analyzeContent(testCode, '.js');
  assert(analyzer.suggestions.some(s => s.includes('console.log')), 
    'Should suggest using proper logging library');
});

// Summary
console.log('\n' + '='.repeat(50));
console.log(`Tests completed: ${passed + failed}`);
console.log(`✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log('='.repeat(50) + '\n');

if (failed > 0) {
  process.exit(1);
} else {
  console.log('🎉 All tests passed!\n');
  process.exit(0);
}
