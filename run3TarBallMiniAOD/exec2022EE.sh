#!/bin/bash

export HOME=${PWD}

tar xvaf submit.tgz
cd submit
bash ./runEventGeneration2022EE.sh
cd ${HOME}
rm -r submit/
exit 0
