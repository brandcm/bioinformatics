# Using osx64 Programs on M1 Macbooks
Macbooks with the new Apple M1 chip are incredibly fast and efficient, making them indispensiable for bioinformatics. Unfortunately, some commonly used conda packages (particularly those in the Bioconda channel) are not currently available for the native osx-arm64 assembly if your conda was installed for Apple M1 (arm64). If you attempt to install a package in conda, you will receive the following error: 

```
PackagesNotFoundError: The following packages are not available from current channels:
```

There are a handful of solutions to this problem and I describe below what I think is the most straightforward approach.

## Download Rosetta 2
Rosetta is an emulator (or translator depending on who you ask) that translates apps built for Intel so that they can run on Apple.

```
softwareupdate --install-rosetta
```

## Create Conda Environment
Now create a dedicated Conda environment to run osx-64 packages. 

```
CONDA_SUBDIR=osx-64 conda create -n your_environment_name python
conda activate your_environment_name
conda env config vars set CONDA_SUBDIR=osx-64
conda deactivate
conda activate your_environment_name
```

Now try this following code.

```
python -c "import platform;print(platform.machine())"  # Should print "x86_64"
echo "CONDA_SUBDIR: $CONDA_SUBDIR"  # Should print "CONDA_SUBDIR: osx-64"
```

And voila. You can now run osx-64 packages on your M1 Mac! 

## Reference:
https://conda-forge.org/docs/user/tipsandtricks.html
