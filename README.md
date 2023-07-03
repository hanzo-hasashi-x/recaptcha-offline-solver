# About Solver

This solver is able to solve recaptcha(audio version), with using selenium(undetected-chromedriver) without using online API.

### License
GNU Lesser General Public License v3.0


### Demo

![Demo](demo.gif "demo(speed: 1.35x)")

### To install

```
pip install undetected-chromedriver, pydub, vosk, soundfile, librosa
git clone https://github.com/hanzo-hasashi-x/recaptcha-offline-solver.git
```

### To test 

```
from recaptcha import main

chromedriver_path = 'your chromedriver path'
main(chromedriver_path)
```


### To use

```
from recaptcha import solving_recaptcha

solving_recaptcha(driver, action, driver_path)
```
