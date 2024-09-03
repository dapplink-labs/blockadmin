#!/bin/bash

for envdir in $(echo $PWD/../../env $PWD/../../py3); do
    if [ -x "$envdir/bin/python" ]; then
        export ENVDIR=$envdir
        source $ENVDIR/bin/activate
        break
    fi
done

if [ -z "$ENVDIR" ]; then
    echo No envdir exist >&2
    return
fi

export PYTHONPATH="$ENVDIR:$PWD::$PYTHONPATH"
export PATH="$ENVDIR/bin:$PATH"
