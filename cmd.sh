for i in {1..50}; do curl -s -o /dev/null -w "%{http_code}\n" https://ai.testtikee.com/api/v1/chat; done
