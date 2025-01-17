if [ -d "ulab" ]; then
  echo "Directory 'ulab' exists. Backing up 'ulab.h'..."
  cp ulab/code/ulab.h /ulab_old.h
fi
echo "Cloning the 'micropython-ulab' repository..."
git clone https://github.com/v923z/micropython-ulab ulab