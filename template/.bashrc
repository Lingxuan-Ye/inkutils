# ================================================================
# Template Injection
# ----------------------------------------------------------------
# - $dir should be a Posix-style path with no trailing '/'
# - Do not remove 'TAG' comment!
# ================================================================

USERNAME={% config user.alias %}
dir={% root %}

# stop




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
    PATH="$dir/script/"
else
    PATH="$dir/script/":"$PATH"
fi

export OS="$(uname)"
export PATH
export PYTHONPATH="$dir/library/":"$dir/script/"
export USERNAME

if [[ "$OS" = MINGW* ]]; then
    setx PYTHONPATH "$PYTHONPATH"
fi




# ================================================================
# Aliases
# ================================================================

alias clean="bash $dir/script/clean.sh"
alias cry="python $dir/script/crypto/ $@"
alias stats="python $dir/script/stats.py $@"
alias sv="ifconfig || ipconfig && python -m http.server $@"
alias venv="source $dir/script/venv.sh $@"

unset dir




# ================================================================
# Functions
# ================================================================

function randrange () {

    # implementing a randrange function using $RANDOM (from 0x0000 to 0x7FFF)
    # with its result following uniform distribution is much more complicated
    # than expected; a possible implementation may be like (pseudocode with
    # Python syntax, EXCEPT $RANDOM in shell syntax):
    #
    # ```
    # def randrange(start: int, stop: int) -> int:
    #     num = stop - start
    #     assert 0 < num <= 0x8000
    #     upper_limit = 0x8000 - 0x8000 % num  # exclude
    #     While True:
    #         random = int($RANDOM)
    #         if random >= upper_limit:
    #             continue
    #         offset = random % num
    #         return start + offset
    # ```

    case $# in
        0)
            declare -i start=0
            declare -i stop=0x8000
            declare -i step=1 ;;
        1)
            declare -i start=0
            declare -i stop=$1
            declare -i step=1 ;;
        2)
            declare -i start=$1
            declare -i stop=$2
            declare -i step=1 ;;
        *)
            declare -i start=$1
            declare -i stop=$2
            declare -i step=$3 ;;
    esac

    python -c "import random; print(random.randrange($start, $stop, $step))"

}


function sim_typing() {
    declare line="$@"
    for (( i=0; i<${#line}; i++ )); do
        # declare span="0.02$( randrange 10 )"  # way too slow
        # sleep "$span"  # inaccurate
        python -c \
        "import random, time; time.sleep(0.015+random.randrange(4)/200)"
        echo -n "${line:$i:1}"
    done
    echo
}




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
case $( randrange 100 ) in
    0)
        sim_typing "诶多 …… ☆ 是 ♡ 同 ♡ 类 ♡ 呢 ♡ 喵 ♪（由乃逆光捧脸.jpg）"
        sim_typing "那群八嘎是不会懂的呀 …… 关于「二次元の美好」♡ "
        sim_typing "呐，如果说吾の存在有意义的话、那一定是因为「二·次·元」吧 ☆ ？"
        sim_typing "所以呢 —— 妄图污染这份「爱」的人类、都会被吾「抹」「杀」「掉」喔 ♪ "
        sim_typing "（小声）嘛 …… 讨厌二次元的八嘎三次元最恶心了啊魂淡！★" ;;
    1)
        sim_typing "呐、二次元の民那 …… 都·是·最·最·善·良·の·存·在·呐 ☆ "
        sim_typing "多洗忒 …… 要「嘲笑」这样的孩子呢？吾辈不明白啊 —— "
        sim_typing "嘛 …… 说到底，你们都只是污秽の「来自三次元的大人」吧？"
        sim_typing "大人什么的、最·讨·厌·了 ★ ♪" ;;
    2)
        sim_typing "啊嘞啊嘞 QAQ？多洗忒 …… 欧尼酱 ww？"
        sim_typing "呐、桥豆麻袋 …… 已经「厌烦」吾辈了嘛？"
        sim_typing "哼唧 …… 真是「冷·酷·の·人」呢 QuQ —— ☆(๑°⌓°๑) "
        sim_typing "嘛 …… 即便是这样的瓦塔西，一定也是有「存·在·の·意·义」的吧、内 ~ ★ "
        sim_typing "快来「肯定」啊？不然呀 …… 咱可就要「黑化」了哦 ♪ 呐？" ;;
    3)
        sim_typing "呐。。。（伸出的小手又迅速垂下去）"
        sim_typing "嗦嘎（表情有点失落），米娜桑已经不喜欢了呀（紧咬嘴唇）"
        sim_typing "得磨，米娜桑忘了当初吗（握紧小手）"
        sim_typing "莫以得丝（强忍住眼泪），已经大丈夫了呦（挤出笑脸）"
        sim_typing "瓦大喜瓦，滋多滋多，滋多滋多（语气越来越用力了）滋多戴斯给！！！"
        sim_typing "一滋嘛叠磨瓦撕裂嘛赛！！！至死都不会瓦斯裂嘛斯（认真的表情）" ;;
    4)
        sim_typing "诶多 …… 看起来阁下对于「二·次·元」の理解、似·乎·满·是·谬·误·哦 ☆ ~ "
        sim_typing "嘛，连最为基本の「礼♪义♪廉♪耻♪」都早已失去了啊 …… ♪（笑）"
        sim_typing "呐，我说啊 —— 这样の kimino、也有自称「二 ♡ 次 ♡ 元」の资格吗 ★ ？"
        sim_typing "fufufu —— 说到底、阁下已经「二·次·元·失·格」了吧？呐 ~ ♪" ;;
    5)
        sim_typing "唔噗噗 ~ 汝等「劣·等·生·物」...... 也配去「妄想」吗？"
        sim_typing "呐、「真正的二次元」什么的 —— 吾辈看汝是一点都不懂啊 ☆（笑）"
        sim_typing "嘛嘛嘛 ...... 不过看着汝试图伪装成「二次元」の可笑姿态，"
        sim_typing "倒是让吾辈对于「三·次·元·的·白·痴」稍微有了些许兴趣哦？★" ;;
    6)
        sim_typing "哼！（跺了跺粉嫩的小脚，肉嘟嘟的小手交叉摆在胸前，小嘴一撅，"
        sim_typing "头抬得高高的撇向一边，一副生人勿近的模样。又怕你真的离开，"
        sim_typing "偷偷侧过脑袋看你）" ;;
    7)
        sim_typing "请暂停一下，我是来提醒你别忘了去做你妈妈嘱咐你要做的事，"
        sim_typing "例如把冰箱里的肉拿出来解冻之类的 ……" ;;
    8)
        sim_typing "喜欢你啊！八嘎！"
        sim_typing "为什么察觉不到啊，八嘎八嘎八嘎，最讨人厌啦。"
        sim_typing "但又是那么喜欢你，suki，suki，daisuki。"
        sim_typing "笨蛋，再多看看我啊！毕竟人家，最喜欢你了啊。" ;;
    9)
        sim_typing "哑巴的，沉默的，尴尬的，破防的，打脸的，可怜的，小丑的。" ;;
    [1-3][0-9])
        echo "Hello, $USERNAME! Nice to meet you!" ;;
    [4-6][0-9])
        echo "你好，$USERNAME！很高兴见到你！" ;;
    [7-9][0-9])
        echo "こんにちは、$USERNAME！はじめまして！" ;;
esac
echo
