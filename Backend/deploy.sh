#!/bin/bash

REPOSITORY=/home/ec2-user
PROJECT_NAME=CoTEVer-Server

rm ../nohup.out

sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-ports 8080

cd $REPOSITORY/$PROJECT_NAME/

echo "> Git Pull"

git pull

gradle build -x test

cd $REPOSITORY

cp $REPOSITORY/$PROJECT_NAME/build/libs/CoTEVer-0.0.1-SNAPSHOT.jar $REPOSITORY/

CURRENT_PID=$(pgrep -f CoTEVer-0.0.1-SNAPSHOT.jar)

echo " 현재 구동중인 애플리케이션pid: $CURRENT_PID"

if [ -z "$CURRENT_PID" ]; then
	echo "> 현재 구동중인 서버가 없음"
else
	kill -15 $CURRENT_PID
	echo "> kill"
	sleep 5
fi

JAR_NAME=$(ls -tr $REPOSITORY/ | grep jar | head -n 1)

nohup java -jar $REPOSITORY/$JAR_NAME 2>&1 &
