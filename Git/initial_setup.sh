#!/bin/bash

# Setup user name and email, used for commits
git config --global user.name "Ares Ou"
git config --global user.email "aresowj@gmail.com"

# Setup alias for shortcuts
git config --global alias.cm "commit -m"
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.st "status"

# Setup default editor
git config --global core.editor vim
