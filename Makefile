IMAGE_NAME = "protracking"
AWS_ACCOUNT_ID = "390229387745"
AWS_REGION = "ap-southeast-1"

deploy:
	docker build -t $(IMAGE_NAME) .
	docker tag $(IMAGE_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(IMAGE_NAME):latest
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(IMAGE_NAME):latest
