# ================================================================
# Author: Lingxuan Ye
# Website: https://lingxuan-ye.github.io
# ================================================================


# ----------------------------------------------------------------
# Auto-launching `ssh-agent` on Git for Windows
# ----------------------------------------------------------------

if [[ "$(uname)" = MINGW* ]]; then

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
# Get absolute path of 'inkutils'
# ----------------------------------------------------------------

dir="$( cat ~/.inkpath )"


# ----------------------------------------------------------------
# Exports
# ----------------------------------------------------------------

export PATH="$dir/scripts/":$HOME/scripts/:$PATH
export PYTHONPATH="$dir/packages/python/":$HOME/packages/:$PYTHONPATH
export USERNAME="Lingxuan Ye"
export NICKNAME="inknos"


# ----------------------------------------------------------------
# Alias
# ----------------------------------------------------------------

alias clean="$dir/scripts/clean.sh"
alias cry="python -m crypto $@"
alias rn="python $dir/packages/python/hash_rename.py $@"
alias stats="python $dir/packages/python/stats.py $@"
alias sv="ifconfig || ipconfig && python -m http.server $@"
alias venv="source $dir/scripts/venv.sh $@"


# ----------------------------------------------------------------
# Activate default venv
# ----------------------------------------------------------------

source ~/venv/ink/Scripts/activate


# ----------------------------------------------------------------
# Welcome
# ----------------------------------------------------------------

echo
case $(( $RANDOM % 4 )) in
    0) echo "你好，$NICKNAME！很高兴见到你！" ;;
    1) echo "こんにちは、$NICKNAME！はじめまして！" ;;
    2) echo "Hello, $NICKNAME! Nice to meet you!" ;;
    3) echo -e "诶多……☆是♡同♡类♡呢♡喵♪\n\n啊嘞啊嘞QAQ？多洗忒……欧尼酱ww？呐、桥豆麻袋……已经「厌烦」吾辈了嘛？哼唧……真是「冷·酷·の·人」呢QuQ——☆(๑°⌓°๑)嘛……即便是这样的哇达西，一定也是有「存·在·の·意·义」的吧、内~★快来「肯定」啊？不然呀……咱可就要「黑化」了哦♪呐？" ;;
esac
echo
