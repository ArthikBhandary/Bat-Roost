## Map of bat roost

To get started, create a python virtual environment.

Shell comands

 ```
 pip install virtualenv
 virtualenv myenv
 source myenv/bin/activate
 ```

  ### Install the required libraries

  ```
  pip install -r requirements.txt
  ```

  ### Apply migrations

  ```
  cd bat_roost
  python manage.py makemigrations
  python manage.py migrate
  ```

  ### Run local server

  ```
  python manage.py runserver
  ```

  The server should run on [127.0.0.1:8000](127.0.0.1:8000) .
  If the port 8000 is busy, instead run `python manage.py runserver 2020` or a random port between 0 to 64000 instead of 2020.

  # NOTE

Only [127.0.0.1:8000/login](127.0.0.1:8000/login) is implemented now
