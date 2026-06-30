#!/bin/bash

export HOME=${PWD}

tar xvaf submit.tgz
cd submit
bash ./runEventGeneration2023.sh
cd ${HOME}
rm -r submit/
exit 0
