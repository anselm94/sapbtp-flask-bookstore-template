CF_API = https://api.cf.us10.hana.ondemand.com
CF_ORG = S4HANAD@S_sap-build-training-hcd2uswp
CF_SPACE = dev

.PHONY: login build deploy undeploy

login:
	@echo "Logging into Cloud Foundry..."
	cf login -a $(CF_API) -o $(CF_ORG) -s $(CF_SPACE) --sso

build:
	@echo "Building the project with MBT..."
	mbt build

deploy:
	@echo "Deploying to Cloud Foundry using MBT..."
	cf deploy mta_archives/$(shell ls mta_archives | grep .mtar | tail -n 1)

undeploy:
	@echo "Undeploying from Cloud Foundry..."
	cf undeploy sapbtp-flask-bookstore --delete-services
