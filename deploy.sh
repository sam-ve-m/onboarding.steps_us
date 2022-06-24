#!/bin/bash
fission spec init
fission env create --spec --name watch-list-save-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name watch-list-save-fn --env watch-list-save-env --src "./func/*" --entrypoint main.save_symbols  --rpp 100000
fission route create --spec --method POST --url /watch_list/add --function watch-list-save-fn
