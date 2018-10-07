#!/bin/bash

python predict_rating_test_file.py ./test_data/data1.json ./test_data/output1.json
python get_accuracy_score.py ./test_data/output1.json ./test_data/expected_result1.json
