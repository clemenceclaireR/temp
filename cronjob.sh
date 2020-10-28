#!/bin/sh

/home/clemence/env_virtuels/projet10/bin/python /home/clemence/sites/PurBeurre_Production/manage.py api_openfoodfacts 2>&1 | tee /home/clemence/sites/PurBeurre_Production/log_bdd_inputs.txt
