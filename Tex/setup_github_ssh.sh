#!/bin/bash
# Generate SSH key for GitHub
ssh-keygen -t ed25519 -C "fzmwml@github" -f ~/.ssh/id_ed25519 -N ""
echo "SSH key generated successfully!"
echo "Public key content:"
cat ~/.ssh/id_ed25519.pub
