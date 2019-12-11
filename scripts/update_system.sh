#! /bin/bash

read -p "Do you really want to update system? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo 'Running apt-get upgrades'
    sudo apt update && sudo apt upgrade -y && sudo apt autoremove
    read -p "Should I run dist-upgrade? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
      echo 'Running dist-upgrade'
      sudo apt dist-upgrade && sudo apt autoremove
    fi
    sudo gem update && sudo snap refresh
    read -p 'Should I reboot? ' -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
      echo 'Rebooting!'
      sudo reboot
    fi
fi