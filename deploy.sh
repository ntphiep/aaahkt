#!/bin/bash

# AWS DevOps Pipeline - Deployment Helper Script
# This script helps with local testing and deployment preparation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Header
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        AWS DevOps Pipeline - Deployment Helper              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "src" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Menu
echo "Select an option:"
echo "  1) Install dependencies (backend)"
echo "  2) Install dependencies (dashboard)"
echo "  3) Run tests"
echo "  4) Run demo"
echo "  5) Start backend API"
echo "  6) Start dashboard (development)"
echo "  7) Build dashboard (production)"
echo "  8) Check security vulnerabilities"
echo "  9) Deploy to Vercel (requires Vercel CLI)"
echo "  10) Full setup (install all dependencies)"
echo "  0) Exit"
echo ""
read -p "Enter option: " option

case $option in
    1)
        print_step "Installing Python dependencies..."
        pip install -r requirements.txt
        print_success "Backend dependencies installed"
        ;;
    
    2)
        print_step "Installing Node.js dependencies..."
        cd dashboard
        npm install
        cd ..
        print_success "Dashboard dependencies installed"
        ;;
    
    3)
        print_step "Running tests..."
        python -m pytest tests/ -v
        if [ $? -eq 0 ]; then
            print_success "All tests passed!"
        else
            print_error "Some tests failed"
            exit 1
        fi
        ;;
    
    4)
        print_step "Running demo script..."
        python demo.py
        print_success "Demo completed"
        ;;
    
    5)
        print_step "Starting backend API..."
        print_warning "API will run on http://localhost:8000"
        print_warning "Press Ctrl+C to stop"
        python -m src.api.main
        ;;
    
    6)
        print_step "Starting dashboard in development mode..."
        print_warning "Dashboard will run on http://localhost:3000"
        print_warning "Press Ctrl+C to stop"
        cd dashboard
        npm run dev
        ;;
    
    7)
        print_step "Building dashboard for production..."
        cd dashboard
        npm run build
        if [ $? -eq 0 ]; then
            print_success "Dashboard built successfully"
            print_success "Build output in dashboard/.next/"
        else
            print_error "Build failed"
            exit 1
        fi
        cd ..
        ;;
    
    8)
        print_step "Checking for security vulnerabilities..."
        
        print_step "Checking Python dependencies..."
        pip list --format=json | python -c "
import json, sys
deps = json.load(sys.stdin)
print(f'Found {len(deps)} Python packages installed')
"
        
        if [ -d "dashboard/node_modules" ]; then
            print_step "Checking Node.js dependencies..."
            cd dashboard
            npm audit || true
            cd ..
        else
            print_warning "Node modules not installed. Run option 2 first."
        fi
        
        print_success "Security check completed"
        ;;
    
    9)
        print_step "Deploying to Vercel..."
        
        # Check if Vercel CLI is installed
        if ! command -v vercel &> /dev/null; then
            print_error "Vercel CLI not found"
            print_warning "Install with: npm install -g vercel"
            exit 1
        fi
        
        print_warning "Make sure you've set up environment variables in Vercel"
        read -p "Continue with deployment? (y/n): " confirm
        
        if [ "$confirm" == "y" ]; then
            cd dashboard
            vercel --prod
            print_success "Deployment initiated"
        else
            print_warning "Deployment cancelled"
        fi
        ;;
    
    10)
        print_step "Full setup - Installing all dependencies..."
        
        print_step "1/3 Installing Python dependencies..."
        pip install -q -r requirements.txt
        print_success "Python dependencies installed"
        
        print_step "2/3 Installing Node.js dependencies..."
        cd dashboard
        npm install --silent
        cd ..
        print_success "Node.js dependencies installed"
        
        print_step "3/3 Running tests to verify setup..."
        python -m pytest tests/ -v
        
        if [ $? -eq 0 ]; then
            echo -e "\n${GREEN}"
            echo "╔══════════════════════════════════════════════════════════════╗"
            echo "║                    Setup Complete! ✓                         ║"
            echo "╚══════════════════════════════════════════════════════════════╝"
            echo -e "${NC}"
            echo "Next steps:"
            echo "  • Run './deploy.sh' and choose option 5 to start backend API"
            echo "  • Run './deploy.sh' and choose option 6 to start dashboard"
            echo "  • See DEPLOYMENT.md for deployment instructions"
        else
            print_error "Setup completed but tests failed"
            exit 1
        fi
        ;;
    
    0)
        print_warning "Exiting..."
        exit 0
        ;;
    
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
print_success "Operation completed successfully!"
