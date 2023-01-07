#!/usr/bin/env bash

# run this script once you move or rename 'inkutils'

echo "$( dirname -- "$( readlink -f -- "$0" )" )" > ~/.inkpath
