import os
from Hydroinformatics import compile_less

compile_less.compile_less([os.path.join(os.getcwd(),"public","static")])