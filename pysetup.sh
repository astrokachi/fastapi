#!/bin/bash

if [[ $SHELL == *bash ]]; then
    echo "✔️ BASH shell, good..."
    if [[ $0 == *bash ]]; then
        echo "✔️ Sourced!"
    else
        >&2 echo "❌ Don't run < ${0##*/} > directly mate! Source it!" 
        >&2 echo "   DO: $ source ${0##*/}"
        >&2 echo " "
        exit 1
    fi
else
    >&2 echo "❌ Run what you deploy! Switch to using BASH shell!"
    >&2 echo "" 
    return 99
fi

echo -ne " Virtual ENV check...\r"
python -m venv ./venv
if [ $? -eq 0 ]; then
    echo "✔️ Python venv looks happy"
else
    >&2 echo "\n"
    >&2 echo "❌ Python error creating the VENV." 
    return 2
fi

echo -ne " Activating venv..\r" 
source ./venv/Scripts/activate

if [ $? -eq 0 ]; then
    echo "✔️ Python venv Activated!"
else
    >&2 echo "\n"
    >&2 echo "❌ Error Activating the VENV."
    return 3
fi

if [[ ${VIRTUAL_ENV} ]]; then
    echo "✔️ VIRTUAL_ENV = $VIRTUAL_ENV"
else
    >&2 echo "\n"
    >&2 echo "❌ Python Virtual Environment not working."
    return 4
fi

if [[ -f ${VIRTUAL_ENV}/Scripts/pip.exe ]]; then 
    echo "✔️ pip binary is where it should be!" 
else
    >&2 echo "\n"
    echo "❌ pip is missing"
    return 5
fi

echo -ne " Update pip...\r"
pip install --upgrade pip > /dev/null
if [ $? -eq 0 ]; then
    vs=`pip --version`
    va=($vs)
    echo "✔️ pip is up to date: [v${va[@]:1:1}]"
else
    >&2 echo "\n"
    >&2 echo "❌ Failed to upgrade pip."
    return 6
fi

req_file=requirements.txt 
req_path="./"
if [[ -f ./${req_file} ]]; then 
    echo "✔️ requirements.txt file found in current dir" 
elif [[ -f ../${req_file} ]]; then
    echo "✔️ requirements.txt file found in PARENT dir"
    req.paths"../"
else
    >&2 echo "\n"
    echo "❓ No requirements.txt file found"
    python --version
    pip list
    echo " "
    echo "OK, now go run: python example.py"
    return 0
fi

pip install -r $req_path$req_file --require-virtualenv > /dev/null 
if [ $? -eq 0 ]; then
    echo "✔️ pip installed all libs from requirement.txt OK." 
else
    >&2 echo "\n"
    >&2 echo "❌ PIP: Installing requirements failed" 
    return 7
fi 

echo " "
python --version
pip list
echo " "
echo "OK, now go run: python example.py"
