############################################## CREATE AWS REPO ##############################################################
DOCKER_REGISTRY=384694669145.dkr.ecr.us-west-1.amazonaws.com
for new_repo in $(grep 'container_name: ' docker-compose_deploy.yml | sed -e 's/container_name: //')
do
	aws ecr create-repository --repository-name "$new_repo" --region us-west-1
done
 #
aws ecr create-repository --repository-name hello-repository --region region


  web:
    container_name: wscontainer
    image: 384694669145.dkr.ecr.us-west-1.amazonaws.com/wscontainer:latest
############################################## LOGIN TO DOCKER USING AWS#########################################################
aws ecr get-login-password --region us-west-1 --profile htran_dev | docker login --username AWS --password-stdin 384694669145.dkr.ecr.us-west-1.amazonaws.com
##################################################################################################################

docker tag hdt1996-portfolionet_proxy:latest 384694669145.dkr.ecr.us-west-1.amazonaws.com/proxycontainer:latest
docker tag hdt1996-portfolionet_web:latest 384694669145.dkr.ecr.us-west-1.amazonaws.com/wscontainer:latest
docker tag timescale/timescaledb:latest-pg14 384694669145.dkr.ecr.us-west-1.amazonaws.com/dbcontainer:latest
#docker tag oznu/cloudflare-ddns:latest 384694669145.dkr.ecr.us-west-1.amazonaws.com/cfcontainer:latest

docker push 384694669145.dkr.ecr.us-west-1.amazonaws.com/proxycontainer:latest
docker push 384694669145.dkr.ecr.us-west-1.amazonaws.com/wscontainer:latest
docker push 384694669145.dkr.ecr.us-west-1.amazonaws.com/dbcontainer:latest
#docker push 384694669145.dkr.ecr.us-west-1.amazonaws.com/cfcontainer:latest
#
docker context create ecs hdt1996-portfolio
docker context use hdt1996-portfolio
docker compose up #RECALL THE LACK OF HYPHEN
aws ecs execute-command --cluster hdt1996-portfolionet --task f888dcb021b848a3827fe32974977654 --container proxycontainer --interactive --command "/bin/sh"

#When permission errors... Double check BOTH JSON!!!!! and Visual editor for GROUP tab in IAM
############################################### Set Up Docker Compose Compatibility #################################
#Linux apt_install contains aws cli docker compose integration

#
# 
################  htran_dev IAMS User #######################
# Access Key ID           AKIAVTEMWZ5M3JNJFFWL
# SECRET FOR AWS          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 


#AWS Access Key ID [None]: AKIAVTEMWZ5M3JNJFFWL
#AWS Secret Access Key [None]: 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
#Default region name [None]: us-west-1
#Default output format [None]: json
