#!/bin/bash
fission spec init
fission env create --spec --name onboarding-steps-us-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name onboarding-steps-us-fn --env onboarding-steps-us-env --src "./func/*" --entrypoint main.get_onboarding_step_us  --rpp 100000
fission route create --spec --method GET --url /onboarding_steps_us --function onboarding-steps-us-fn
