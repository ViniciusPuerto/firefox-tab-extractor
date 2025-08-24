#!/bin/bash

# Build and Publish Script for Firefox Tab Extractor
# This script helps with local building and publishing to PyPI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to clean previous builds
clean_build() {
    print_status "Cleaning previous builds..."
    rm -rf build/ dist/ *.egg-info/
    print_success "Build cleaned"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    if command_exists pytest; then
        pytest tests/ -v
        print_success "Tests passed"
    else
        print_warning "pytest not found, skipping tests"
    fi
}

# Function to run linting
run_lint() {
    print_status "Running linting checks..."
    
    if command_exists black; then
        print_status "Running Black..."
        black --check firefox_tab_extractor/ tests/ examples/
        print_success "Black passed"
    else
        print_warning "Black not found, skipping"
    fi
    
    if command_exists flake8; then
        print_status "Running flake8..."
        flake8 firefox_tab_extractor/ tests/ examples/
        print_success "flake8 passed"
    else
        print_warning "flake8 not found, skipping"
    fi
    
    if command_exists mypy; then
        print_status "Running mypy..."
        mypy firefox_tab_extractor/
        print_success "mypy passed"
    else
        print_warning "mypy not found, skipping"
    fi
}

# Function to build package
build_package() {
    print_status "Building package..."
    
    # Install build dependencies if not present
    if ! command_exists build; then
        print_status "Installing build dependencies..."
        pip install build twine
    fi
    
    # Build the package
    python -m build
    
    # Check the package
    twine check dist/*
    
    print_success "Package built successfully"
}

# Function to publish to Test PyPI
publish_test() {
    print_status "Publishing to Test PyPI..."
    
    if [ -z "$TEST_PYPI_TOKEN" ]; then
        print_error "TEST_PYPI_TOKEN environment variable not set"
        print_status "To set it up:"
        print_status "1. Go to https://test.pypi.org/manage/account/token/"
        print_status "2. Create a new token"
        print_status "3. Export TEST_PYPI_TOKEN=your_token_here"
        exit 1
    fi
    
    twine upload --repository testpypi dist/*
    print_success "Published to Test PyPI"
}

# Function to publish to PyPI
publish_production() {
    print_status "Publishing to PyPI..."
    
    if [ -z "$PYPI_TOKEN" ]; then
        print_error "PYPI_TOKEN environment variable not set"
        print_status "To set it up:"
        print_status "1. Go to https://pypi.org/manage/account/token/"
        print_status "2. Create a new token"
        print_status "3. Export PYPI_TOKEN=your_token_here"
        exit 1
    fi
    
    twine upload dist/*
    print_success "Published to PyPI"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  clean       Clean previous builds"
    echo "  test        Run tests"
    echo "  lint        Run linting checks"
    echo "  build       Build the package"
    echo "  test-pypi   Publish to Test PyPI"
    echo "  pypi        Publish to PyPI"
    echo "  all         Run all steps (clean, test, lint, build)"
    echo "  release     Full release (all + publish to PyPI)"
    echo "  help        Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  TEST_PYPI_TOKEN  Token for Test PyPI (for test-pypi command)"
    echo "  PYPI_TOKEN       Token for PyPI (for pypi and release commands)"
    echo ""
    echo "Examples:"
    echo "  $0 build                    # Build package only"
    echo "  $0 test-pypi                # Publish to Test PyPI"
    echo "  $0 release                  # Full release to PyPI"
}

# Main script logic
case "${1:-help}" in
    clean)
        clean_build
        ;;
    test)
        run_tests
        ;;
    lint)
        run_lint
        ;;
    build)
        clean_build
        run_tests
        run_lint
        build_package
        ;;
    test-pypi)
        clean_build
        run_tests
        run_lint
        build_package
        publish_test
        ;;
    pypi)
        clean_build
        run_tests
        run_lint
        build_package
        publish_production
        ;;
    all)
        clean_build
        run_tests
        run_lint
        build_package
        ;;
    release)
        clean_build
        run_tests
        run_lint
        build_package
        publish_production
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
esac
