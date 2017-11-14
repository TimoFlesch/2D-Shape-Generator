#!/bin/bash


#-------------- bvae training data
# rota
python main.py --num_transformations 10 --to_transform trx try scale --shapes rect ellipse star5 

# colour
python main.py --num_transformations 10 --to_transform trx try colour --shapes rect ellipse star5 

# ------------- bvae test data (different shapes and offset)
# rota
python main.py --num_transformations 10 --to_transform trx try scale --shapes star6 poly3 --rng_trx .12 .92 --rng_try .12 .92 

# colour
python main.py --num_transformations 10 --to_transform trx try colour --shapes star6 poly3 --rng_trx .12 .92 --rng_try .12 .92 




