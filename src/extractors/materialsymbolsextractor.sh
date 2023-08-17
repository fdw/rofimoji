#!/bin/env bash

url="https://raw.githubusercontent.com/google/material-design-icons/master/variablefont/MaterialSymbolsOutlined%5BFILL%2CGRAD%2Copsz%2Cwght%5D.codepoints"

curl -s "$url" |
    while read -r line; do
        echo -e "\u${line#* } ${line% *}"
    done
