# sample-size
Sample size extraction from scientific writing. Currently designed for abstracts of articles with human subjects, but can be improved for other uses.

Installation
--
```shell
cd /desired/location/of/package/
git clone git@github.com:NBCLab/samplesize.git
cd samplesize/

# for users:
python setup.py install

# for developers:
python setup.py develop
```

Usage
--
```python
import samplesize as ss

folder = '/some/folder/with/abstracts/as/text/files/'
df = ss.find_corpus(folder)
```
