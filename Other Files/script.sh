#!/bin/bash

echo "This script will remove all Python installations and reinstall Python using Homebrew."
echo "Please make sure you have backups of any important Python projects or virtual environments."
read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Operation cancelled."
    exit 1
fi

# Remove Python installations
echo "Removing Python installations..."
sudo rm -rf /Library/Frameworks/Python.framework
sudo rm -rf /Applications/Python*
sudo rm -rf /usr/local/bin/python*
sudo rm -rf /usr/local/bin/pip*

# Remove Python-related directories
echo "Removing Python-related directories..."
rm -rf ~/Library/Python
rm -rf ~/.python_history

# Remove Homebrew Python if installed
if command -v brew &> /dev/null
then
    echo "Removing Homebrew Python installations..."
    brew uninstall --force python python@2 python@3.7 python@3.8 python@3.9 python@3.10 python@3.11
    brew cleanup
fi
