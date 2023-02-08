## Map of bat roost

"The “Map a Bat Roost” is a Citizen Science initiative of Bat Conservation India Trust and supported by The Habitats Trust’s Lesser Known Species Grant. The objective of this app is to identify potential roosts of bats, especially colonies so that we can monitor the ecology and population dynamics of the roost in the long run. The data will also help us understand distribution of various species which hitherto is limited. Your contribution for this project would be invaluable."

[Get the app on google play](https://play.google.com/store/apps/details?id=bat_roost.bat_roost)



To start the server, create a python virtual environment.

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
  If the port 8000 is busy, instead run `python manage.py runserver 2020` or a random port between 1025 to 64000 instead of 2020.

