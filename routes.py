from config import app
from controller_functions import test


#test
app.add_url_rule("/",view_func=test)