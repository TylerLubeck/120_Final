#Rate Limit Rodeo#

##Contents##

* ratelimit.py - This file contains the code for the python/django decorator. It is the meat of the project.

* 120-final-project-presentation - This directory contains the slides for the presentation. It is a submodule that will bring you to a repo managed by Alex Lenail. Please see the README contained therein.

* sample - This directory contains a Django app that allows us to demonstrate the ratelimiting. 

* requirements.txt - a pip requirements file that lists the requirements for the Django sample app.

* infinitehits.sh && slowhits.sh - bash scripts that will demonstrate the ratelimiting.


##What it is##

ratelimit.py contains comments that describe the process in detail, but the gist of it is this:

1. A request is made to a decorated endpoint
2. The decorator is called, and a cacheing key is built. For the prototype, this key is a combination of the name of the wrapped view, and the IP address of the requestor
3. We attempt to retrieve a value from the cache using the key.
4. If a value is NOT found, we allow the request through to the view function. We also do some math to determine how long until a request from that key should be allowed in again. We then insert they key in to the cache, and set the timeout to be the time determined in the math step.
5. If a value IS found, it means that the requestor has tried to access the endpoint too recently. They are not allowed in to the view, and are given an error message in JSON format.

##Running the sample##

1. Make sure you have memcached installed on your machine
2. Create a python virtual environment, and with it active, run: 
```
pip install -r requirements.txt
```
3. From the sample directory, run
```
python manage.py runserver
```
4. Run the two test scripts with
```
bash infinitehits.sh
bash slowhits.sh
```


