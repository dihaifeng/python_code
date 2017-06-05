#!/bin/bash

#参数化构建

#https://yq.aliyun.com/articles/53971 
#Jenkins官网:https://jenkins.io/index.html
#https://en.wikipedia.org/wiki/Comparison_of_continuous_integration_software
#http://www.techweb.com.cn/network/system/2016-01-28/2270191.shtml

"-----------------------------------------------------------------
echo $deploy_envirenment 
case $deploy_envirenment in 
  deploy) 
     echo "deploy: $deploy_envirenment" ansible webservers -m script -a "~/bashscript/xxxxxx_deploy.sh --local-repository=/www/test/test --repository-url=git仓库地址 --backup-dir=/www/test/bak --webdir=/www/test/www" ;;
  rollback) 
     echo "rollback: $deploy_envirenment" ansible webservers -m script -a '~/bashscript/xxxxxx_rollback.sh --backup-dir=/www/test/bak --webdir=/www/test/www' ;; *)
  exit;;
esac

deploy_envirenment
deploy
rollback 
