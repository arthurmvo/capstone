$databaseName = "capstone"
$psqlUser = "postgres"
$password = "arthur"
$dropCommand = "psql -U $psqlUser -h localhost -c 'DROP DATABASE IF EXISTS $databaseName;'"
$createCommand = "psql -U $psqlUser -h localhost -c 'CREATE DATABASE $databaseName;'"


$env:PGPASSWORD = $password
Invoke-Expression $dropCommand
Invoke-Expression $createCommand
echo "ok!"

$env:DATABASE_URL='postgresql://postgres:arthur@localhost:5432/capstone'