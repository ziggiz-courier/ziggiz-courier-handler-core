#!/bin/zsh
# setup_tox_environment.sh - Setup script for tox testing environment

echo "Setting up environment for tox matrix testing of Ziggiz-Courier..."

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "pyenv not found. Installing pyenv..."
    if [ "$(uname)" = "Darwin" ]; then
        brew install pyenv
    else
        echo "Please install pyenv manually for your platform."
        echo "See: https://github.com/pyenv/pyenv#installation"
        exit 1
    fi
fi

# Install Python versions
echo "Installing required Python versions. This may take a while..."
PYTHON_VERSIONS=("3.8.18" "3.9.18" "3.10.13" "3.11.8" "3.12.2" "3.13.0")

for version in "${PYTHON_VERSIONS[@]}"; do
    echo "Installing Python $version..."
    pyenv install -s "$version"
done

# Make all versions available
echo "Making Python versions available globally..."
pyenv global system "${PYTHON_VERSIONS[@]}"

# Install tox
echo "Installing tox and tox-poetry..."
pip install tox tox-poetry

echo "Environment setup complete!"
echo "You can now run 'tox' to test across all Python versions"
echo "See TOX_GUIDE.md for more detailed instructions"
