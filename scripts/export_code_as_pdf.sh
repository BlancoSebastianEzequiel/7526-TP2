#!/usr/bin/env bash

SRC=src/

create_file () {
    # shellcheck disable=SC2045
    for case in $(ls "$1"); do
        filename=$(basename ${case%%.*})
        extension="${case##*.}"
        if [ $extension != 'py' ]; then
            continue
        fi

        echo "# $case" >> code.md
        echo '```' >> code.md
        cat "$1"/"$case" >> code.md
        echo '  ' >> code.md
        echo '```' >> code.md
    done
}

if [ -e code.md ]; then
    rm code.md
fi
touch code.md
echo "## src" >> code.md
create_file $SRC
pandoc code.md -t latex -o doc/code.pdf
rm code.md