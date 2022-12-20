env=~/.ssh/agent.env

agent_load_env () { test -f "$env" && . "$env" >| /dev/null ; }

agent_start () {
    (umask 077; ssh-agent >| "$env")
    . "$env" >| /dev/null ; }

agent_load_env

# agent_run_state: 0=agent running w/ key; 1=agent w/o key; 2=agent not running
agent_run_state=$(ssh-add -l >| /dev/null 2>&1; echo $?)

if [ ! "$SSH_AUTH_SOCK" ] || [ $agent_run_state = 2 ]; then
    agent_start
    ssh-add
elif [ "$SSH_AUTH_SOCK" ] && [ $agent_run_state = 1 ]; then
    ssh-add
fi

unset env

# Alias
alias clean="~/inkutils/scripts/clean.sh"
alias cry="python -m crypto $*"
alias rename="python ~/inkutils/source/hash_rename.py $*"
alias stats="python ~/inkutils/source/stats.py $*"
alias sv="ifconfig || ipconfig; python -m http.server $*"
alias venv=". ~/inkutils/scripts/venv.sh $*"
