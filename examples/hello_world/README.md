# Hello World
The tflite micro repository contains Python scripts to train the model
(train.py) and to evaluate (evaluate.py) and test it (evaluate_test.py).
These programs are built and run through the _bazel_ build system.

In the TinyML book jupyter notebooks were used allowing to execute the
procedures step by step and to inspect the result after each step. I re-built
these notebooks with the corresponding explication added in makrdown text.

* train.ipynb transforms train.py into a notebook
* create_sine_model.ipynb corresponds more or less to the notebook described
in the book. In contrary to the new version, it uses a sine function with added
noise for training (the new version uses a straight sine function).
