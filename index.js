#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// This script allows the MCP server to be run via npx
// It spawns the Python MCP server process

const args = process.argv.slice(2);
const pythonArgs = ['-m', 'wolt_api_mcp.server', ...args];

const child = spawn('python', pythonArgs, {
  stdio: 'inherit',
  cwd: process.cwd()
});

child.on('error', (error) => {
  console.error('Failed to start MCP server:', error);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code);
});

// Handle signals
process.on('SIGINT', () => {
  child.kill('SIGINT');
});

process.on('SIGTERM', () => {
  child.kill('SIGTERM');
});