
def autocomplete():
  return """
  _script()
  {
    local cur
    local first

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    first="${COMP_WORDS[1]}"

    opts=$(petal --list-opts "${COMP_WORDS[*]:1}")
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
  }
  complete -F _script petal
  """
