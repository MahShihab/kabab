#! /usr/bin/env sh

echo "Running inside /src/prestart.sh, you could add migrations to this file"

pip3 install --user git+https://github.com/idot/meinheld.git@patch-1 # patch for meinheld-greenlet version mismatch
# TODO check if this is still needed