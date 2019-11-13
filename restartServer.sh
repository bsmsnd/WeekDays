# Script to restart server
echo "should call 'workon django' before running the script"
./manage.py makemigrations
./manage.py migrate
sudo systemctl restart apache2
