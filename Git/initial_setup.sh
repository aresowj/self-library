#!/bin/bash

# Setup user name and email, used for commits
git config --global user.name "Ares Ou"
git config --global user.email "ares.ou@outlook.com"

# Setup alias for shortcuts
git config --global alias.cm "commit -m"
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.st "status"

# Setup default editor
git config --global core.editor vim

# Enable long name support on Windows, run git bash as administrator if encounting permission issue
git config --system core.longpaths true
