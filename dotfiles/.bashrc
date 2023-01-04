# ================================================================
# Author: Lingxuan Ye
# Website: https://lingxuan-ye.github.io
# ================================================================


# ----------------------------------------------------------------
# Auto-launching `ssh-agent` on Git for Windows
# ----------------------------------------------------------------

if [[ "$(uname)" == "MINGW*" ]]; then

    env=~/.ssh/agent.env

    agent_load_env () { test -f "$env" && . "$env" >| /dev/null ; }

    agent_start () {
        (umask 077; ssh-agent >| "$env")
        . "$env" >| /dev/null ; }

    agent_load_env

    # agent_run_state:
    # 0=agent running w/ key;
    # 1=agent w/o key;
    # 2=agent not running
    agent_run_state=$(ssh-add -l >| /dev/null 2>&1; echo $?)

    if [ ! "$SSH_AUTH_SOCK" ] || [ $agent_run_state = 2 ]; then
        agent_start
        ssh-add
    elif [ "$SSH_AUTH_SOCK" ] && [ $agent_run_state = 1 ]; then
        ssh-add
    fi

    unset env

fi


# ----------------------------------------------------------------
# Shell Options
# ----------------------------------------------------------------

shopt -s cdspell
shopt -s cmdhist
shopt -s dotglob
shopt -s globstar


# ----------------------------------------------------------------
# Exports
# ----------------------------------------------------------------

export PATH=$HOME/inkutils/scripts/:$HOME/.scripts/:$PATH
export PYTHONPATH=$HOME/inkutils/packages/python/:$HOME/.packages/:$PYTHONPATH
export USERNAME="Lingxuan Ye"
export NICKNAME="inknos"


# ----------------------------------------------------------------
# Alias
# ----------------------------------------------------------------

alias clean="~/inkutils/scripts/clean.sh"
alias cry="python -m crypto $@"
alias harn="python ~/inkutils/packages/python/hash_rename.py $@"
alias stats="python ~/inkutils/packages/python/stats.py $@"
alias sv="ifconfig || ipconfig && python -m http.server $@"
alias venv="source ~/inkutils/scripts/venv.sh $@"


# ----------------------------------------------------------------
# Welcome
# ----------------------------------------------------------------

echo "Welcome, $NICKNAME! Nice to see you!"
