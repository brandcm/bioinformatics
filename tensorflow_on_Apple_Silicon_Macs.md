# tensorflow on Apple Silicon Macs
Running into challenges using tensorflow on an Apple Silicon Mac machine (M1/M2)? Recently, I encountered an error message after attempting to install tensorflow in a conda ARM64 environment.
```
zsh: illegal hardware instruction
```

I found that the following code was the most efficient solution to this specific problem:
```
conda config --add channels conda-forge # if not already added
conda config --set channel_priority strict 
 
conda create -y --name your_environment_name
conda activate your_environment_name
conda install -y -c apple tensorflow-deps==2.10.0
python -m pip install tensorflow-macos==2.10.0
python -m pip install tensorflow-metal==0.6.0
```

You can confirm this was successful by activating Python and running the following commands:
```
import tensorflow as tf
print('tensorflow version', tf.__version__)
```
This should print "tensorflow version 2.10.0" as specified during the download above. While this solution works for the specific problem identified above, it may not work for others. I recommend checking out the reference below for other potential approaches.

## Reference
https://stackoverflow.com/questions/72964800/what-is-the-proper-way-to-install-tensorflow-on-apple-m1-in-2022
