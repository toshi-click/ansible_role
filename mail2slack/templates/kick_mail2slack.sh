#!/bin/sh

# Working Directroy
cd {{ mail2slack_deploy_path }}

# Exec Script
cat - | {{ mail2slack_python_path }} {{ mail2slack_execute_path }}
