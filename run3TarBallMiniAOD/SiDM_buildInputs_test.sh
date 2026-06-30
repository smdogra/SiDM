#!/bin/bash
export TARBALLDIR="/u/user/sdogra/runTarBallMiniAODv2"

#for FILE in inputs/SIDM_BsTo2DpTo4Mu_MBs-*_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz
#for FILE in inputs/SIDM_BsTo2DpTo4Mu_MBs-10_MDp-1p2_ctau-96_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz
#for FILE in inputs/SIDM_BsTo2DpTo4Mu_MBs-500_MDp-5_ctau-75_Sam_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz
for FILE in inputs/SIDM_XXTo2ATo4Mu_mXX-150_mA-5_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz
do
    echo  $FILE
    PROCESS=$(echo ${FILE} | cut -d "/" -f 2 | sed 's/\_tarball.tar.xz//')
    echo ${PROCESS}
    export BASEDIR=${PWD}
    rm -r work${1}_${PROCESS}
    mkdir work${1}_${PROCESS}
    export SUBMIT_WORKDIR=${PWD}/work${1}_${PROCESS}
    year=${1}
    dirname_tmp=${PROCESS}
    dirname_tem=$(echo ${dirname_tmp} | cut -d "/" -f 2 | sed 's/\_slc6_amd64_gcc481_CMSSW_7_1_30//')
    echo $dirname_tem
    dirname=$dirname_tem
    echo "Final Directory Name  :    " $dirname 

    if [ ${year} -eq 2016 ]; then
        cp ./pythiafragments/${dirname}.py inputs/.
    fi
    if [ ${year} -eq 2017 ]; then
        cp ./pythiafragments/${dirname}.py inputs/.
    fi
    if [ ${year} -eq 2018 ]; then
	cp ./pythiafragments/${dirname}.py inputs/.
    fi
    sed -i "s/processname/${PROCESS}/"  inputs/${dirname}.py


    echo "TARBALL=${PROCESS}_tarball.tar.xz" > ./submit/inputs.sh
    echo "HADRONIZER=${dirname}.py  " >> ./submit/inputs.sh
    echo "PROCESS=${PROCESS}" >> ./submit/inputs.sh
    echo "dirname=${dirname}" >> ./submit/inputs.sh
    echo "USERNAME=${USER}" >> ./submit/inputs.sh    
    

    if [ -z "$2" ]
    then
	echo "MERGE=0" >> ./submit/inputs.sh
	echo "You want to produce events for $1. Good luck!"
    else
	echo "MERGE=1" >> ./submit/inputs.sh
	echo "You want to merge the T2 files for $1? Ok."
    fi
    
    
    if [ ${year} -eq 2016 ]; then
	mkdir -p ./submit/input/
	cp ${TARBALLDIR}/inputs/${PROCESS}_tarball.tar.xz ./submit/input/
	cp ${TARBALLDIR}/inputs/${dirname}.py ./submit/input/
	cp ${BASEDIR}/exec2016HIPM.sh $SUBMIT_WORKDIR
	cp ${BASEDIR}/exec2016post.sh $SUBMIT_WORKDIR
    fi
    
    if [ ${year} -eq 2017 ]; then
	mkdir -p ./submit/input/
	cp ${TARBALLDIR}/inputs/${PROCESS}_tarball.tar.xz ./submit/input/
	cp ${TARBALLDIR}/inputs/${dirname}.py ./submit/input/
	cp ${BASEDIR}/exec2017.sh $SUBMIT_WORKDIR
    fi
    
    if [ ${year} -eq 2018 ]; then
	mkdir -p ./submit/input/
	cp ${TARBALLDIR}/inputs/${PROCESS}_tarball.tar.xz ./submit/input/
	cp ${TARBALLDIR}/inputs/${dirname}.py ./submit/input/
	cp ${BASEDIR}/exec2018.sh $SUBMIT_WORKDIR
    fi
    
    
    #creating tarball
    echo "Tarring up submit..."
    tar -chzf submit.tgz submit 
    rm -r ${BASEDIR}/submit/input/*
    
    mv submit.tgz $SUBMIT_WORKDIR
    
    rm -rf submit/inputs.sh
    #does everything look okay?
    ls -lh $SUBMIT_WORKDIR
done
