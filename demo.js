/**
 * Demo script to showcase the AI Code Review Assistant
 * Run this to see the tool in action with various code samples
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import chalk from 'chalk';

const execAsync = promisify(exec);

console.log(chalk.bold.cyan('\n🎯 AI Code Review Assistant Demo\n'));
console.log(chalk.gray('This demo will analyze different code samples to showcase the tool\'s capabilities\n'));

const files = [
  { path: 'examples/bad-code.js', description: 'JavaScript with multiple issues' },
  { path: 'examples/good-code.js', description: 'Clean JavaScript code' },
  { path: 'examples/bad-code.py', description: 'Python with security vulnerabilities' }
];

async function runDemo() {
  for (const file of files) {
    console.log(chalk.yellow.bold(`\n${'='.repeat(60)}`));
    console.log(chalk.yellow.bold(`Demo: ${file.description}`));
    console.log(chalk.yellow.bold(`${'='.repeat(60)}\n`));
    
    try {
      const { stdout } = await execAsync(`node index.js ${file.path}`);
      console.log(stdout);
    } catch (error) {
      console.log(error.stdout || error.message);
    }
    
    // Wait a bit between demos
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log(chalk.green.bold('\n✨ Demo complete! The AI Code Review Assistant successfully analyzed all files.\n'));
  console.log(chalk.cyan('Try it with your own code:'));
  console.log(chalk.white('  npm start <your-file-path>\n'));
}

runDemo().catch(console.error);
