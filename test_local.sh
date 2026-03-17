export $(cat .env.local | grep -v '^#' | grep -v '^$' | xargs)

if [ -z "$1" ]; then
    python manage.py test
else
    python manage.py test "$1"
fi

# usage example

#./test_local.sh to test all apps
#./test_local.sh {app_name} to test specific app