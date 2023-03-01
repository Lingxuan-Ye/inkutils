# ================================================================
# Template Injection
# ----------------------------------------------------------------
# - $dir should be a Posix-style path with no trailing '/'
# - Do not remove 'TAG' comment!
# ================================================================

USERNAME={% config user.name %}
NICKNAME={% config user.alias %}
root={% root %}

# stop

scripts="${root}/scripts"
library="${root}/library"




# ================================================================
# Shell Options
# ================================================================

shopt -s cdspell
shopt -s cmdhist
shopt -s dotglob
shopt -s globstar




# ================================================================
# Environment Variables
# ----------------------------------------------------------------
# - `export` may not be necessary
# ================================================================

if [[ -z "$PATH" ]]; then
    PATH="$scripts":"/C/ProgramData/chocolatey/bin"
else
    PATH="$scripts":"/C/ProgramData/chocolatey/bin":"$PATH"
fi

export OS="$(uname)"
export PATH
export PYTHONPATH="$library":"$scripts"
export USERNAME

if [[ "$OS" = MINGW* ]]; then
    library_="${library:1}"
    scripts_="${scripts:1}"
    setx PYTHONPATH "${scripts_/'/'/':/'};${scripts_/'/'/':/'}" >| /dev/null
    unset library_
    unset scripts_
fi




# ================================================================
# Aliases
# ================================================================

alias clean="bash ${scripts}/clean.sh"
alias cry="python ${scripts}/crypto/ $@"
alias stats="python ${scripts}/stats.py $@"
alias sv="ifconfig || ipconfig && python -m http.server $@"
alias venv="source ${scripts}/venv.sh $@"

unset root
unset scripts
unset library




# ================================================================
# Activate Default Virtual Environment
# ================================================================

source ~/venv/ink/Scripts/activate




# ================================================================
# Launch ssh-agent
# ----------------------------------------------------------------
# - Source copied from GitHub Docs with trivial modification
# ================================================================

env=~/.ssh/agent.env

function agent_load_env () {
    test -f "$env" && source "$env" >| /dev/null
}

function agent_start () {
    (umask 077; ssh-agent >| "$env")
    source "$env" >| /dev/null
}

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
unset -f agent_load_env
unset -f agent_start




# ================================================================
# Welcome
# ================================================================

echo
case $(( "$RANDOM" % 16 )) in
    0)
        python -m simulate_typing ;;
    [1-5])
        echo "Hello, $NICKNAME! Nice to meet you!" ;;
    [6-9] | 10)
        echo "你好，$NICKNAME！很高兴见到你！" ;;
    1[1-5])
        echo "こんにちは、$NICKNAME！はじめまして！" ;;
esac
echo
