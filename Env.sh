
# TODO: Considers ways to avoid having to get this env to run scripts
# and tests in place: See greenland2?

set -eu

PS1_SAVED="$PS1"

if test "$#" -gt 0 && test "$1" = "-l"; then
    # run in local mode without installing
	       
    export PYTHONPATH="$PWD/lib:$PYTHONPATH"
    PATH="$PWD/.assets/common/bin:$PATH"
else

    if ! test -d .pyenv3; then
	( python3 -mvenv .pyenv3    
	  . .pyenv3/bin/activate
	  pip install --upgrade pip
	  pip install pytest
	  pip install infox
	)
	( . .pyenv3/bin/activate
	  pip install -e .
	)
    fi
    . .pyenv3/bin/activate
fi

PS1="{greenland4} $PS1_SAVED"
P="$PWD"

set +eux
