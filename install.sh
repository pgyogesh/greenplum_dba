#!/usr/bin/env bash

## Check OS

if [[ "$OSTYPE" =~ "darwin" ]]
then
    export OS="mac"
elif [[ "$OSTYPE" == "linux-gnu" ]]
then
    export OS="linux"
else
    echo "Don't know what to do with '$OSTYPE' operating system"
    exit 1
fi

# Git and Curl required
if [[ $(which git) == "" ]]
then
    echo "Install git ( http://git-scm.com ) first"
    exit 1
fi
if [[ $(which curl) == "" ]]
then
    echo "Install curl ( http://curl.haxx.se ) first"
    exit 1
fi


# Backup Existing Dot Files

export VIM_BACKUP_DIR="/tmp/dotvim-backup"
mkdir -p $VIM_BACKUP_DIR
echo "Backing up existing vim files to $VIM_BACKUP_DIR"
for f in $(ls -a $VIM_BACKUP_DIR| grep -v '^.$' | grep -v '^..$')
do
    rm -rf "$VIM_BACKUP_DIR/$f"
done
for f in "$HOME/.vimrc" "$HOME/.gvimrc" "$HOME/.vimrc.local" "$HOME/.vim" "$HOME/.bash_aliases" "$HOME/.bash_prompt" "$HOME/.bash_profile"
do
    [[ -s "$f" ]] && mv -f "$f" $VIM_BACKUP_DIR
done

echo "Ensuring backup directory exists"
mkdir -p "$HOME/.vim/backup"

echo "Download Vundle"
mkdir -p "$HOME/.vim/bundle"
if [[ ! -d "$HOME/.vim/bundle/vundle" ]]
then
    git clone http://github.com/gmarik/vundle.git "$HOME/.vim/bundle/vundle"
fi

echo "Link dotfiles"
ln -s -f "$PWD/dotfiles/vimrc" "$HOME/.vimrc"
ln -s -f "$PWD/dotfiles/gvimrc" "$HOME/.gvimrc"
ln -s -f "$PWD/dotfiles/bash_aliases" "$HOME/.bash_aliases"
ln -s -f "$PWD/dotfiles/bash_prompt" "$HOME/.bash_prompt"
ln -s -f "$PWD/dotfiles/bash_profile" "$HOME/.bash_profile"
ln -s -f "$PWD/dotfiles/bash_exports" "$HOME/.bash_exports"
ln -s -f "$PWD/dotfiles/psqlrc" "$HOME/.psqlrc"


echo "Instruct Vundle to download all the scripts"
vim +BundleInstall +qall

mkdir -p "`python -m site --user-site`"
cp "$PWD/scripts/gplog.py" "`python -m site --user-site`"
echo "Finished"

