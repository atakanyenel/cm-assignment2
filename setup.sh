#!/bin/bash
if [ ! -f big.txt ]
then
wget https://norvig.com/big.txt
cp big.txt sim/big.txt
fi



