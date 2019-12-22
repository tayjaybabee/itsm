 #!/bin/bash

userName=$(whoami);
programName="$1";
main(){
    pidVar=$(top -n 1 -d 1 -b | grep -i "$programName" | cut -c -6 );
    kill $pidVar >& /dev/null;
    echo "killed all \"$programName\" instances.";
}

if [ "$EUID" -ne 0 ] 
    then echo "run as root"
    exit
fi

