#!/usr/bin/bash
ssh -i ~/.ssh/school ubuntu@3.209.12.133 'sudo rm -rfv /var/www/keja-landing-page'
scp -ri ~/.ssh/school ./keja-landing-page ubuntu@3.209.12.133:~/
ssh -i ~/.ssh/school ubuntu@3.209.12.133 'sudo mv ~/keja-landing-page /var/www/'
