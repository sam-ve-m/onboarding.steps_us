fission spec init
fission env create --spec --name onb-us-steps-env --image nexus.sigame.com.br/fission-onboarding-us-steps:0.1.0 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-steps-fn --env onb-us-steps-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name onb-us-steps-rt --method GET --url /onboarding/steps_us --function onb-us-steps-fn
