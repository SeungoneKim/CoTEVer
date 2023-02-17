# CoT-Verification-Toolbox-Backend
22-2 소프트웨어 공학 팀플

웹 페이지 도메인 : https://cotever.netlify.app/

웹 페이지 repo : https://github.com/NormalPlayerJSH/CoT-Verification-Toolbox-Frontend

deploy.sh에 있는 

```c
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-ports 8080
```

이 코드가 8080포트로 들어오는 모든 요청을 80 기본 포트로 바꿔줍니다.

